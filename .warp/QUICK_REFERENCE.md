# Warp Drive Quick Reference Card

## 🚀 Setup (One-Time)

```bash
# 1. View the main README
cat .warp/README.md

# 2. Set up GitHub MCP (required)
cat .warp/mcp/GIT_MCP_SETUP.md
# → Get GitHub token → Add to Warp MCP servers
```

## 📝 Saved Prompts (Copy & Paste)

### Test Runner
```
Run tests for week4
Run tests for week5 test_notes.py
Run tests for week4 test_notes.py::test_create_note
```

### Docs Sync
```
Sync API docs for week4
Sync API docs for week5
```

### Refactor Harness
```
Refactor extract to extraction in week4
Refactor ActionItem to Task in week5
Refactor get_db to get_database_session in week4
```

### Release Helper
```
Prepare release minor for week4
Prepare release patch for week5
Prepare release 1.0.0 for week4
```

## 🔗 MCP Server Commands

### Git Operations
```
Create a new branch called feature/add-pagination and implement it in week4

Create a PR for my current branch with description based on recent commits

What's the status of PR #45?

Fix the linting errors and commit the changes
```

## 🎯 Common Workflows

### TDD Feature Development
```
1. Create branch feature/search-notes and implement search in week4
2. Run tests for week4
3. Sync API docs for week4
4. Create PR with description
```

### Bug Fix
```
1. Create branch hotfix/note-500-error and fix notes.py line 45
2. Run tests for week4
3. Create PR for hotfix
```

### Release
```
1. Run tests for week4
2. Sync API docs for week4
3. Prepare release minor for week4
4. [Review then push]
```

## 📚 Documentation

- **Full Guide:** `.warp/README.md`
- **Repo Rules:** `WARP.md`
- **Implementation:** `WARP_DRIVE_IMPLEMENTATION.md`
- **MCP Setup:** `.warp/mcp/GIT_MCP_SETUP.md`

## 🔒 Security

- Never commit tokens
- Use `.warp/mcp/git-mcp-config.json` as template only
- Store actual token separately
- Rotate tokens every 90 days

## ⚡ Pro Tips

- Chain prompts sequentially for workflows
- Use MCP for autonomous Git operations
- All prompts validate before executing
- Prompts are idempotent where possible
- Review changes before pushing

## 🐛 Troubleshooting

**Prompt not working?**
- Check syntax matches examples
- Verify correct directory
- Review WARP.md for context

**MCP issues?**
- Check Docker: `docker ps`
- View logs: `cd ~/Library/Application\ Support/dev.warp.Warp-Stable/mcp && tail -f github.log`
- Restart server in Warp UI

**Tests failing?**
- Run `make test` directly
- Check PYTHONPATH
- Activate conda environment

---

**Need help?** Check `.warp/README.md` for detailed documentation.
