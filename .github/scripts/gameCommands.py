#!/usr/bin/env python3
import re
from board import get_current_player, get_board_state, check_win
from readme import create_blank_table, update_readme, update_game_history, update_status, replace_cell

def reset_game(repo, issue, readme_content):
    """Reset the game board"""
    owner, repo_name = repo.full_name.split('/')
    
    # Replace the table
    new_table = create_blank_table(owner, repo_name)
    new_readme = re.sub(r'<table>.*?</table>', new_table, readme_content, flags=re.DOTALL)
    
    # Update status
    new_status = "**Status:** Game in progress. X's turn!"
    new_readme = update_status(new_readme, new_status)
    
    # Reset game history
    new_history = "No moves yet! Be the first to play."
    new_readme = re.sub(r'## Game History:.*?<div', f'## Game History:\n{new_history}\n\n<div', new_readme, flags=re.DOTALL)
    
    # Update README
    update_readme(repo, new_readme)
    
    # Comment on issue
    issue.create_comment("Game has been reset! A new game is ready to play.")

def process_move(repo, issue, readme_content, position, issue_creator):
    """Process a player move"""
    owner, repo_name = repo.full_name.split('/')
    current_player, next_player, player_image, player_alt = get_current_player(readme_content)
    
    # Check if position is already taken
    board = get_board_state(readme_content)
    if position < 1 or position > 9 or board[position-1] != "blank":
        issue.create_comment(f"Position {position} is invalid or already taken. Please choose another position.")
        return
    
    # Update board with the new move
    board[position-1] = current_player
    
    # Check game status
    result, winner = check_win(board)
    
    # Replace the cell for the current move
    new_readme = replace_cell(readme_content, position, owner, repo_name, player_image, player_alt)
    
    # Update status based on game result
    if result == "win":
        new_status = f"**Status:** Game over! {current_player} wins! 🎉"
        comment_status = f"Game over! {current_player} wins! 🎉"
    elif result == "draw":
        new_status = "**Status:** Game over! It's a draw! 🤝"
        comment_status = "Game over! It's a draw! 🤝"
    else:
        new_status = f"**Status:** Game in progress. {next_player}'s turn!"
        comment_status = f"It's now {next_player}'s turn!"
    
    new_readme = update_status(new_readme, new_status)
    
    # Update game history
    new_readme = update_game_history(new_readme, issue_creator, current_player, position)
    
    # Update README
    update_readme(repo, new_readme)
    
    # Comment on issue
    issue.create_comment(f"Move processed! {current_player} played at position {position}. {comment_status}")