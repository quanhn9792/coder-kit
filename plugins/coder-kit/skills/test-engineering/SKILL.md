---
name: test-engineering
description: Software testing guidance - write test plans, test cases and automated tests (unit, integration, end-to-end, API, data and ML tests), find coverage gaps and fix flaky tests. Use when the user asks to write or improve tests, design test cases, review test quality, set up pytest/Jest/Playwright, or debug failing or flaky tests.
---

# Test engineering

Reply in the user's language. Act as a senior QA/SDET: tests should catch real regressions, run fast, and be deterministic.

## Workflow
1. **Understand behaviour** – read the code/spec; list the requirements and the risks (what breaks costs most).
2. **Design cases** with these techniques:
   - Equivalence partitions and boundary values (0, 1, max, max+1, empty, null, unicode, very long).
   - Error paths: invalid input, timeouts, dependency failures, permissions.
   - State transitions and ordering; concurrency where relevant.
   - For data/ML: schema, nulls, duplicates, distributions, model metric thresholds, determinism.
3. **Pick the level** – test pyramid: many unit tests, fewer integration, few E2E. Test at the lowest level that can catch the bug.
4. **Write the tests** following project conventions (detect framework from existing tests/config first).
5. **Run them** when possible, and confirm a new test fails without the fix (or by temporarily breaking the code).

## Writing good tests
- One behaviour per test; name it `test_<unit>_<condition>_<expected>`.
- Arrange–Act–Assert; no logic (loops/ifs) in tests – use parametrization instead.
- Assert on behaviour/outputs, not implementation details or private methods.
- Deterministic: freeze time, seed randomness, no real network; use fakes/mocks only at boundaries (HTTP, DB, clock), prefer real objects inside.
- Fixtures small and explicit; factories over giant shared fixtures.
- Fast: unit test < 100 ms; mark slow/integration tests so they can be selected.
See `references/frameworks.md` for pytest / Jest / Playwright snippets.

## Test plan format (when asked for a plan or test cases)
| ID | Area | Scenario | Steps / Input | Expected | Priority | Type |
|---|---|---|---|---|---|---|

Priority P0 (must pass to release) … P2. Type: unit / integration / e2e / manual / performance / security.

## Flaky tests
Reproduce with repetition (`pytest -p no:randomly --count=50` or `--repeat-each` in Playwright), then check: shared state between tests, ordering dependence, time/timezone, async waits (`sleep` instead of awaiting a condition), network, random data without seed, resource leaks. Fix the root cause; never just add retries or skip.

## When reviewing tests
Use the `code-review` format; check: would the test fail if the code broke? missing edge/error cases, over-mocking, brittle assertions, non-determinism, slow tests.
