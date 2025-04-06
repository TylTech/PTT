import streamlit as st

# Emoji constants
PLAYER = "👸"
BOT = "🦄"
EMPTY = "⬜"

def reset_board():
    st.session_state.board = [EMPTY] * 9
    st.session_state.turn = "player"
    st.session_state.game_over = False
    st.session_state.winner = None

def check_winner(board, icon):
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    return any(all(board[i] == icon for i in line) for line in wins)
