#!/usr/bin/env python3
import os
import sys
from github import Github
from board import get_current_player, get_board_state, check_win
from readme import read_readme, update_readme
from commands import reset_game, process_move

# Environment variables
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
ISSUE_TITLE = os.environ['ISSUE_TITLE']
ISSUE_NUMBER = int(os.environ['ISSUE_NUMBER'])
ISSUE_CREATOR = os.environ['ISSUE_CREATOR']
REPO_NAME = os.environ['REPO_NAME']

# Initialize Github client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)
issue = repo.get_issue(ISSUE_NUMBER)

# Close the issue immediately
issue.create_comment("Processing your request...")
issue.edit(state='closed')

# Parse command from issue title
# Format: ttt|command|parameter
parts = ISSUE_TITLE.split('|')
command = parts[1] if len(parts) > 1 else ""
position = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0

# Main execution
try:
    readme_content = read_readme(repo)
    
    if command == "reset":
        reset_game(repo, issue, readme_content)
    elif command == "move" and position > 0:
        process_move(repo, issue, readme_content, position, ISSUE_CREATOR)
    else:
        issue.create_comment("Invalid command. Please use 'ttt|move|position' or 'ttt|reset'.")
        
except Exception as e:
    issue.create_comment(f"Error processing your request: {str(e)}")
    print(f"Error: {str(e)}")
    sys.exit(1)