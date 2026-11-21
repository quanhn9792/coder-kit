# Review checklist (load when reviewing security-sensitive or large changes)

## Security
- [ ] User input reaches SQL/shell/HTML/templates only through parameterization or escaping
- [ ] No secrets, tokens or PII in code, config committed to git, logs or error messages
- [ ] Every new endpoint/handler checks authentication AND authorization
- [ ] File paths from input are normalized and confined
- [ ] Outbound requests to user-supplied URLs are restricted (SSRF)
- [ ] Deserialization (pickle, yaml.load, eval) never touches untrusted data
- [ ] Dependencies added are pinned and from trusted sources

## Reliability
- [ ] Errors are handled or propagated deliberately, not swallowed
- [ ] Retries have backoff and are safe (idempotent operation)
- [ ] Timeouts on network/database calls
- [ ] Resources (files, connections, locks) are released (context managers / finally)
- [ ] Concurrency: shared state is protected; no check-then-act races

## Data
- [ ] Migrations are backward compatible and reversible, or the plan is documented
- [ ] Timezones explicit (UTC storage), encodings explicit (UTF-8)
- [ ] Money/precision uses decimal types

## Language specifics
- Python: mutable default args, broad `except:`, `is` vs `==`, late-binding closures in loops
- JS/TS: `==` vs `===`, unhandled promise rejections, `any` leaks, missing `await`
- SQL: `NULL` comparisons, implicit casts, `SELECT *` in production code, missing `WHERE` on UPDATE/DELETE
- Go: ignored `err`, goroutine leaks, loop variable capture (pre-1.22)
