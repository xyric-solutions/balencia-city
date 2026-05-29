---
skill_id: "DEV-05"
name: "Webapp Testing"
version: "v2.0"
category: "development"
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
license: Complete terms in LICENSE.txt
related_skills: EXPERT-04 (QA methodology), DEV-02 (test generation)
---

# DEV-05: Web Application Testing

## Purpose

Test local web applications by writing native Python Playwright scripts. Verify frontend functionality, debug UI behavior, capture screenshots, and inspect browser logs.

## Philosophy

**Test what users experience, not how code is structured.** A test that clicks a button and verifies the resulting page state is valuable. A test that asserts a component's internal state variable changed from `false` to `true` is fragile and tells you nothing about user-facing behavior.

**Reconnaissance before action.** Dynamic web apps render asynchronously. Never assume the DOM is ready — always wait for `networkidle`, then inspect before acting. Taking a screenshot first costs seconds; debugging a flaky selector costs minutes.

**Scripts are black boxes, not reading material.** Helper scripts in `scripts/` exist to handle complex workflows reliably. Run them with `--help` and invoke them directly. Reading their source pollutes your context window and adds no value for the task at hand.

## When to Activate

**Triggers**:
- Verifying a frontend feature works correctly
- Debugging UI behavior or layout issues
- Capturing screenshots for visual review
- Testing user flows (login, form submission, navigation)
- Checking browser console for errors

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

Run scripts with `--help` first. Do not read their source unless a customized solution is absolutely necessary.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices

- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly. 
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Sample Test Structure

A well-structured Playwright test for verifying a login flow:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:3000/login")
    page.wait_for_load_state("networkidle")

    # Reconnaissance: verify form is rendered
    page.screenshot(path="/tmp/login-before.png")

    # Act: fill and submit login form
    page.fill('input[name="email"]', "test@example.com")
    page.fill('input[name="password"]', "password123")
    page.click('button[type="submit"]')

    # Wait for navigation, then verify result
    page.wait_for_url("**/dashboard")
    page.wait_for_load_state("networkidle")
    assert page.locator("h1").inner_text() == "Dashboard"
    page.screenshot(path="/tmp/login-after.png")

    browser.close()
```

Key traits: waits before inspecting, uses user-visible selectors (form fields, button text), asserts user-facing outcomes (page title, URL), captures visual evidence.

## Anti-Patterns

| Anti-Pattern | Why It Fails | Do Instead |
|---|---|---|
| Inspecting DOM before `networkidle` | JS hasn't executed; selectors miss dynamic content | Always `wait_for_load_state("networkidle")` first |
| Testing component internals | Breaks on any refactor, tests nothing the user sees | Test visible outcomes: text, URLs, screenshots |
| Hardcoded `wait_for_timeout(3000)` | Slow when fast, flaky when slow — worst of both worlds | Use `wait_for_selector()`, `wait_for_url()`, or `wait_for_load_state()` |
| Reading helper script source into context | Wastes token budget, scripts are designed as black boxes | Run `--help`, then invoke directly |
| No screenshots on failure | Debugging without visual context is guesswork | Capture screenshot before assertions, always on failure |
| CSS class selectors (`".btn-primary"`) | Break when styling changes, not tied to user intent | Use `role=`, `text=`, `[name=]`, or `[data-testid=]` selectors |
| Skipping server readiness check | Tests run against a half-started server | Use `with_server.py` which waits for port readiness |

## Success Criteria

- [ ] Test waits for page readiness before any DOM inspection
- [ ] Selectors target user-visible attributes (text, role, name), not implementation details
- [ ] Assertions verify user-facing outcomes (displayed text, navigation, visual state)
- [ ] Screenshots captured at key checkpoints for visual verification
- [ ] Server lifecycle managed by helper script (not manual start/stop)
- [ ] No hardcoded sleep/timeout values — use event-based waits
- [ ] Browser closed in all code paths (success and failure)

## Reference Files

- **examples/** - Examples showing common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation