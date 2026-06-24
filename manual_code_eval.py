#!/usr/bin/env python3

import json
import re
import time
import requests
from pathlib import Path

HOST = "http://localhost:8081"
MODEL = "Qwen3.6-35B-A3B-UD-Q4_K_M"
PROMPT_FILE = "evals/bubble-sort/rust/prompt.md"
OUTPUT_DIR = "evals/bubble-sort/rust/qwen-q4"
OUTPUT_TO_TERM = True

LANG_CODE_FILENAMES = {
    "python": "bubble_sort.py",
    "java": "BubbleSortTasks.java",
    "rust": "lib.rs",
}

REPO_ROOT = Path(__file__).parent


def detect_language(prompt_path: str) -> str:
    match = re.search(r'/(\w+)/prompt\.md$', prompt_path)
    if not match:
        raise ValueError(f"Cannot detect language from prompt path: {prompt_path}")
    lang = match.group(1).lower()
    if lang not in LANG_CODE_FILENAMES:
        raise ValueError(f"Unknown language '{lang}' in path. Expected one of: {list(LANG_CODE_FILENAMES.keys())}")
    return lang


def extract_code(response_text: str) -> str:
    blocks = re.findall(r'```\w*\n(.*?)```', response_text, re.DOTALL)
    if not blocks:
        print("\nWARNING: No fenced code blocks found in response. Saving raw response as code.")
        return response_text
    return "\n".join(block.strip() for block in blocks)


def run_eval():
    prompt_path = REPO_ROOT / PROMPT_FILE
    prompt_text = prompt_path.read_text()
    lang = detect_language(PROMPT_FILE)
    code_filename = LANG_CODE_FILENAMES[lang]

    request_body = {
        "model": "local",
        "messages": [{"role": "user", "content": prompt_text}],
        "stream": True,
        "stream_options": {"include_usage": True},
        "temperature": 0.0,
    }

    print(f"Model      : {MODEL}")
    print(f"Host       : {HOST}")
    print(f"Prompt     : {PROMPT_FILE}")
    print(f"Language   : {lang}")
    print(f"Code file  : {code_filename}")
    print(f"Output dir : {OUTPUT_DIR}")
    print(f"\nPrompt:\n{prompt_text}\n")

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

    out_dir = REPO_ROOT / OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    _write_trace(out_dir, prompt_text, reasoning_text, content_text,
                 ttft, total_time, reasoning_tokens, answer_tokens, completion_tokens)
    _write_code(out_dir, code_filename, content_text)


def _write_trace(out_dir, prompt_text, reasoning_text, content_text,
                 ttft, total_time, reasoning_tokens, answer_tokens, total_tokens):
    safe_model = MODEL.replace(":", "_")
    out_path = out_dir / f"{safe_model}.md"

    lines = [
        f"# Code Eval: {MODEL}",
        "",
        "## Prompt",
        "",
        prompt_text,
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
    print(f"\nTrace written to: {out_path}")


def _write_code(out_dir, code_filename, content_text):
    code = extract_code(content_text)
    out_path = out_dir / code_filename
    out_path.write_text(code + "\n")
    print(f"Code written to:  {out_path}")


if __name__ == "__main__":
    run_eval()
