#!/usr/bin/env python3
import re

def read_readme(repo):
    """Read the current README content"""
    readme = repo.get_contents("README.md")
    return readme.decoded_content.decode('utf-8')

def update_readme(repo, content):
    """Update the README with new content"""
    readme = repo.get_contents("README.md")
    repo.update_file(
        "README.md",
        "Update Tic-Tac-Toe game state",
        content,
        readme.sha
    )

def create_blank_table(owner, repo_name):
    """Create a blank Tic-Tac-Toe table"""
    table = ['<table>']
    
    for row in range(3):
        table.append('  <tr>')
        for col in range(3):
            pos = row * 3 + col + 1
            table.append(f'    <td width="80" height="80" align="center">')
            table.append(f'      <a href="https://github.com/{owner}/{repo_name}/issues/new?title=ttt%7Cmove%7C{pos}&body=Just+click+submit+to+make+your+move!">')
            table.append(f'        <img src="https://raw.githubusercontent.com/{owner}/{repo_name}/main/assets/blank.png" width="50" alt="blank">')
            table.append('      </a>')
            table.append('    </td>')
        table.append('  </tr>')
    
    table.append('</table>')
    return '\n'.join(table)

def update_game_history(readme_content, issue_creator, current_player, position):
    """Update the game history section in README"""
    if "No moves yet!" in readme_content:
        new_history = f"- {issue_creator} played {current_player} at position {position}"
    else:
        history_match = re.search(r'## Game History:(.*?)<div', readme_content, re.DOTALL)
        if history_match:
            current_history = history_match.group(1).strip()
            new_history = f"{current_history}\n- {issue_creator} played {current_player} at position {position}"
        else:
            new_history = f"- {issue_creator} played {current_player} at position {position}"
    
    return re.sub(r'## Game History:.*?<div', f'## Game History:\n{new_history}\n\n<div', readme_content, flags=re.DOTALL)

def update_status(readme_content, new_status):
    """Update the status line in README"""
    return re.sub(r'\*\*Status:\*\*.*', new_status, readme_content)

def replace_cell(readme_content, position, owner, repo_name, player_image, player_alt):
    """Replace a cell in the game board with a player's mark"""
    cell_pattern = re.compile(
        r'<td width="80" height="80" align="center">\s*'
        r'<a href="https://github\.com/[^/]+/[^/]+/issues/new\?title=ttt%7Cmove%7C' + str(position) + r'[^>]*>\s*'
        r'<img[^>]*>\s*'
        r'</a>\s*'
        r'</td>', 
        re.DOTALL
    )
    
    # New cell HTML
    new_cell = f'<td width="80" height="80" align="center"><img src="https://raw.githubusercontent.com/{owner}/{repo_name}/main/assets/{player_image}" width="50" alt="{player_alt}"></td>'
    
    # Replace the cell
    return cell_pattern.sub(new_cell, readme_content)