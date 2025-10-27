# Git MCP Server Setup

This MCP server integration enables Warp to interact with Git and GitHub autonomously, allowing for automated branch creation, commits, PR management, and more.

## What This Enables

With the Git MCP server, Warp can:

- 🌿 **Create branches** automatically based on context
- 💾 **Commit changes** with generated commit messages
- 🔀 **Manage pull requests** (create, update, merge)
- 🏷️ **Create and manage tags** for releases
- 📊 **Query repository status** (files changed, branch info)
- 🔍 **Search issues and PRs** for context
- 📝 **Generate PR descriptions** from commit history
- ✅ **Check CI/CD status** before merging

## Prerequisites

- Docker installed and running
- GitHub Personal Access Token (PAT) with appropriate permissions

## Setup Instructions

### 1. Create GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Name: `warp-mcp-server`
4. Select scopes:
   - ✓ `repo` (Full control of private repositories)
   - ✓ `workflow` (Update GitHub Action workflows)
   - ✓ `read:org` (Read org and team membership)
   - ✓ `user:email` (Access user email addresses)
5. Generate token and copy it (you won't see it again!)

### 2. Install the MCP Server in Warp

#### Option A: Via Warp UI

1. Open Warp
2. Open Command Palette (Cmd+P) → "Open MCP Servers"
3. Click "+ Add"
4. Paste the contents of `git-mcp-config.json`
5. Replace `YOUR_GITHUB_TOKEN_HERE` with your actual token
6. Click "Save"
7. Start the GitHub MCP server

#### Option B: Via Manual Configuration

1. Copy `git-mcp-config.json` contents
2. Replace `YOUR_GITHUB_TOKEN_HERE` with your token
3. In Warp: Settings → AI → Manage MCP servers → + Add
4. Paste the JSON configuration
5. Save and start the server

### 3. Verify Installation

In Warp Agent Mode, ask:
```
List available MCP tools
```

You should see GitHub tools like:
- `github_create_branch`
- `github_create_pull_request`
- `github_list_issues`
- `github_get_file_contents`
- `github_push_files`
- etc.

## Usage Examples

### Example 1: Create Feature Branch and Commit

```
Create a new branch called feature/add-pagination, implement pagination for the notes endpoint in week4, and commit the changes
```

Warp will:
1. Create branch `feature/add-pagination`
2. Make code changes
3. Stage and commit with descriptive message
4. Offer to push and create PR

### Example 2: Prepare Pull Request

```
Create a PR for my current branch with a description based on recent commits
```

Warp will:
1. Analyze commits since branching
2. Generate PR title and description
3. Create pull request on GitHub
4. Add relevant labels

### Example 3: Release Workflow

```
Create a release branch for version 0.2.0, update version files, generate changelog, and create a PR
```

Warp will:
1. Create `release/0.2.0` branch
2. Update version numbers
3. Generate changelog from commits
4. Create PR with release notes

### Example 4: Review PR Status

```
What's the status of PR #45? Are there any failing checks?
```

Warp will:
1. Fetch PR details
2. Check CI/CD status
3. Report any failures
4. Suggest fixes if needed

### Example 5: Auto-fix and Commit

```
Fix the linting errors in week4 and commit the changes
```

Warp will:
1. Run linter to identify issues
2. Apply auto-fixes
3. Stage changes
4. Commit with message like "fix: Resolve linting errors in routers/notes.py"

## Repository-Specific Workflows

### For CS146S Repository

The MCP server is pre-configured to work with common workflows in this repository:

#### Weekly Assignment Flow
```
Start work on week5 assignment: create branch, set up initial structure
```

#### Test-Driven Development
```
Create a branch for adding search functionality to notes, write failing tests, implement the feature, and commit when tests pass
```

#### Documentation Updates
```
Sync API docs for week4, commit changes to docs/API.md
```

## Available Tools

Common GitHub MCP tools you can use:

| Tool | Description |
|------|-------------|
| `github_create_branch` | Create a new branch |
| `github_create_pull_request` | Open a new PR |
| `github_push_files` | Push changes to remote |
| `github_list_issues` | Query issues |
| `github_get_file_contents` | Read file from repo |
| `github_create_issue` | Create new issue |
| `github_update_pull_request` | Update PR details |
| `github_merge_pull_request` | Merge a PR |
| `github_create_release` | Create GitHub release |

## Security Best Practices

- ✓ Never commit your GitHub token to the repository
- ✓ Use minimal required permissions for PAT
- ✓ Rotate tokens periodically (every 90 days)
- ✓ Use separate tokens for different projects
- ✓ Revoke tokens immediately if compromised

## Troubleshooting

### MCP Server Won't Start

Check Docker:
```bash
docker ps
docker logs $(docker ps -q --filter ancestor=ghcr.io/github/github-mcp-server)
```

### Authentication Errors

1. Verify token has correct permissions
2. Check token hasn't expired
3. Try regenerating token

View logs:
```bash
cd "$HOME/Library/Application Support/dev.warp.Warp-Stable/mcp"
tail -f github.log
```

### Permission Denied Errors

Your token might need additional scopes. Regenerate with:
- `repo` (for private repos)
- `workflow` (for Actions)
- `write:org` (for org operations)

## Advanced: Custom MCP Workflows

You can combine the Git MCP with saved prompts for powerful workflows:

### Automated Hotfix
```
I need to hotfix a bug in production. Create a hotfix branch, apply the fix to notes.py line 45, run tests, and create an urgent PR.
```

### Weekly Assignment Submission
```
I'm done with week4 assignment. Run all checks, ensure tests pass, create a final commit, and prepare submission PR.
```

### Code Review Assistant
```
Review PR #12 and check if it follows repository standards from WARP.md
```

## Integration with Saved Prompts

The Git MCP works seamlessly with your saved prompts:

- **Test Runner** → Auto-commit passing tests
- **Docs Sync** → Auto-commit doc updates  
- **Refactor Harness** → Create refactor branch automatically
- **Release Helper** → Push releases and create GitHub releases

## Removing the MCP Server

To remove the Git MCP server:

1. Open Warp → MCP Servers
2. Find "GitHub" server
3. Click Stop, then Delete
4. Revoke the GitHub token on GitHub.com

Or via Docker:
```bash
docker stop $(docker ps -q --filter ancestor=ghcr.io/github/github-mcp-server)
docker rmi ghcr.io/github/github-mcp-server
```

## Additional Resources

- [GitHub MCP Server Docs](https://github.com/github/github-mcp-server)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Warp MCP Documentation](https://docs.warp.dev/features/mcp)
