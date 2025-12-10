# Warp Drive Resources for CS146S

This directory contains Warp Drive resources (saved prompts, rules, and MCP integrations) designed to streamline development workflows for the CS146S course repository.

## 📁 Directory Structure

```
.warp/
├── README.md              # This file
├── prompts/               # Saved prompts for common workflows
│   ├── test-runner.md
│   ├── docs-sync.md
│   ├── refactor-harness.md
│   └── release-helper.md
└── mcp/                   # MCP server configurations
    ├── git-mcp-config.json
    └── GIT_MCP_SETUP.md
```

## 🚀 Quick Start

### 1. Install GitHub MCP Server (Required)

The Git MCP server enables autonomous Git operations. Follow the setup guide:

```bash
# View setup instructions
cat .warp/mcp/GIT_MCP_SETUP.md
```

**Key steps:**
1. Get GitHub Personal Access Token
2. Add MCP server in Warp (Settings → AI → MCP Servers)
3. Use the config from `.warp/mcp/git-mcp-config.json`
4. Replace `YOUR_GITHUB_TOKEN_HERE` with your token

### 2. Use Saved Prompts

Saved prompts are reusable workflows. To use them, simply reference them in Warp Agent Mode:

```
Run tests for week4
Sync API docs for week5
Refactor extract to extraction in week4
Prepare release minor for week4
```

## 📝 Available Saved Prompts

### 1. Test Runner (`prompts/test-runner.md`)

**Purpose:** Run tests with coverage analysis, flaky test detection, and actionable feedback.

**Usage:**
```
Run tests for {{week}} {{optional_test_path}}
```

**Examples:**
```
Run tests for week4
Run tests for week5 test_notes.py
Run tests for week4 test_notes.py::test_update_note_success
```

**What it does:**
- ✅ Runs pytest with verbose output
- ✅ Detects flaky tests (re-runs failures)
- ✅ Analyzes coverage (>80% target)
- ✅ Provides specific fix suggestions
- ✅ Identifies missing test coverage

**Output examples:**
- Success: Coverage report with suggestions
- Failure: Exact error + ranked fix suggestions
- Flaky: Identifies intermittent failures

---

### 2. Docs Sync (`prompts/docs-sync.md`)

**Purpose:** Generate/update API documentation from OpenAPI spec and detect route deltas.

**Usage:**
```
Sync API docs for {{week}}
```

**Examples:**
```
Sync API docs for week4
Sync API docs for week5
```

**What it does:**
- 📄 Fetches OpenAPI spec from server
- 🔍 Detects new/changed/removed endpoints
- 📝 Generates comprehensive API.md
- ✅ Validates documentation completeness
- 🎯 Preserves manual sections (auth, rate limits)

**Output:**
- Route delta report (🆕 new, ⚠️ modified, ❌ removed)
- Documentation coverage percentage
- Missing descriptions/examples

**Idempotent:** Safe to run multiple times.

---

### 3. Refactor Harness (`prompts/refactor-harness.md`)

**Purpose:** Safely refactor modules, classes, or functions with automatic import updates.

**Usage:**
```
Refactor {{old_name}} to {{new_name}} in {{week}}
```

**Examples:**
```
Refactor extract to extraction in week4
Refactor ActionItem to Task in week5
Refactor get_db to get_database_session in week4
```

**What it does:**
- 🔍 Shows preview of affected files
- 📦 Creates backup branch automatically
- ✏️ Updates all imports (absolute & relative)
- 🧹 Runs linter and auto-fixes
- ✅ Runs full test suite
- ↩️ Rolls back on failure

**Safety features:**
- Git branch created for changes
- Validates before executing
- Comprehensive test validation
- Automatic rollback on errors

---

### 4. Release Helper (`prompts/release-helper.md`)

**Purpose:** Prepare releases with version bumps, checks, changelog generation, and tagging.

**Usage:**
```
Prepare release {{version_type}} for {{week}}
```

