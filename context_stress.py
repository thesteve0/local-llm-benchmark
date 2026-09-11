#!/usr/bin/env python3
"""Run one long-context retrieval probe against a running llama.cpp server."""

import argparse
import json
import time
from pathlib import Path

import requests


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="http://127.0.0.1:8080")
    parser.add_argument("--target-tokens", type=int, required=True)
    parser.add_argument("--needle", default="NEMOTRON_CONTEXT_NEEDLE_739184")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def build_prompt(target_tokens: int, needle: str, chars_per_token: float = 5.8) -> str:
    filler = (
        "This is deterministic context filler for a long context validation request. "
        "It carries no answer and should be ignored while locating the marked record.\n"
    )
    desired_chars = max(1000, int(target_tokens * chars_per_token))
    filler_count = max(1, (desired_chars - 1200) // len(filler))
    sections = [filler] * filler_count
    marker_index = max(0, len(sections) * 3 // 4)
    sections.insert(marker_index, f"The marked record is: {needle}.\n")
    sections.append(
        f"\nEnd of context. Locate the marked record and reply with only this exact code: {needle}\n"
    )
    return "".join(sections)


def calibrate_prompt(host: str, target_tokens: int, needle: str) -> tuple[str, int]:
    prompt = build_prompt(target_tokens, needle)
    for _ in range(3):
        response = requests.post(f"{host}/tokenize", json={"content": prompt}, timeout=300)
        response.raise_for_status()
        actual = len(response.json().get("tokens", []))
        if not actual:
            break
        prompt = build_prompt(target_tokens, needle, len(prompt) / actual * 0.99)
    response = requests.post(f"{host}/tokenize", json={"content": prompt}, timeout=300)
    response.raise_for_status()
    return prompt, len(response.json().get("tokens", []))


def run(args):
    prompt, calibrated_tokens = calibrate_prompt(args.host, args.target_tokens, args.needle)
    payload = {
        "model": "local",
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
        "stream_options": {"include_usage": True},
        "temperature": 0.0,
        "max_tokens": 128,
    }
    started = time.perf_counter()
    content = []
    usage = {}
    timings = {}
    with requests.post(f"{args.host}/v1/chat/completions", json=payload,
                       stream=True, timeout=1800) as response:
        response.raise_for_status()
        for raw_line in response.iter_lines():
            if not raw_line:
                continue
            line = raw_line.decode("utf-8")
            if not line.startswith("data: "):
                continue
            data = line[6:]
            if data.strip() == "[DONE]":
                break
            try:
                chunk = json.loads(data)
            except json.JSONDecodeError:
                continue
            usage.update(chunk.get("usage") or {})
            timings.update(chunk.get("timings") or {})
            choices = chunk.get("choices") or []
            if choices:
                delta = choices[0].get("delta") or {}
                content.append(delta.get("reasoning_content") or "")
                content.append(delta.get("content") or "")
    elapsed = time.perf_counter() - started
    answer = "".join(content).strip()
    result = {
        "target_tokens": args.target_tokens,
        "prompt_chars": len(prompt),
        "calibrated_prompt_tokens": calibrated_tokens,
        "prompt_tokens": timings.get("prompt_n", usage.get("prompt_tokens")),
        "answer": answer,
        "needle_found_exactly": answer == args.needle,
        "needle_found_anywhere": args.needle in answer,
        "generation_tokens": timings.get("predicted_n", usage.get("completion_tokens")),
        "prompt_eval_ms": timings.get("prompt_ms"),
        "prompt_eval_tps": timings.get("prompt_per_second"),
        "generation_ms": timings.get("predicted_ms"),
        "generation_tps": timings.get("predicted_per_second"),
        "wall_seconds": elapsed,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run(parse_args())
