#!/usr/bin/env python3

import argparse
import json
import re
import time
import requests
from pathlib import Path

DEFAULT_HOST = "http://localhost:8080"
DEFAULT_MODEL = "NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16"
DEFAULT_PROMPT_FILE = "evals/bubble-sort/java/prompt.md"
DEFAULT_OUTPUT_DIR = "evals/bubble-sort/java/nemotron-3.5-lightning-30b-a3b-bf16"
DEFAULT_TEMPERATURE = 0.0
OUTPUT_TO_TERM = True

LANG_CODE_FILENAMES = {"python": "bubble_sort.py", "java": "BubbleSortTasks.java", "rust": "lib.rs"}
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
    parser = argparse.ArgumentParser(description="Run a coding evaluation against llama.cpp.")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--prompt-file", default=DEFAULT_PROMPT_FILE)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    parser.add_argument("--no-output", action="store_true")
    return parser.parse_args()


def detect_language(prompt_path: str) -> str:
    match = re.search(r"/(\w+)/prompt\.md$", prompt_path)
    if not match:
        raise ValueError(f"Cannot detect language from prompt path: {prompt_path}")
    lang = match.group(1).lower()
    if lang not in LANG_CODE_FILENAMES:
        raise ValueError(f"Unknown language '{lang}' in path")
    return lang


def extract_code(response_text: str) -> str:
    blocks = re.findall(r"```\w*\n(.*?)```", response_text, re.DOTALL)
    if not blocks:
        print("\nWARNING: No fenced code blocks found in response. Saving raw response as code.")
        return response_text
    return "\n".join(block.strip() for block in blocks)


def run_eval(args):
    prompt_path = REPO_ROOT / args.prompt_file
    prompt_text = prompt_path.read_text()
    lang = detect_language(args.prompt_file)
    code_filename = LANG_CODE_FILENAMES[lang]
    request_body = {
        "model": "local",
        "messages": [{"role": "user", "content": prompt_text}],
        "stream": True,
        "stream_options": {"include_usage": True},
        "temperature": args.temperature,
    }
    print(f"Model      : {args.model}\nHost       : {args.host}\nTemperature: {args.temperature}")
    print(f"Prompt     : {args.prompt_file}\nLanguage   : {lang}\nCode file  : {code_filename}")
    print(f"Output dir : {args.output_dir}\n\nPrompt:\n{prompt_text}\n")

    reasoning_chunks, content_chunks = [], []
    start = time.perf_counter()
    first_token_at = None
    active_field = None
    usage, timings = {}, {}
    with requests.post(f"{args.host}/v1/chat/completions", json=request_body,
                       stream=True, timeout=900) as resp:
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
    reasoning_text, content_text = "".join(reasoning_chunks), "".join(content_chunks)
    ttft = (first_token_at - start) if first_token_at else None
    total_time = end - start
    completion_tokens = usage.get("completion_tokens")
    if completion_tokens is not None:
        chars = len(reasoning_text) + len(content_text)
        reasoning_tokens = round(completion_tokens * len(reasoning_text) / chars) if chars else 0
        answer_tokens = completion_tokens - reasoning_tokens
    else:
        reasoning_tokens, answer_tokens = round(len(reasoning_text) / 4), round(len(content_text) / 4)
        completion_tokens = reasoning_tokens + answer_tokens

    print("\n" + "=" * 70 + "\n\n--- Timing ---")
    if ttft is not None:
        print(f"Time to first token : {ttft:.2f}s")
    print(f"Total generation    : {total_time:.2f}s\n\n--- Tokens ---")
    print(f"Reasoning tokens    : {reasoning_tokens}\nAnswer tokens       : {answer_tokens}\nTotal tokens        : {completion_tokens}")
    if timings:
        print("\n--- Server timings (llama.cpp) ---")
        for line in server_timing_lines(timings):
            print(line[2:])

    out_dir = REPO_ROOT / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_trace(out_dir, args, prompt_text, reasoning_text, content_text, ttft,
                 total_time, reasoning_tokens, answer_tokens, completion_tokens, timings)
    _write_code(out_dir, code_filename, content_text)


def _write_trace(out_dir, args, prompt_text, reasoning_text, content_text, ttft,
                 total_time, reasoning_tokens, answer_tokens, total_tokens, timings=None):
    safe_model = args.model.replace(":", "_")
    lines = [f"# Code Eval: {args.model}", "", "## Prompt", "", prompt_text, ""]
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
    path = out_dir / f"{safe_model}.md"
    path.write_text("\n".join(lines))
    print(f"\nTrace written to: {path}")


def _write_code(out_dir, code_filename, content_text):
    path = out_dir / code_filename
    path.write_text(extract_code(content_text) + "\n")
    print(f"Code written to:  {path}")


if __name__ == "__main__":
    run_eval(parse_args())