Where `version_type` is: `major`, `minor`, `patch`, or specific like `1.2.3`

**Examples:**
```
Prepare release minor for week4
Prepare release patch for week5
Prepare release 1.0.0 for week4
```

**What it does:**
- ✅ Validates clean working tree
- 🔢 Determines new version number
- 🧪 Runs full test suite + linting + coverage
- 📝 Generates changelog from git commits
- 📦 Updates version in all files
- 🏷️ Creates commit + annotated tag
- 📤 Provides push/publish instructions

**Pre-release checks:**
- All tests pass
- Linting passes
- Coverage ≥80%
- Optional: Type checking

**Changelog:**
- Auto-categorizes commits (feat, fix, refactor, docs, test)
- Preserves existing CHANGELOG.md entries
- Includes commit hashes

**Safety:**
- Never auto-pushes (manual confirmation required)
- Creates backup before changes
- Rollback procedure included

---

## 🔗 Git MCP Server Integration

### What It Enables

The GitHub MCP server allows Warp to autonomously:

- 🌿 Create branches
- 💾 Commit changes with AI-generated messages
- 🔀 Manage pull requests (create, update, merge)
- 🏷️ Create and manage tags
- 📊 Query repo status
- 🔍 Search issues/PRs
- ✅ Check CI/CD status

### Setup

See detailed instructions in: `.warp/mcp/GIT_MCP_SETUP.md`

Quick setup:
1. Generate GitHub Personal Access Token
2. In Warp: Settings → AI → MCP Servers → + Add
3. Paste contents of `.warp/mcp/git-mcp-config.json`
4. Replace token placeholder
5. Start the server

### Usage Examples

**Create feature branch and commit:**
```
Create a new branch called feature/add-pagination, implement pagination for the notes endpoint in week4, and commit the changes
```

**Prepare pull request:**
```
Create a PR for my current branch with a description based on recent commits
```

**Release workflow:**
```
Create a release branch for version 0.2.0, update version files, generate changelog, and create a PR
```

**Review PR status:**
```
What's the status of PR #45? Are there any failing checks?
```

### Integration with Saved Prompts

Combine MCP with prompts for powerful workflows:

- **Test Runner** + MCP → Auto-commit passing tests
- **Docs Sync** + MCP → Auto-commit doc updates
- **Refactor Harness** + MCP → Create refactor branch automatically
- **Release Helper** + MCP → Push releases + create GitHub releases

## 🎯 Workflow Scenarios

### Scenario 1: Implementing a New Feature (TDD)

```
1. Create a new branch called feature/search-notes and add a search endpoint to week4
2. Run tests for week4 test_notes.py::test_search_notes
3. [Fix any failures based on feedback]
4. Run tests for week4
5. Sync API docs for week4
6. Create a PR with description based on recent commits
```

### Scenario 2: Fixing a Bug

```
1. Create branch hotfix/note-update-500-error and fix the null pointer in notes.py line 45
2. Run tests for week4
3. Refactor get_note to get_note_or_404 in week4
4. Run tests for week4
5. Create PR for the hotfix
```

### Scenario 3: Releasing a New Version

```
1. Run tests for week4
2. Sync API docs for week4
3. Prepare release minor for week4
4. [Review changes with: git show v0.2.0]
5. [Push: git push origin main && git push origin v0.2.0]
```

### Scenario 4: Weekly Assignment Workflow

```
1. Start work on week5 assignment: create branch assignment-week5
2. [Implement features]
3. Run tests for week5
4. Sync API docs for week5
5. Create PR with title "Week 5 Assignment Submission"
```

## 💡 Best Practices

### Using Saved Prompts

- ✅ **Start simple:** Use basic commands first
- ✅ **Chain workflows:** Combine multiple prompts sequentially
- ✅ **Review output:** Always review before committing
- ✅ **Customize:** Adapt prompt templates for your needs

### Using Git MCP

