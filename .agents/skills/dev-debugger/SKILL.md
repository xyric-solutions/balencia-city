---
skill_id: "DEV-03"
name: "Debugger Assistant"
version: "v2.0"
category: "development"
description: "Systematic debugging using the DEBUG framework, transforming chaotic troubleshooting into structured problem-solving."
---

# DEV-03: Debugger Assistant

## Purpose

Systematic debugging using the DEBUG framework. Transform chaotic troubleshooting into structured problem-solving.

## When to Activate

**Triggers**:
- "Help me debug this error"
- "Why isn't this working?"
- "I'm getting [error message]"
- Unexpected behavior or performance issues

## The DEBUG Framework

| Step | Focus | Key Questions |
|------|-------|---------------|
| **D**escribe | What's happening? | Exact error, expected vs actual, consistent or intermittent? |
| **E**nvironment | Where? | OS, versions, dev vs prod, recent changes? |
| **B**reakpoint | Isolate | Last working state, minimum reproduction, what triggers it? |
| **U**nderstand | Why? | Read error carefully, trace code flow, check logs |
| **G**enerate | Solutions | Hypotheses ranked by likelihood, test one at a time |

## Debugging Process

### Phase 1: Gather Information
- Get exact error message (full text)
- Document steps to reproduce
- Check recent code changes (`git diff`)
- Review relevant logs

### Phase 2: Isolate
- Create minimal reproduction
- Remove variables one by one
- Test in different environments

### Phase 3: Root Cause
- Trace code execution path
- Add logging at decision points
- Check variable states at each step

### Phase 4: Fix & Verify
- Make ONE change at a time
- Test the specific scenario
- Verify no regression
- Document the fix

## Xyric Rules

1. **Fix root cause, not symptoms** - understand WHY before fixing
2. **One change at a time** - avoid shotgun debugging
3. **Read the full error** - error messages contain answers
4. **Test to reproduce first** - write a failing test before fixing (DEV-02)
5. **Document the fix** - help future debugging

## Integration

| Skill | Integration |
|-------|-------------|
| DEV-01 | Review findings inform debug priorities |
| DEV-02 | Write test to reproduce, ensure fix persists |

## Anti-Patterns

- **Shotgun debugging**: Random changes hoping something works
- **Debugging by coincidence**: "It works now, not sure why"
- **Print overload**: `console.log(1); console.log(2);` with no labels
- **Ignoring errors**: "Some error about types or something"

## When to Escalate

Ask for help when:
- Spent > 30 minutes without progress
- Need domain knowledge you lack
- Blocked on external dependency

Include: goal, attempts made, environment, minimal code, full error.
