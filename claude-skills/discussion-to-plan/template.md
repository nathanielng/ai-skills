# Plan Template: Discussion → Structured Document

Use this template when converting a discussion/decision thread into a formal plan.

---

## Overview

**What are we building?**
- Clear statement of purpose
- Key constraints/requirements
- High-level goals

---

## Design Decisions & Tradeoffs

### Decision 1: [Topic]
- **Choice**: What we decided
- **Why**: Rationale
- **Tradeoff**: What we gave up / downside
- **Alternatives considered**: Other options and why they didn't win

### Decision 2: [Topic]
- ...

---

## Architecture

### System Structure
```
Brief ASCII diagram or description of how components fit together
```

### Component Overview
- **Component A**: What it does, responsibilities
- **Component B**: What it does, responsibilities
- ...

### Data Flow
- How data moves through the system
- Key interfaces/contracts

---

## Data Schemas

### Core Objects

#### [ObjectType] Schema
```json
{
  "id": "string (unique identifier)",
  "type": "string (object type)",
  "property": "example value",
  "...": "..."
}
```

**Rationale**: Why this structure
**Extensibility**: How to add fields/types over time

---

## Implementation Phases

### Phase 1: [Name]
**Goal**: What gets shipped
**Components**:
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

**Outcomes**: What you can do after Phase 1

---

### Phase 2: [Name]
**Goal**: What gets shipped
**Components**:
- [ ] Task 1
- [ ] Task 2

**Outcomes**: What's new

---

## Rationale & Benefits

- **Benefit 1**: Why this approach is good
- **Benefit 2**: How it enables future work
- **Design principle**: What philosophy guides decisions

---

## Implementation Notes

### Extensibility Strategy
- How to add new features without breaking existing code
- What's designed to be extensible vs. fixed

### Potential Gotchas
- Edge cases to watch for
- Performance considerations
- Concurrency issues (if any)

### File/Directory Structure
```
project/
├── component-a/
├── component-b/
└── shared/
```

---

## Future Considerations

- What comes after the phases?
- What's deliberately left out for now?
- Migration paths (data, schema, storage)
