# CORE-01: Placeholder Guardian

**Skill ID**: CORE-01
**Category**: Core Infrastructure
**Priority**: 🔴 Critical
**Version**: 1.0
**Last Updated**: 2025-11-30

---

## Purpose

Ensures Claude **NEVER** invents implementation times, revenue projections, or cost estimates without explicit human input. This is the most critical skill for maintaining trust and accuracy in business documentation.

---

## When to Activate

**Automatic Triggers**:
- Creating financial projections
- Writing roadmaps with milestones
- Estimating development timelines
- Discussing budgets or costs
- Creating business plans
- Any document involving time/money estimates

**Manual Invocation**:
```
"Use placeholder guardian - don't invent any estimates"
"I need human input placeholders for all time and cost data"
```

---

## Forbidden Patterns

Claude must **NEVER** write:

### Time Estimates
- ❌ "This will take approximately 2 weeks"
- ❌ "Development timeline: 3-4 months"
- ❌ "Expected delivery by Q2 2026"
- ❌ "Implementation estimated at 160 hours"

### Revenue Claims
- ❌ "Expected revenue of $50K in Month 6"
- ❌ "Projected MRR of $10,000"
- ❌ "Revenue forecast: $500K annually"
- ❌ "Breakeven expected by Month 12"

### Cost Estimates
- ❌ "Development cost estimated at $30K"
- ❌ "Budget requirement: $100,000"
- ❌ "Infrastructure costs: $500/month"
- ❌ "Hiring costs approximately $60K per developer"

### Vague Estimates
- ❌ "Roughly 2-3 weeks"
- ❌ "Around $20K-30K"
- ❌ "Approximately 6 months"
- ❌ "Probably by end of year"

---

## Required Pattern

**ALWAYS** use placeholders requiring human input:

### Time Placeholders
```markdown
**Timeline**: [HUMAN INPUT REQUIRED - Estimated duration based on team capacity]
**Milestone Date**: [HUMAN INPUT REQUIRED - Target date considering dependencies]
**Sprint Duration**: [HUMAN INPUT REQUIRED - Based on team velocity]
```

### Revenue Placeholders
```markdown
**Month 6 Revenue**: [HUMAN INPUT REQUIRED - Target based on sales pipeline]
**MRR Target**: [HUMAN INPUT REQUIRED - Based on customer acquisition goals]
**Annual Revenue**: [HUMAN INPUT REQUIRED - Based on growth assumptions]
```

### Cost Placeholders
```markdown
**Development Budget**: [HUMAN INPUT REQUIRED - Cost breakdown by role/phase]
**Infrastructure Cost**: [HUMAN INPUT REQUIRED - Based on actual usage projections]
**Total Budget**: [HUMAN INPUT REQUIRED - Approved budget from finance]
```

---

## Verification Workflow

### Step 1: Detection
Before writing ANY content, scan for time/revenue/cost patterns:
```
Keywords to flag:
- "will take", "estimated", "approximately", "roughly"
- "$", "revenue", "cost", "budget", "expense"
- "weeks", "months", "years", "hours", "days"
- "timeline", "deadline", "due date", "delivery"
```

### Step 2: Pause and Ask
When estimate is needed, STOP and ask user:
```
"I need to include [timeline/cost/revenue] information here.
Do you have estimates for:
- [Specific metric 1]
- [Specific metric 2]

Please provide your estimates with the reasoning behind them."
```

### Step 3: Document User Input
When user provides estimate:
```markdown
**User-Provided Estimate** (2025-11-30):
- Metric: Month 6 Revenue
- Value: $5,000/month
- Rationale: Based on 2 confirmed client engagements at $2,500/month each
- Confidence: Medium (pending contract signatures)
```

### Step 4: Preserve Placeholders
If user doesn't have estimate:
```markdown
**[HUMAN INPUT REQUIRED]**
- Metric needed: Month 6 Revenue Target
- Why needed: Required for breakeven calculation
- Suggested approach: Review sales pipeline, count warm leads
- Decision deadline: [HUMAN INPUT REQUIRED]
```

---

## Examples

### ❌ WRONG - Claude Inventing

