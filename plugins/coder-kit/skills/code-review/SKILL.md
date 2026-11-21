---
name: code-review
description: Review code changes (a diff, PR, file or pasted snippet) for correctness bugs, security issues, performance, readability and test gaps, and report prioritized findings. Use when the user asks to review code, check a PR or diff, find bugs, or give feedback on an implementation.
---

# Code review

Reply in the user's language (Vietnamese if they write in Vietnamese). Keep code, identifiers and quoted errors as-is.

## 1. Establish scope
- Identify what is being reviewed: a git diff (`git diff`, `git diff main...HEAD`), a PR, specific files, or a pasted snippet.
- Find the intent: PR description, commit message, linked issue, or ask in one line if it is truly unclear.
- Skim surrounding code that the change calls or is called by. Do not review only the changed lines in isolation.

## 2. Review in priority order
Work top-down; stop polishing style if there are real bugs.

1. **Correctness** – logic errors, off-by-one, wrong conditions, null/None handling, unhandled errors, race conditions, broken invariants, wrong API use, behaviour that contradicts the stated intent.
2. **Security** – injection (SQL, shell, template), secrets in code or logs, missing authz checks, unsafe deserialization, path traversal, SSRF, overly broad permissions. See `references/checklist.md`.
3. **Data & state** – migrations that lose data, non-idempotent jobs, missing transactions, cache invalidation, timezone and encoding bugs.
4. **Performance** – N+1 queries, quadratic loops on large inputs, loading whole datasets into memory, missing indexes, blocking I/O in async code.
5. **Tests** – does a test fail without this change? Are edge cases and error paths covered?
6. **Maintainability** – naming, duplication, dead code, overly clever code, missing docs for non-obvious decisions.

## 3. Verify before reporting
For each candidate finding, construct a concrete failure scenario (input/state → wrong result). If you cannot, downgrade it to a question or drop it. Prefer few, high-confidence findings over many speculative ones. When you can run code or tests, do so to confirm.

## 4. Report
Use this format:

```
## Summary
<1–3 sentences: overall verdict (approve / approve with nits / request changes) and the main risk>

## Findings
### [severity] <short title> — `path/file.py:42`
<what is wrong, the concrete failure scenario, and a suggested fix (code if short)>
```

Severity: `blocker` (bug, security, data loss) · `major` (likely bug or significant risk) · `minor` (should fix) · `nit` (optional style).
Order findings by severity. End with what you did NOT check (e.g. "did not run tests").

## Tone
Be direct and specific; critique code, not people. Acknowledge good decisions briefly when notable.
