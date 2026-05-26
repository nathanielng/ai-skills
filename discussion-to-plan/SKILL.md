# discussion-to-plan

Transform a discussion/conversation thread into a comprehensive structured plan document.

## Usage

```bash
/discussion-to-plan
```

When invoked, this skill:
1. Analyzes the conversation history up to this point
2. Extracts key decisions, design choices, and technical details
3. Structures them into a comprehensive plan.md with:
   - **Overview** — what we're building
   - **Design Decisions & Tradeoffs** — why we chose X over Y
   - **Architecture** — system structure and components
   - **Data Schemas** — JSON/data models
   - **Phases** — breakdown of work
   - **Rationale & Benefits** — why this approach
   - **Implementation Notes** — gotchas, extensibility points
   - **Future Considerations** — what comes next

The output is saved as `plan.md` in the current directory.

## Example Output

See `template.md` for the structure and organization approach.

## Tips

- Invoke early to lock in decisions before implementation
- Use as a reference during development to stay aligned
- Update if architecture changes significantly
