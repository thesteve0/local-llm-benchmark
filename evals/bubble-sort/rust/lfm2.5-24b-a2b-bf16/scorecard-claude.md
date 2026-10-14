# Scorecard — LFM2.5-24B-A2B-BF16 (rust, AI MAX+ 395)

- Tests: **0/11** — compile failure E0753: model emitted a second `//!` inner-doc block mid-file (lines 16-24) after the Task struct. Extraction verified byte-for-byte vs trace = model bug, not tooling.
- Quality: **19/25** (visible code is well-structured: Task struct, derives, docs — but invalid Rust). Mirrors Nemotron's 0/11-but-good-code treatment.
- Perf: 6,478 tokens @ 11.42 t/s; prompt eval ~241 t/s; temp 0.0; server cold-restarted.
