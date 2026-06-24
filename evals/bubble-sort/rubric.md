# Code Quality Rubric — Bubble Sort Eval

Score each dimension 1–5. Total: 25 points.

## 1. Naming (1–5)

| Score | Criteria |
|------:|----------|
| 5 | All names are descriptive and self-documenting. Language conventions followed perfectly (snake_case for Python/Rust, camelCase for Java). |
| 4 | Good names throughout with one minor lapse (e.g., a single-letter loop variable where a name would help). |
| 3 | Acceptable names but some are generic (e.g., `temp`, `result`, `data` where a more specific name would clarify intent). |
| 2 | Several unclear or misleading names. Mixed conventions. |
| 1 | Single-letter variables, cryptic abbreviations, or wrong language conventions throughout. |

## 2. Documentation (1–5)

Documentation has two layers, both of which matter:
- **External documentation** (docstrings, Javadoc, doc-comments): summarizes what a function/class does, its parameters, return value, and key rules.
- **Inline documentation**: explains the business rule or intent at the point of implementation. Comments like `// Both null: sort by createdAt ascending` add value even if the rule is also in the docstring, because they provide context right where the reader needs it. This is distinct from mechanical restatements of the code itself (e.g., `// increment i`).

| Score | Criteria |
|------:|----------|
| 5 | Clear docstring/doc-comment explaining: what the function does, the sorting rules, parameters, return value, and null/None handling. Inline comments explain business rules and intent at the point of implementation. No purely mechanical restatements of code. |
| 4 | Good external documentation covering most of the above. Minor omission (e.g., doesn't mention null handling explicitly). Inline comments present but incomplete or inconsistent. |
| 3 | Has a docstring but it's either too terse ("sorts tasks") or missing inline documentation of business rules. |
| 2 | Minimal or boilerplate documentation that doesn't explain the sorting rules. No meaningful inline comments. |
| 1 | No documentation at all. |

## 3. Language Idiom (1–5)

| Score | Criteria |
|------:|----------|
| 5 | Fully idiomatic. **Python:** type hints, appropriate use of list/dict patterns. **Java:** records (or well-structured classes), generics, proper access modifiers. **Rust:** correct ownership/borrowing, idiomatic Option handling (match/map/unwrap_or), derive macros. |
| 4 | Mostly idiomatic with one non-idiomatic choice that still works. |
| 3 | Functional but written in a style that feels like another language translated. |
| 2 | Fights the language — e.g., manual memory management patterns in Python, C-style loops in Rust. |
| 1 | Broken or deeply non-idiomatic code that a practitioner would reject in review. |

## 4. Structure (1–5)

| Score | Criteria |
|------:|----------|
| 5 | Comparison logic is cleanly separated (helper function or clear inline block). Function is a reasonable length. No unnecessary abstractions, no missing helpful ones. |
| 4 | Good structure with a minor issue (e.g., comparison logic slightly tangled with swap logic but still readable). |
| 3 | Everything in one function but still followable. Or over-engineered with unnecessary classes/abstractions. |
| 2 | Hard to follow the flow. Comparison logic is scattered or duplicated. |
| 1 | Spaghetti code or massively over-engineered for a bubble sort. |

## 5. Edge Case Handling (1–5)

| Score | Criteria |
|------:|----------|
| 5 | Handles empty list, single element, and all-null priorities gracefully without special-case branches — the main logic just works. |
| 4 | Handles all edge cases correctly but with unnecessary explicit checks (e.g., `if len(tasks) <= 1: return`). |
| 3 | Handles most edge cases but one path is fragile or would crash on unexpected input. |
| 2 | Crashes or returns wrong results on at least one edge case (empty, single, all-null). |
| 1 | No edge case consideration. Crashes on empty input. |
