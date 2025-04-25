#!/usr/bin/env python3
import re

def get_current_player(readme_content):
    """Determine current player from README status line"""
    status_match = re.search(r'\*\*Status:\*\*\s*(.*)', readme_content)
    if status_match:
        status_line = status_match.group(1)
        if "X's turn" in status_line:
            return "X", "O", "x-mark.png", "X"
        elif "O's turn" in status_line:
            return "O", "X", "o-mark.png", "O"
    return "X", "O", "x-mark.png", "X"  # Default to X if can't determine

def get_board_state(readme_content):
    """Extract current board state from README"""
    board = ["blank"] * 9
    
    # Parse the entire table HTML to find positions
    table_match = re.search(r'<table>.*?</table>', readme_content, re.DOTALL)
    if table_match:
        table_html = table_match.group(0)
        
        # Find all cells
        cells = re.findall(r'<td width="80" height="80" align="center">.*?</td>', table_html, re.DOTALL)
        
        for i, cell in enumerate(cells):
            if i >= 9:  # Safety check
                break
                
            if 'alt="X"' in cell:
                board[i] = "X"
            elif 'alt="O"' in cell:
                board[i] = "O"
    
    return board

def check_win(board):
    """Check if there's a winner or draw"""
    # Win patterns: rows, columns, diagonals
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    
    for pattern in win_patterns:
        if board[pattern[0]] != "blank" and board[pattern[0]] == board[pattern[1]] == board[pattern[2]]:
            return "win", board[pattern[0]]
    
    if "blank" not in board:
        return "draw", None
        
    return "continue", None