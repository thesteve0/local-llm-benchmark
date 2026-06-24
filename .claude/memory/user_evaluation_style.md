---
name: user-evaluation-style
description: User finds relative/pairwise comparison more natural than absolute scoring, struggles with 5-point scale calibration
metadata:
  type: user
---

When evaluating model code output, Steve's natural mode is relative ranking ("which code would I prefer to inherit from a junior developer") rather than absolute scoring against a rubric. He recognizes this as an inherent bias and noted it mirrors the RLHF vs supervised scoring distinction.

Specific challenges with the current 5-point absolute scale:
- Difficulty distinguishing adjacent levels (3 vs 4) without a clear "gold standard" anchor
- Scores drift toward relative positioning between submissions rather than absolute quality
- Easier to give feedback ("here's what I'd tell the junior dev") than assign a number

Related: [[feedback-inline-docs]]
