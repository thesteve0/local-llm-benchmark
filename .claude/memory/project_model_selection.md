---
name: model-selection
description: Decided on Qwen 3.6 Q8 (reasoning) + Mellum2 Q8 (coding) as the two-model agentic harness setup on Framework Desktop
metadata:
  type: project
---

Model selection finalized for agentic harness: Qwen 3.6 Q8 as reasoning/orchestration model, Mellum2 Q8 as coding specialty model. Both running locally on Framework Desktop via Ramalama.

**Why:** Three independent evaluations (user on Java, James on Python, Claude on Python) all converged on the same ranking. Mellum2 Q8 consistently produced the best code quality (20-21/25). Qwen 3.6 Q8 scored well on reasoning but had code style issues. The two-model split plays to each model's strengths.

**How to apply:** When building the agentic harness, route reasoning/planning tasks to Qwen 3.6 Q8 and code generation tasks to Mellum2 Q8. Both are served via Ramalama on [[user-hardware]].
