# create-guide

Generate comprehensive guides from conversation context, extracting workflows, pitfalls, troubleshooting, and verification steps into structured markdown.

## Usage

```bash
# Generate example HyperFrames guide
python3 create-guide.py --example --output my-guide.md

# Create custom guide programmatically
python3 create-guide.py --custom --topic "My Topic"
```

## What It Does

The `create-guide` skill transforms unstructured conversation learnings into professional guides with these sections:

1. **Quick Start** — Time estimate, prerequisites, essential steps (5 minutes to production)
2. **Step-by-Step Workflow** — Each major phase with:
   - What you're doing (context)
   - Critical checklist (must-haves)
   - Verification steps (how to confirm success)
3. **Troubleshooting** — Problem → Cause → Solution table
4. **Pitfalls to Avoid** — Common mistakes and how to fix them
5. **Verification Checklist** — Per-phase confirmation at key milestones

## Python API

### Create a Guide Programmatically

```python
from create_guide import GuideGenerator

# Initialize
guide = GuideGenerator(
    topic="My Amazing Workflow",
    description="Complete guide to doing X"
)

# Add quick start
guide.add_quick_start(
    steps=[
        "Step 1",
        "Step 2",
        "Step 3",
    ],
    prerequisites="Node.js, ffmpeg",
    time_estimate="5 minutes"
)

# Add workflow steps
guide.add_workflow_step(
    step_number=1,
    name="Setup",
    description="What you're doing here",
    checklist=[
        "Checklist item 1",
        "Checklist item 2",
    ],
    verification=[
        "Verification step 1",
        "Verification step 2",
    ]
)

# Add troubleshooting
guide.add_troubleshooting(
    problem="Something doesn't work",
    cause="Because of this",
    solution="Do this to fix it"
)

# Add pitfalls
guide.add_pitfall(
    title="Common Mistake",
    description="This happens when...",
    why="Because...",
    fix="To fix: ..."
)

# Add verification items
guide.add_verification_item(
    phase="After Step 1",
    items=[
        "Check this",
        "Verify that",
    ]
)

# Generate and save
guide.save("my-guide.md")
```

## When to Use

- **Extracting learnings from long sessions** — Consolidate conversation into structured guide
- **Creating runbooks** — For workflows you do repeatedly
- **Onboarding documentation** — Help others learn the workflow
- **Personal reference** — Create personal playbooks with your own learnings
- **Building institutional knowledge** — Save hard-won lessons from each project

## Examples

### HyperFrames Setup
```bash
python3 create-guide.py --example --output hyperframes-guide.md
```

This generates a complete guide including:
- Quick start (scaffolding, preview, rendering)
- 6 workflow steps (composition → audio → validation → integration → testing → rendering)
- Troubleshooting table (audio issues, rendering issues, etc.)
- 4 major pitfalls (silent audio, path mismatches, duration mismatches, process management)
- Verification checklists for each phase

## Output Format

Guides are generated as markdown with these features:
- ✅ Verification checkmarks at key steps
- ❌ Pitfall warnings highlighted
- 📋 Searchable tables for troubleshooting
- [ ] Checkbox lists for verification items
- **Bold emphasis** on critical points

## Integration with Other Skills

- **Learnings:** Guides often extract from `/save-learnings`
- **Pageindex:** Query saved learnings with `/pageindex` to inform guide creation
- **Graphify:** Use `/graphify` to extract key concepts from documentation
- **Claude Code:** Use this in project workflows to create `SETUP_GUIDE.md` and `RUNBOOK.md`

## File Structure

```
create-guide/
├── create-guide.py        # Main guide generator
├── SKILL.md              # This file
└── examples/
    └── hyperframes-guide.md  # Example output
```

## Why This Matters

**Traditional documentation problems:**
- Scattered across conversations and notes
- Missing troubleshooting (only happy path documented)
- No pitfall warnings (you learn by failing)
- Verification steps unclear (how do you know it worked?)

**Structured guides solve this:**
- Everything in one place
- Problems + solutions included
- Pitfalls prevent others from your mistakes
- Verification steps = confidence at each phase

---

**Created:** 2026-05-24
**Based on:** HyperFrames animation workflow session
**Use Case:** Consolidating conversation learnings into actionable guides
