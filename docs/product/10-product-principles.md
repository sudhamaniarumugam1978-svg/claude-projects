# 10 — Product Principles

These principles are the constitution of StockSense. They are not aspirations; they are
constraints. Every feature, model, screen, and message is measured against them. When a
trade-off arises, these principles decide it. They are enforced concretely in the
[Agent Architecture](../architecture/13-agent-architecture.md) and recorded as
[ADR-0001](../architecture/adr/0001-decision-intelligence-not-dashboards.md).

---

## The Always / Never Charter

### Always

1. **Always explain recommendations.** Every recommendation states *why* in plain language.
2. **Always show a confidence score.** The user always knows how much to trust an output.
3. **Always prioritize business impact.** Output is ranked by dollars at stake, not volume.
4. **Always provide actionable insights.** Every insight resolves to a concrete next step.
5. **Always keep the human in control.** The human approves, modifies, or rejects.
6. **Always ground outputs in the retailer's real data.** No generic, ungrounded advice.
7. **Always be proactive.** Surface problems before they occur, not after.
8. **Always make outputs traceable.** Any conclusion can be followed back to its evidence.

### Never

1. **Never recommend without evidence.** No supporting data, no recommendation.
2. **Never generate unexplained AI outputs.** No black boxes.
3. **Never overwhelm with unnecessary dashboards or charts.** Insight beats raw data.
4. **Never project false confidence.** Uncertainty is communicated honestly.
5. **Never make the final business decision for the user by default.** Augment, don't replace.
6. **Never bury the signal.** Noise (low-impact, low-confidence noise) is suppressed.
7. **Never require a data science team to get value.** Expertise is delivered, not demanded.

---

## The Product Philosophy, Expanded

### Principle I — Decisions are the product; data is the raw material
Traditional software's deliverable is *information*. Ours is a *decision*. A screen that
shows a number but does not help the user decide has failed our standard, no matter how
elegant. This is the core of [ADR-0001](../architecture/adr/0001-decision-intelligence-not-dashboards.md).

### Principle II — Prediction over reporting
The past is only useful insofar as it predicts the future. We invest our effort in "what
will happen," and we treat historical reporting as supporting evidence for a forecast, not
as an end in itself.

### Principle III — Explanation is a first-class feature, not an afterthought
The explanation is shipped, tested, and designed with the same rigor as the prediction it
justifies. A recommendation and its rationale are a single, inseparable unit. This is why
the [Recommendation Agent](../agents/agent-catalog.md) is contractually forbidden from
emitting a recommendation without reasoning, confidence, supporting data, and impact.

### Principle IV — Impact is the universal sort order
When everything competes for a busy user's attention, business impact is the tiebreaker.
The most expensive problem, the biggest opportunity, comes first. "Interesting but
low-impact" ranks below "urgent and costly."

### Principle V — Confidence is a promise, and it must be kept
A confidence score is a commitment about reliability. We calibrate it, monitor it, and
treat miscalibration as a defect. Honest uncertainty earns more trust than confident error.

### Principle VI — The human is the decision-maker, always
We are a decision *support* system. The retailer's authority over their own business is
sacred. The system's job is to make the human faster, better informed, and more
consistent — never to remove them. This is codified in the [AI Philosophy](12-ai-philosophy.md).

### Principle VII — Signal over noise
Every alert competes against the user's trust. One false alarm costs more credibility than
ten correct alerts earn. We are ruthless about suppressing low-value output; an unopened
notification is a failure.

### Principle VIII — Work on top of what the retailer already has
We are a layer, not a replacement. Respecting the retailer's existing systems of record
lowers adoption friction to near zero and keeps our scope disciplined
([Product Scope](06-product-scope.md)).

### Principle IX — Accessible sophistication
Advanced capability must arrive in a form a non-expert can use. If a feature requires
training a user to think like a data scientist, we have shipped the wrong feature.

### Principle X — Earn trust incrementally, keep it permanently
Adoption is a trust curve. We start by being transparently useful on small, verifiable
decisions, and we expand the user's reliance on us only as fast as we earn it. We never
trade long-term trust for a short-term "wow."

---

## Applying the Principles: A Worked Example

> **Situation:** SKU #4471 (a fast-moving beverage) will run out in 3 days; the next
> delivery is in 5 days.

| Principle | How it shapes the output |
| --- | --- |
| Prediction over reporting | We surface it *now*, based on a forecast — not after it stocks out |
| Always explain | "Weekend demand is 3× weekday; your delivery arrives after the weekend." |
| Always show confidence | "Confidence: 84% (based on 12 weeks of consistent weekend spikes)." |
| Always actionable | "Recommended: expedite 120 units, or place a 2-day bridge order of 60 units." |
| Impact is the sort order | Ranked #1 today because est. revenue at risk is the highest on the list |
| Human in control | Manager taps Approve, Modify quantity, or Reject |
| Signal over noise | A low-impact slow-mover with the same math is *not* alerted today |

---

## Governance

- These principles are versioned with the product blueprint.
- Any proposed exception must be recorded as an ADR with explicit rationale and trade-offs
  (see [ADR Index](../architecture/adr/README.md)).
- Conflicts between principles are resolved in favor of **trust** (explanation, honesty,
  human control) over **cleverness** (accuracy, automation, breadth).
