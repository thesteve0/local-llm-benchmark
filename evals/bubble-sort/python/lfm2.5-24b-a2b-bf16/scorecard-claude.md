# Scorecard — LFM2.5-24B-A2B-BF16 (python, AI MAX+ 395)

- Tests: **11/11 passed** (run_tests.py)
- Quality: **24/25** — Naming 5, Docs 5, Idiom 4, Structure 5, Edge 5. Python: mixed typing style (typing.List unused-with Dict/Tuple imports, builtin generics in signature); otherwise correct 3-way ordering, early exit, n-i-1. Java: records + Integer.compare/Long.compare (avoids boxed pitfall); minor 'temp' lapse.
- Perf (timings): gen 7240 tokens @ 11.4-11.8 t/s (~10 min); prompt eval ~240 t/s; server cold-restarted; temp 0.0
