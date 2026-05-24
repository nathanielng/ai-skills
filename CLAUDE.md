# AI Skills Repository

## Git Security: Automated Secret Scanning

**Automated pre-commit hooks enabled** — secret detection runs automatically before every commit via `gitleaks` + `pre-commit-hooks`:

```bash
git commit               # Hooks run automatically, scanning for:
                        # - Hardcoded secrets (API keys, tokens, credentials)
                        # - Private SSH keys
                        # - Passwords and auth tokens
                        # - Config files with secrets
```

**What's protected:**
- API keys, tokens, credentials
- AWS/GCP/Azure credentials
- `.env` files and `secrets.json`
- Personal info (emails, phone numbers, SSN)
- Auth tokens, JWT secrets
- Database connection strings with passwords

**If secrets are detected:**
```bash
# The commit will be blocked and you'll see the detected secrets
# Option 1: Remove the file from staging
git restore --staged filename

# Option 2: Delete the secret content, then stage again
# Edit filename to remove the secret, then:
git add filename
git commit

# Option 3: Permanently remove from git history (if already committed)
git rm --cached filename  # Remove the file
git commit --amend        # Amend the commit
```

**Manual review still recommended:**
```bash
git diff --cached        # Review what you're about to commit
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
