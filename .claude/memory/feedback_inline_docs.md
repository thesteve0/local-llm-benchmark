---
name: feedback-inline-docs
description: User values verbose inline documentation that explains business rules at the point of execution, distinct from class/method-level Javadoc
metadata:
  type: feedback
---

Inline code comments that explain the business rule or intent at the point of implementation are valuable, not redundant — even if the same information is in the class-level Javadoc.

**Why:** User has ADHD and prefers having context right at the point of reading rather than needing to scroll up and map Javadoc back to specific lines. Most LLM-generated code is too sparse on inline documentation.

**How to apply:** When evaluating documentation quality, distinguish between (1) comments that restate the code mechanically (`// increment i`) — bad, and (2) comments that restate the rule being implemented (`// Both null: sort by createdAt ascending`) — good. Don't penalize the second kind. Related: [[feedback-metrics-source]]
