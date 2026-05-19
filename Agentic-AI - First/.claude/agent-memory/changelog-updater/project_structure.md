---
name: project-structure
description: Root directory, agent location, and changelog conventions for the Agentic-AI First project
metadata:
  type: project
---

Root directory is `/Users/kapilkumar/Git/Agentic-AI - First`. CHANGE.md lives at the root level.

The changelog agent definition is at `.claude/agents/changelog-updater.md` (renamed from `commit-changelog-writer.md` in commit 9c4a781).

**Why:** The project uses date-based single-line changelog entries (not semantic versioning sections). Format is `[YYYY-MM-DD] <one-line summary> [<short-hash>]`.

**How to apply:** Always write one line per commit in CHANGE.md. Do not use multi-section (Added/Changed/Fixed) format — the agent spec explicitly uses flat single-line entries.