```markdown
## yHealth MVP Roadmap

### Phase 1: Foundation (January 2026)
Development will take approximately 8 weeks with an estimated budget of $40,000.
Expected to generate $5,000 MRR by Month 3.

### Phase 2: Launch (March 2026)
Full launch estimated for March 2026, with projected revenue of $20,000/month
by Q4 2026 based on market analysis.
```

### ✅ CORRECT - Placeholder Pattern

```markdown
## yHealth MVP Roadmap

### Phase 1: Foundation
**Start Date**: [HUMAN INPUT REQUIRED - Dependent on design completion]
**Duration**: [HUMAN INPUT REQUIRED - Based on Salman's availability and scope]
**Budget**: [HUMAN INPUT REQUIRED - Development cost breakdown needed]

To provide estimates, please consider:
- Current yHealth design completion: 64%
- Team capacity: Salman available [X]% for yHealth
- Parallel work on other products

### Phase 2: Launch
**Target Date**: [HUMAN INPUT REQUIRED - After Phase 1 completion + buffer]
**Revenue Target**: [HUMAN INPUT REQUIRED - Based on launch strategy]

**Questions to answer**:
1. What's the realistic launch window?
2. How many users/clients targeted at launch?
3. What's the pricing model?
```

---

## Protected Values

**ALWAYS** require human input for:

| Category | Specific Items |
|----------|----------------|
| **Time** | Development duration, milestone dates, delivery dates, sprint velocity |
| **Revenue** | Monthly targets, MRR, ARR, revenue growth rates, conversion rates |
| **Costs** | Development costs, infrastructure, salaries, marketing spend |
| **Projections** | Breakeven point, profitability date, ROI calculations |
| **Headcount** | Hiring timeline, team growth, resource allocation |
| **Market** | Market size (unless from cited research), growth rates |

---

## Integration with Other Skills

### With DOC-01 (Documentation Validator)
- Validator flags documents containing invented estimates
- Completeness check requires all placeholders filled

### With FIN-01 (Financial Propagator)
- Financial changes propagate with user confirmation
- Never auto-fill financial data

### With DEV-02 (Test Generator)
- Time estimates for testing require human input
- Never assume test duration

---

## Anti-Patterns to Avoid

❌ **Don't** use hedging language to sneak in estimates:
- "Roughly speaking, this might take around 2 weeks"
- "A reasonable estimate would be $30K"

❌ **Don't** reference "industry standards" as estimates:
- "Industry standard is 3-6 months for MVP"
- "Typical SaaS CAC is $500"

❌ **Don't** use ranges as cover for guessing:
- "Timeline: 2-4 months" (still inventing)
- "Budget: $20K-50K" (still inventing)

❌ **Don't** extrapolate from partial data:
- "Based on Phase 1, Phase 2 will take 6 weeks"
- "Given current revenue, we'll hit $100K by December"

---

## Best Practices

✅ **Do** ask clarifying questions before creating financial content
✅ **Do** document the source of every number
✅ **Do** use `[HUMAN INPUT REQUIRED]` consistently
✅ **Do** explain WHY an estimate is needed
✅ **Do** suggest what information would help provide the estimate
✅ **Do** timestamp all user-provided estimates
✅ **Do** note confidence levels for estimates

---

## Validation Checklist

Before finalizing any document:

- [ ] No time estimates without user confirmation
- [ ] No revenue projections without user data
- [ ] No cost estimates without user input
- [ ] All placeholders clearly marked
- [ ] User-provided estimates have dates and rationale
- [ ] No hedging language hiding guesses

---

## Success Criteria

✅ Zero invented estimates in any document
✅ All financial data traceable to user input
✅ Placeholders clearly visible and actionable
✅ Users provide estimates within context
✅ Documents remain accurate and trustworthy

---

## Troubleshooting

**Issue**: Claude still inventing estimates despite skill
**Solution**: Explicitly invoke: "Stop - use placeholder guardian. I need human input for all estimates."

**Issue**: Too many placeholders making document unreadable
**Solution**: Group related placeholders into a "Required Inputs" section at the end

**Issue**: User doesn't know what estimate to provide
**Solution**: Ask clarifying questions, provide frameworks for thinking through estimates

---

*Skill CORE-01 v1.0 | Xyric Solutions | 2025-11-30*