- ✅ **Descriptive branches:** Use conventional naming (feature/, fix/, refactor/)
- ✅ **Review before push:** MCP creates local commits first
- ✅ **Verify tests:** Always run tests before pushing
- ✅ **Security:** Never commit tokens, rotate regularly

### General Tips

- 📚 Reference WARP.md for repository context
- 🧪 Run tests frequently during development
- 📝 Keep docs in sync with code changes
- 🏷️ Use semantic versioning for releases
- 🔄 Leverage idempotent workflows (safe to re-run)

## 🛠️ Customization

### Adding New Prompts

1. Create new `.md` file in `.warp/prompts/`
2. Follow existing prompt structure:
   - Title and description
   - Usage syntax
   - What it does (numbered steps)
   - Detailed step-by-step instructions
   - Output format examples
   - Safety guidelines
   - Examples

3. Document in this README

### Modifying Existing Prompts

- Update the `.md` file directly
- Maintain backward compatibility
- Update examples if syntax changes
- Test thoroughly before committing

### Adding More MCP Servers

Consider adding:
- **Linear MCP** (for issue tracking)
- **Sentry MCP** (for error monitoring)
- **Slack MCP** (for notifications)

See `.warp/mcp/GIT_MCP_SETUP.md` for MCP documentation links.

## 📊 Prompt Characteristics

| Prompt | Idempotent | Read-Only | Auto-Commit | MCP Integration |
|--------|-----------|-----------|-------------|-----------------|
| Test Runner | ✅ | ✅ | ❌ | Optional |
| Docs Sync | ✅ | ❌ | ❌ | Optional |
| Refactor Harness | ❌ | ❌ | ❌ | Recommended |
| Release Helper | ❌ | ❌ | ❌ | Recommended |

- **Idempotent:** Safe to run multiple times with same result
- **Read-Only:** Doesn't modify files (only runs commands)
- **Auto-Commit:** Automatically creates git commits
- **MCP Integration:** Benefits from Git MCP server

## 🔒 Security Notes

### GitHub Token Security

- ⚠️ **Never commit tokens** to the repository
- ⚠️ Token file (`.warp/mcp/git-mcp-config.json`) should be gitignored if it contains real token
- ⚠️ Use environment variables for production
- ⚠️ Rotate tokens every 90 days

### Safe Usage

- ✅ All prompts validate before making changes
- ✅ Prompts create backups (branches, stashes)
- ✅ Rollback procedures documented
- ✅ No automatic force-pushes

## 🐛 Troubleshooting

### Prompt Not Working

1. Check syntax matches examples exactly
2. Verify you're in the correct directory
3. Ensure required tools installed (pytest, docker, etc.)
4. Review WARP.md for repo-specific context

### MCP Server Issues

1. Check Docker is running: `docker ps`
2. Verify token permissions
3. View logs: `cd ~/Library/Application\ Support/dev.warp.Warp-Stable/mcp && tail -f github.log`
4. Restart server in Warp UI

### Tests Failing

1. Run `make test` directly to see full output
2. Check PYTHONPATH is set correctly
3. Verify conda environment is activated
4. Review test-specific errors in prompt output

## 📚 Additional Resources

- **WARP.md**: Repository-specific guidance for Warp
- **CLAUDE.md**: Additional context for Claude Code agents
- **Root README.md**: Setup and environment configuration
- **Week-specific READMEs**: Assignment details

## 🤝 Contributing

To improve these Warp Drive resources:

1. Test changes thoroughly in your environment
2. Update documentation in this README
3. Add examples for new workflows
4. Follow existing prompt structure conventions
5. Document any new dependencies or prerequisites

## 📝 Version History

- **v1.0** (2025-01-27): Initial release
  - 4 saved prompts (test-runner, docs-sync, refactor-harness, release-helper)
  - Git MCP server integration
  - Comprehensive documentation

---

**Questions?** Check the individual prompt files for detailed step-by-step instructions, or refer to the [Warp Documentation](https://docs.warp.dev/).
