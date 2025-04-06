import streamlit as st
import random
from utils.game_logic import check_winner, reset_board, EMPTY, PLAYER, BOT

def run():
    st.header("👸 Solo Mode: Princess vs. Unicorn Bot 🦄")

    if "board" not in st.session_state:
        reset_board()

    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            index = i * 3 + j
            with cols[j]:
                if st.button(st.session_state.board[index], key=f"cell_{index}", use_container_width=True):
                    if not st.session_state.game_over and st.session_state.board[index] == EMPTY and st.session_state.turn == "player":
                        st.session_state.board[index] = PLAYER
                        if check_winner(st.session_state.board, PLAYER):
                            st.session_state.game_over = True
                            st.session_state.winner = PLAYER
                        elif EMPTY not in st.session_state.board:
                            st.session_state.game_over = True
                        else:
                            st.session_state.turn = "bot"
                            bot_move()

    if st.session_state.game_over:
        if st.session_state.winner == PLAYER:
            st.success("🎉 Princess wins!")
        elif st.session_state.winner == BOT:
            st.error("🦄 Unicorn wins!")
        else:
            st.info("🤝 It's a draw!")

    st.button("🔄 Reset Game", on_click=reset_board)

def bot_move():
    available = [i for i, val in enumerate(st.session_state.board) if val == EMPTY]
    if available:
        move = random.choice(available)
        st.session_state.board[move] = BOT
        if check_winner(st.session_state.board, BOT):
            st.session_state.game_over = True
            st.session_state.winner = BOT
        elif EMPTY not in st.session_state.board:
            st.session_state.game_over = True
        else:
            st.session_state.turn = "player"
