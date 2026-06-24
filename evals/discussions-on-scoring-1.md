# Discussion on Scoring — Session 1

**Date:** 2026-06-24
**Participants:** Steve Pousty (human evaluator), Claude (AI evaluator)
**Context:** First manual scoring exercise — Java bubble-sort submissions from 4 models (Qwen Q8, Qwen Q4, Mellum Q8, Mellum Q6)

---

## What happened

After Steve scored all four Java submissions, Claude independently scored the same code against the same rubric. Both evaluators then compared scores and discussed disagreements.

### Score comparison

| Dimension | Qwen Q8 (Steve / Claude) | Qwen Q4 (Steve / Claude) | Mellum Q8 (Steve / Claude) | Mellum Q6 (Steve / Claude) |
|-----------|:---:|:---:|:---:|:---:|
| Naming | 3 / 4 | 4 / 4 | 4 / 4 | 5 / 4 |
| Documentation | 3 / 4 | 4 / 4 | 5 / 4 | 5 / 4 |
| Language Idiom | 5 / 5 | 5 / 5 | 5 / 5 | 4 / 4 |
| Structure | 3 / 5 | 5 / 5 | 4 / 5 | 4 / 5 |
| Edge Cases | 4 / 4 | 4 / 4 | 5 / 5 | 5 / 5 |
| **Total** | **18\* / 22** | **22 / 22** | **23 / 23** | **23 / 22** |

\* Steve wrote 19 but 3+3+5+3+4 = 18.

### Key disagreements

**Biggest gap: Qwen Q8 Structure (Steve 3, Claude 5).** Steve felt lines 46–50 had poor naming and hard-to-follow logic. Claude argued the `compareTasks` helper IS cleanly separated — those lines are standard swap mechanics that wouldn't confuse a Java developer.

**Documentation philosophy (all models).** Claude initially docked both Mellum models from 5 to 4 for "redundant" inline comments like `// Both null: sort by createdAt ascending`. Steve pushed back: inline comments that explain the business rule at the point of implementation are a distinct documentation layer, not redundancy. This led to a rubric update (see below).

**Int vs boolean comparator (Mellum models).** Steve docked both Mellum models on Structure for using an int-returning `compare` method instead of a boolean `shouldSwap`. Claude argued this is a standard Java Comparator pattern. Both positions have merit — boolean is simpler for bubble sort, but int is a well-known idiom.

---

## Insight: two kinds of inline documentation

Steve identified a distinction the original rubric didn't capture:

- **Rule-level inline comments** (valuable): `// Both null: sort by createdAt ascending` — explains the business rule being implemented at that exact line. Saves the reader from scrolling to the docstring and mapping it back.
- **Mechanical inline comments** (noise): `// increment i`, `// Record is immutable; no explicit constructor needed` — restates the code or explains language features.

**Action taken:** Updated `rubric.md` Documentation criteria to explicitly value inline comments that explain business rules and intent at the point of implementation, while still penalizing mechanical restatements.

---

## Insight: relative ranking vs absolute scoring

Steve observed that he found it easier to compare models against each other ("I'd prefer to inherit this code from a junior developer") than to score each model against an absolute standard. Specific challenges:

1. **Difficulty calibrating on a 5-point scale.** Distinguishing a 3 from a 4 requires a clear mental model of what "perfect" looks like. Without that anchor, scores drift toward relative positioning.

2. **No gold standard to deviate from.** The rubric describes each level, but a reference implementation scored at 5/5/5/5/5 would make it easier to identify and quantify deviations.

3. **Natural bias toward ranking.** When evaluating multiple submissions, the brain naturally sorts them best-to-worst rather than assigning absolute scores. Steve's scores had a 5-point spread (18–23) while Claude's had a 1-point spread (22–23) — the actual quality differences are small, but relative ranking amplifies them.

4. **RLHF analogy.** Steve noted this mirrors the difference between reinforcement learning from human feedback (pairwise preference: "A is better than B") and supervised scoring (absolute: "A is a 4.2"). RLHF works well precisely because pairwise preference is a more natural human judgment than absolute scoring. Our benchmark asks for absolute scores, but the evaluator's natural mode is relative preference.

### Possible implications for the benchmark

- **Pairwise comparison** might be a more reliable evaluation format than absolute scoring, at least for dimensions where quality differences are subtle.
- **Anchor examples** at each score level (not just the single scorecard_example.md) could help calibrate absolute scoring.
- **Inter-rater reliability** is measurable now that we have two independent scorers (Steve and Claude). The disagreements reveal which rubric dimensions are underspecified.
- The current 5-point scale may have more resolution than evaluators can reliably use — a 3-point scale (below expectations / meets expectations / exceeds expectations) might produce more consistent results across evaluators.

---

## Open questions

1. Should we add a scored reference implementation as a "gold standard" anchor?
2. Is pairwise comparison ("which code would you rather inherit?") a useful supplement to absolute scoring?
3. Should the scale be simplified for dimensions where inter-rater agreement is low?
4. How do we handle evaluator-specific preferences (e.g., inline documentation, boolean vs int comparators) without undermining cross-evaluator consistency?
