# AI Skills Repository

## Git Security: PII & Sensitive Data Check

**⚠️ BEFORE EVERY `git commit` AND `git push`:**

Always scan for sensitive data using:
```bash
git diff --cached      # Review what's being committed
git log -p -S"password" --all  # Search history for passwords
git log -p -S"key" --all        # Search history for keys
git log -p -S"credential" --all # Search for credentials
```

**Never commit:**
- API keys, tokens, credentials
- `.env` files (use `.env.example` instead)
- `secrets.json`, `credentials.yaml`
- AWS/GCP/Azure credentials
- Personal info (emails, phone numbers, SSN)
- Private URLs or endpoints
- Auth tokens, JWT secrets
- Database connection strings with passwords

**If you find sensitive data:**
```bash
git restore --staged filename    # Remove from staging
# Edit .gitignore to prevent future commits
git rm --cached filename         # Remove from repo history (if already committed)
# Then recommit after fixing
```

## Repository Structure

- `create-guide/` — Skill for generating structured guides from conversations
  - `create-guide.py` — Main guide generator (Python API)
  - `SKILL.md` — Full documentation
  - `README.md` — Quick reference
  - `example-hyperframes-guide.md` — Example output

- `claude-skills/` — Other skills and utilities

## Contributing Skills

When adding new skills:
1. Create a folder: `skill-name/`
2. Include: `SKILL.md`, `README.md`, and implementation files
3. Add .gitignore entry if skill creates local cache/output files
4. Document usage and examples
5. **SECURITY CHECK**: Run `git diff --cached` before committing

## Skills

### create-guide
Transform conversation learnings into professional guides with:
- Quick start
- Step-by-step workflow
- Troubleshooting
- Pitfalls to avoid
- Verification checklists

Usage:
```bash
python3 create-guide/create-guide.py --example --output my-guide.md
```

See `create-guide/SKILL.md` for full API reference.

---

**Repository:** https://github.com/nathanielng/ai-skills
**Last Updated:** 2026-05-25
