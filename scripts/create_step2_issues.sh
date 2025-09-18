#!/usr/bin/env bash
set -euo pipefail

# Requires GitHub CLI: https://cli.github.com/
# Usage: GITHUB_TOKEN=... ./scripts/create_step2_issues.sh owner/repo
REPO="${1:-}"
if [[ -z "$REPO" ]]; then
  echo "Usage: $0 <owner>/<repo>" >&2
  exit 1
fi

create_issue() {
  local title="$1"; shift
  local file="$1"; shift
  gh issue create \
    --repo "$REPO" \
    --title "$title" \
    --label "user-story,step2" \
    --body-file "$file"
}

create_issue "US01 - User Registration" .github/issue_templates/US01_user_registration.md
create_issue "US02 - User Login" .github/issue_templates/US02_user_login.md
create_issue "US03 - Create TODO" .github/issue_templates/US03_create_todo.md
create_issue "US04 - Read/List TODOs" .github/issue_templates/US04_read_list_todos.md
create_issue "US05 - Update TODO" .github/issue_templates/US05_update_todo.md
create_issue "US06 - Delete TODO" .github/issue_templates/US06_delete_todo.md

echo "All Step 2 user stories created as GitHub issues in $REPO"
