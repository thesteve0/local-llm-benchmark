#!/usr/bin/env python3

import argparse
import json
import time
import requests
from pathlib import Path

DEFAULT_HOST = "http://localhost:8080"
DEFAULT_MODEL = "NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16"
DEFAULT_OUTPUT = "output/manual_eval/transformer_v_mamba"
DEFAULT_TEMPERATURE = 0.0
OUTPUT_TO_TERM = True
PROMPT = (
"""
 Write a comprehensive, detailed technical essay of at least 500 words and less than 1000 words, explaining the architectural differences between Transformer-based Large Language Models and State Space Models (like Mamba). Discuss their respective approaches to the attention mechanism, computational complexity regarding sequence length, and their practical implications for long-context window processing. Use an academic, introductory course style of writing and tone.
"""
)

REPO_ROOT = Path(__file__).parent


def server_timing_lines(timings: dict) -> list[str]:
    """Format authoritative llama.cpp server-side timing fields."""
    if not timings:
        return []
    lines = []
    if timings.get("prompt_n") is not None:
        lines.append(f"- Prompt tokens: {timings['prompt_n']}")
    if timings.get("prompt_per_second") is not None:
        lines.append(f"- Prompt eval speed: {timings['prompt_per_second']:.2f} t/s")
    if timings.get("prompt_ms") is not None:
        lines.append(f"- Prompt eval time: {timings['prompt_ms']:.2f} ms")
    if timings.get("predicted_n") is not None:
        lines.append(f"- Generation tokens: {timings['predicted_n']}")
    if timings.get("predicted_per_second") is not None:
        lines.append(f"- Generation speed: {timings['predicted_per_second']:.2f} t/s")
    if timings.get("predicted_ms") is not None:
        lines.append(f"- Generation time: {timings['predicted_ms']:.2f} ms")
    return lines


def parse_args():
    parser = argparse.ArgumentParser(description="Run the essay evaluation against llama.cpp.")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help="Output path prefix; model name is appended with an underscore")
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--no-output", action="store_true",
                        help="Do not stream reasoning/answer text to the terminal")
    return parser.parse_args()


def run_eval(args):
    request_body = {
        "model": "local",
        "messages": [{"role": "user", "content": PROMPT}],
        "stream": True,
        "stream_options": {"include_usage": True},
        "temperature": args.temperature,
    }

    print(f"Model : {args.model}")
    print(f"Host  : {args.host}")
    print(f"Temperature: {args.temperature}")
    print(f"\nPrompt:\n{PROMPT}\n")

    reasoning_chunks = []
    content_chunks = []
    start = time.perf_counter()
    first_token_at = None
    active_field = None
    usage = {}
    timings = {}

    with requests.post(
        f"{args.host}/v1/chat/completions",
        json=request_body,
        stream=True,
        timeout=900,
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
            if chunk.get("timings"):
                timings = chunk["timings"]

            choices = chunk.get("choices")
            if not choices:
                continue
            delta = choices[0].get("delta", {})
            for field, store in (("reasoning_content", reasoning_chunks), ("content", content_chunks)):
                token = delta.get(field)
                if not token:
                    continue
                if first_token_at is None:
                    first_token_at = time.perf_counter()
                if OUTPUT_TO_TERM and not args.no_output and active_field != field:
                    active_field = field
                    print("\n" + "=" * 70)
                    print("REASONING" if field == "reasoning_content" else "RESPONSE")
                    print("=" * 70)
                store.append(token)
                if OUTPUT_TO_TERM and not args.no_output:
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

    print("\n" + "=" * 70)
    print("\n--- Timing ---")
    if ttft is not None:
        print(f"Time to first token : {ttft:.2f}s")
    print(f"Total generation    : {total_time:.2f}s")
    print("\n--- Tokens ---")
    print(f"Reasoning tokens    : {reasoning_tokens}")
    print(f"Answer tokens       : {answer_tokens}")
    print(f"Total tokens        : {completion_tokens}")
    if timings:
        print("\n--- Server timings (llama.cpp) ---")
        for line in server_timing_lines(timings):
            print(line[2:])

    _write_output(args, reasoning_text, content_text, ttft, total_time,
                  reasoning_tokens, answer_tokens, completion_tokens, timings)


def _write_output(args, reasoning_text, content_text, ttft, total_time,
                  reasoning_tokens, answer_tokens, total_tokens, timings=None):
    safe_model = args.model.replace(":", "_")
    out_path = REPO_ROOT / f"{args.output}_{safe_model}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# Manual Eval: {args.model}", "", "## Prompt", "", PROMPT, ""]
    if reasoning_text:
        lines += ["## Reasoning", "", reasoning_text, ""]
    lines += ["## Response", "", content_text, "", "## Timings", ""]
    if ttft is not None:
        lines.append(f"- Time to first token: {ttft:.2f}s")
    lines += [f"- Temperature: {args.temperature}", f"- Total generation: {total_time:.2f}s",
              f"- Reasoning tokens: {reasoning_tokens}", f"- Answer tokens: {answer_tokens}",
              f"- Total tokens: {total_tokens}", ""]
    server_lines = server_timing_lines(timings or {})
    if server_lines:
        lines += ["## Server Timings (llama.cpp)", "", *server_lines, ""]
    out_path.write_text("\n".join(lines))
    print(f"\nOutput written to: {out_path}")


if __name__ == "__main__":
    run_eval(parse_args())
