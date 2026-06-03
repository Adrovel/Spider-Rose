# Spider Rose Product Decisions

Version: 0.1.0  
Status: Active decision system  
Last updated: 2026-06-03

Purpose: keep Spider Rose product decisions explicit, reviewable, and separated from ambiguous questions.

## Rule

Ambiguous questions and product decisions belong in the same Spider Rose app, under this `product-decisions` folder.

Do not treat an ambiguous product question as a decision.

Questions begin in `Ambiguous-Questions.md` when the answer is unclear, partial, contradictory, or still being explored. Once Joel gives enough clarity, move the question into `Product-Decisions.md` using the product decision format.

## Files

- `Product-Decisions.md` — clarified product decisions in question, answer, decision, and follow-up format.
- `Ambiguous-Questions.md` — queued product questions that are not ready to become decisions.

## Decision Flow

1. Ask a focused product question.
2. If the answer is clear, write it in `Product-Decisions.md`.
3. If the answer is uncertain, write it in `Ambiguous-Questions.md`.
4. When clarity arrives, move it from the queue into `Product-Decisions.md`.
5. Implementation should follow product decisions, not queued ambiguous questions.

## Product Decisions Format

```text
Question:
Answer:
Decision:
Follow-up:
```
