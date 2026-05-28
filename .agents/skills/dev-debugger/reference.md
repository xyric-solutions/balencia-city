# DEV-03 Reference: Deep Expertise

Loaded on demand for detailed patterns, examples, and guidance.

---

## Common Debugging Scenarios

### Null/Undefined Errors
- Check the call chain: which step returns null?
- Verify API responses match expected shape
- Check optional chaining usage

### Async/Promise Issues
- Verify await is used on async calls
- Check for unhandled promise rejections
- Look for race conditions in parallel operations

### Type Errors
- Compare expected vs actual types at each step
- Check TypeScript strict mode settings
- Verify JSON parsing of API responses

### Performance Issues
- Profile with browser devtools or Node profiler
- Check for N+1 query patterns
- Look for unnecessary re-renders in React

## Escalation Template

When escalating, provide:

```
Goal: [What I'm trying to accomplish]
Error: [Full error message]
Environment: [OS, Node version, etc.]
Steps to reproduce: [1, 2, 3...]
What I've tried: [Approaches attempted]
Minimal code: [Smallest code that reproduces]
```
