#!/usr/bin/env python3

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from manual_code_eval import LANG_CODE_FILENAMES

REPO_ROOT = Path(__file__).parent
LANG_TEST_FILES = {"python": ["test_bubble_sort.py"], "java": ["BubbleSortTasksTest.java"]}


def parse_args():
    parser = argparse.ArgumentParser(description="Run hidden tests for a generated bubble-sort solution.")
    parser.add_argument("--language", choices=LANG_TEST_FILES)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model", default="model")
    return parser.parse_args()


def infer_language(out_dir: Path) -> str:
    matches = [lang for lang, filename in LANG_CODE_FILENAMES.items() if (out_dir / filename).exists()]
    matches = [lang for lang in matches if lang in LANG_TEST_FILES]
    if len(matches) != 1:
        raise ValueError(f"Could not uniquely infer language from {out_dir}; pass --language")
    return matches[0]


def get_eval_dir(out_dir: Path) -> Path:
    # Expected path: evals/bubble-sort/<language>/<run-name>
    parts = out_dir.parts
    try:
        index = parts.index("bubble-sort")
        return REPO_ROOT.joinpath(*parts[:index + 2])
    except ValueError as exc:
        raise ValueError(f"Output directory is not under evals/bubble-sort: {out_dir}") from exc


def count_expected_tests(lang: str, eval_dir: Path) -> int:
    if lang == "python":
        text = (eval_dir / "test_bubble_sort.py").read_text()
        return len(re.findall(r"def test_", text))
    text = (eval_dir / "BubbleSortTasksTest.java").read_text()
    return len(re.findall(r'startTest\("', text))


def copy_test_files(lang: str, eval_dir: Path, out_dir: Path):
    for filename in LANG_TEST_FILES[lang]:
        shutil.copy2(eval_dir / filename, out_dir)


def run_tests(lang: str, out_dir: Path) -> tuple[str, int]:
    if lang == "python":
        result = subprocess.run([sys.executable, "-m", "unittest", "test_bubble_sort", "-v"],
                                cwd=out_dir, capture_output=True, text=True, timeout=60)
    else:
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{out_dir}:/work", "-w", "/work",
             "eclipse-temurin:21", "sh", "-c", "javac *.java && java BubbleSortTasksTest"],
            capture_output=True, text=True, timeout=120)
    return result.stdout + result.stderr, result.returncode


def parse_results(lang: str, output: str) -> tuple[int, int]:
    if lang == "python":
        ran = re.search(r"Ran (\d+) test", output)
        total = int(ran.group(1)) if ran else 0
        failures = len(re.findall(r"^(?:FAIL|ERROR):", output, re.MULTILINE))
        if "OK" in output.split("Ran")[-1] if "Ran" in output else "":
            return total, 0
        return total - failures, failures
    match = re.search(r"Results: (\d+) passed, (\d+) failed", output)
    return (int(match.group(1)), int(match.group(2))) if match else (0, 0)


def cleanup(lang: str, out_dir: Path):
    for filename in LANG_TEST_FILES[lang]:
        (out_dir / filename).unlink(missing_ok=True)
    if lang == "python":
        for path in out_dir.glob("__pycache__"):
            shutil.rmtree(path, ignore_errors=True)
    else:
        for path in out_dir.glob("*.class"):
            path.unlink(missing_ok=True)


def main():
    args = parse_args()
    out_dir = (REPO_ROOT / args.output_dir).resolve()
    lang = args.language or infer_language(out_dir)
    eval_dir = get_eval_dir(out_dir)
    code_filename = LANG_CODE_FILENAMES[lang]
    if not (out_dir / code_filename).exists():
        print(f"ERROR: Code file not found: {out_dir / code_filename}", file=sys.stderr)
        return 1
    print(f"Model      : {args.model}\nLanguage   : {lang}\nOutput dir : {out_dir}")
    copy_test_files(lang, eval_dir, out_dir)
    output, returncode = run_tests(lang, out_dir)
    print(output)
    expected_total = count_expected_tests(lang, eval_dir)
    passed, failed = parse_results(lang, output)
    total = max(expected_total, passed + failed)
    print(f"\n--- Results: {passed} passed, {total - passed} failed (of {total} tests) ---")
    scorecard = out_dir / "scorecard.md"
    scorecard.write_text(f"""# Scorecard: {args.model}\n\n## Test Results\n\n- **Tests passed:** {passed} / {total}\n- **Tests failed:** {total - passed}\n\n## Code Quality (see rubric.md for criteria)\n\n| Dimension | Score (1-5) | Notes |\n|-----------|:-----------:|-------|\n| Naming | | |\n| Documentation | | |\n| Language Idiom | | |\n| Structure | | |\n| Edge Cases | | |\n| **Total** | **/ 25** | |\n\n## Evaluation\n\n- **Evaluator:**\n- **Date:**\n\n## Overall Notes\n\n""")
    print(f"Scorecard written to: {scorecard}")
    cleanup(lang, out_dir)
    return 0 if returncode == 0 and failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
