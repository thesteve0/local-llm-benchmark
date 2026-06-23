#!/usr/bin/env python3

import json
import time
import requests
from pathlib import Path

HOST = "http://localhost:8081"
MODEL = "Qwen3.6-35B-A3B-UD-Q4_K_M"
OUTPUT = "output/manual_eval/transformer_v_mamba"
OUTPUT_TO_TERM = True
PROMPT = (
"""
 Write a comprehensive, detailed technical essay of at least 500 words and less than 1000 words, explaining the architectural differences between Transformer-based Large Language Models and State Space Models (like Mamba). Discuss their respective approaches to the attention mechanism, computational complexity regarding sequence length, and their practical implications for long-context window processing. Use an academic, introductory course style of writing and tone.
"""
)

REPO_ROOT = Path(__file__).parent


def run_eval():
    request_body = {
        "model": "local",
        "messages": [{"role": "user", "content": PROMPT}],
        "stream": True,
        "stream_options": {"include_usage": True},
        "temperature": 0.0,
    }

    print(f"Model : {MODEL}")
    print(f"Host  : {HOST}")
    print(f"\nPrompt:\n{PROMPT}\n")

    reasoning_chunks = []
    content_chunks = []
    start = time.perf_counter()
    first_token_at = None
    active_field = None
    usage = {}

    with requests.post(
        f"{HOST}/v1/chat/completions",
        json=request_body,
        stream=True,
        timeout=300,
    ) as resp:
        resp.raise_for_status()
        for raw_line in resp.iter_lines():
            if not raw_line:
                continue
            line = raw_line.decode("utf-8")
            if not line.startswith("data: "):
                continue
            data = line[len("data: "):]
            if data.strip() == "[DONE]":
                break
            try:
                chunk = json.loads(data)
            except json.JSONDecodeError:
                continue

            if chunk.get("usage"):
                usage = chunk["usage"]

            choices = chunk.get("choices")
            if not choices:
                continue
            delta = choices[0].get("delta", {})
            for field, store in (
                ("reasoning_content", reasoning_chunks),
                ("content", content_chunks),
            ):
                token = delta.get(field)
                if not token:
                    continue
                if first_token_at is None:
                    first_token_at = time.perf_counter()
                if OUTPUT_TO_TERM and active_field != field:
                    active_field = field
                    if field == "reasoning_content":
                        print("\n" + "=" * 70)
                        print("REASONING")
                        print("=" * 70)
                    else:
                        print("\n" + "=" * 70)
                        print("RESPONSE")
                        print("=" * 70)
                store.append(token)
                if OUTPUT_TO_TERM:
                    print(token, end="", flush=True)

    end = time.perf_counter()

    reasoning_text = "".join(reasoning_chunks)
    content_text = "".join(content_chunks)
    ttft = (first_token_at - start) if first_token_at else None
    total_time = end - start

    completion_tokens = usage.get("completion_tokens")
    if completion_tokens is not None:
        total_chars = len(reasoning_text) + len(content_text)
        if total_chars > 0:
            reasoning_tokens = round(completion_tokens * len(reasoning_text) / total_chars)
            answer_tokens = completion_tokens - reasoning_tokens
        else:
            reasoning_tokens = answer_tokens = 0
    else:
        reasoning_tokens = round(len(reasoning_text) / 4)
        answer_tokens = round(len(content_text) / 4)
        completion_tokens = reasoning_tokens + answer_tokens

    if OUTPUT_TO_TERM:
        print("\n" + "=" * 70)
    print("\n--- Timing ---")
    if ttft is not None:
        print(f"Time to first token : {ttft:.2f}s")
    print(f"Total generation    : {total_time:.2f}s")
    print("\n--- Tokens ---")
    print(f"Reasoning tokens    : {reasoning_tokens}")
    print(f"Answer tokens       : {answer_tokens}")
    print(f"Total tokens        : {completion_tokens}")

    _write_output(reasoning_text, content_text, ttft, total_time,
                  reasoning_tokens, answer_tokens, completion_tokens)


def _write_output(reasoning_text, content_text, ttft, total_time,
                  reasoning_tokens, answer_tokens, total_tokens):
    safe_model = MODEL.replace(":", "_")
    out_path = REPO_ROOT / f"{OUTPUT}_{safe_model}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Manual Eval: {MODEL}",
        "",
        "## Prompt",
        "",
        PROMPT,
        "",
    ]

    if reasoning_text:
        lines += [
            "## Reasoning",
            "",
            reasoning_text,
            "",
        ]

    lines += [
        "## Response",
        "",
        content_text,
        "",
        "## Timings",
        "",
    ]
    if ttft is not None:
        lines.append(f"- Time to first token: {ttft:.2f}s")
    lines += [
        f"- Total generation: {total_time:.2f}s",
        f"- Reasoning tokens: {reasoning_tokens}",
        f"- Answer tokens: {answer_tokens}",
        f"- Total tokens: {total_tokens}",
        "",
    ]

    out_path.write_text("\n".join(lines))
    print(f"\nOutput written to: {out_path}")


if __name__ == "__main__":
    run_eval()
