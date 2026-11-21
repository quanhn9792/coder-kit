# Framework snippets

## pytest
```python
import pytest

@pytest.mark.parametrize("raw, expected", [
    ("", 0),
    ("1", 1),
    ("1,2,3", 6),
])
def test_sum_csv_valid_input_returns_total(raw, expected):
    assert sum_csv(raw) == expected

def test_sum_csv_non_numeric_raises():
    with pytest.raises(ValueError, match="not a number"):
        sum_csv("1,a")

@pytest.fixture
def frozen_now(monkeypatch):
    import datetime as dt
    fixed = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
    monkeypatch.setattr("app.clock.now", lambda: fixed)
    return fixed
```
Useful: `pytest -x -q`, `--lf` (last failed), `-k name`, `pytest-cov --cov=src --cov-report=term-missing`, `pytest-xdist -n auto`.

## Jest / Vitest
```ts
describe("formatPrice", () => {
  it.each([[0, "0 ₫"], [1000, "1.000 ₫"]])("formats %d", (input, out) => {
    expect(formatPrice(input)).toBe(out);
  });
  it("throws on negative", () => {
    expect(() => formatPrice(-1)).toThrow(/negative/);
  });
});
```
Use `vi.useFakeTimers()` / `jest.useFakeTimers()` for time.

## Playwright (E2E)
```ts
import { test, expect } from "@playwright/test";
test("user can log in", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill("user@example.com");
  await page.getByLabel("Password").fill("secret");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();
});
```
Prefer role/label locators; rely on auto-waiting `expect`, never `waitForTimeout`.

## Data tests (pandas / pandera)
```python
import pandera as pa
schema = pa.DataFrameSchema({
    "order_id": pa.Column(str, unique=True, nullable=False),
    "amount": pa.Column(float, pa.Check.ge(0)),
})
schema.validate(df)
```
