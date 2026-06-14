# create-guide Skill

Transform conversation learnings into comprehensive, actionable guides with quick-start, workflows, troubleshooting, pitfalls, and verification steps.

## Quick Start

```bash
# Generate example HyperFrames guide
cd ~/.claude/skills/create-guide
python3 create-guide.py --example --output hyperframes-setup.md

# View the guide
open hyperframes-setup.md
```

## What's Included

- **Quick Start** — 5-minute essential steps, prerequisites, time estimates
- **Step-by-Step Workflow** — Each phase with what/why/checklist/verification
- **Troubleshooting** — Problem → Cause → Solution table
- **Pitfalls** — Common mistakes and fixes (prevent learning from failure)
- **Verification** — Checklists at each phase (confirm you're on track)

## Use Cases

1. **Session learnings** — Extract insights from long conversations into guides
2. **Runbooks** — Create repeatable workflows for common tasks
3. **Onboarding** — Help new team members learn your process
4. **Personal reference** — Build your own playbooks
5. **Documentation** — Professional guides with all the context

## Files

- `create-guide.py` — Main guide generator (Python)
- `SKILL.md` — Skill documentation with API reference
- `examples/` — Example guides (HyperFrames, etc.)

## Integration

Use with other Claude Code skills:
- **`/save-learnings`** — Save individual learnings, then aggregate into guides
- **`/pageindex`** — Query learnings with natural language
- **`/graphify`** — Extract key concepts from documentation
- **Claude Code** — Create guides for projects (`SETUP_GUIDE.md`, `RUNBOOK.md`)

## Python API

```python
from create_guide import GuideGenerator

guide = GuideGenerator(topic="Your Workflow", description="Description")

# Add sections
guide.add_quick_start(steps=[...], prerequisites="...", time_estimate="5 min")
guide.add_workflow_step(1, "Step Name", "Description", [...], [...])
guide.add_troubleshooting("Problem", "Cause", "Solution")
guide.add_pitfall("Title", "Description", "Why", "Fix")
guide.add_verification_item("Phase", ["item1", "item2"])

# Save
guide.save("my-guide.md")
```

## Example Workflow

```
Conversation → Extract Learnings → Save to /save-learnings
   ↓
Query with /pageindex → Consolidate Key Insights
   ↓
Create Guide → Structured, Searchable, Professional
```

## Status

✅ **Ready to use**
- [x] Guide generation framework
- [x] Example HyperFrames guide
- [x] Python API documented
- [x] Troubleshooting templates
- [x] Verification checklists

---

**Last Updated:** 2026-05-24
**Version:** 1.0
