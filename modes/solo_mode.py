import streamlit as st
import random
import time

# Constants
EMPTY = "⬜"
PLAYER = "👸"
BOT = "🦄"
THINKING = "🤔"  # Special state for when bot is thinking

def check_winner(board, player):
    """Check if the given player has won"""
    win_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]

    for combo in win_combos:
        if all(board[i] == player for i in combo):
            return True
    return False

def reset_board():
    """Reset the game board and state"""
    if 'scores' not in st.session_state:
        st.session_state.scores = {'player': 0, 'bot': 0, 'ties': 0}

    st.session_state.board = [EMPTY] * 9
    st.session_state.game_state = "player_turn"  # States: player_turn, waiting_for_bot_trigger, bot_thinking, player_turn
    st.session_state.game_over = False
    st.session_state.winner = None
    # Reset the timestamp for bot thinking
    if 'bot_think_start' in st.session_state:
        del st.session_state.bot_think_start

def run():
    # Initialize session state
    if "board" not in st.session_state:
        reset_board()

    if "bot_difficulty" not in st.session_state:
        st.session_state.bot_difficulty = "easy"

    # Game controls
    col1, col2 = st.columns([3, 1])

    with col1:
        # Bot difficulty
        bot_difficulty = st.radio(
            "Unicorn Bot Level:",
            ["Easy", "Smart"],
            horizontal=True,
            index=0 if st.session_state.bot_difficulty == "easy" else 1,
        )
        st.session_state.bot_difficulty = bot_difficulty.lower()

    with col2:
        # Score display
        scores = st.session_state.scores
        st.write(f"👸 {scores['player']} | 🦄 {scores['bot']} | 🤝 {scores['ties']}")

    # Game status message
    status = st.empty()

    # Process bot thinking state
    board = st.session_state.board

    # State for when the bot is actively thinking
    if st.session_state.game_state == "bot_thinking":
        # Show that it's now the bot's turn
        status.warning("🦄 Unicorn is thinking...")
        
        # Start the bot thinking timer if not already started
        if 'bot_think_start' not in st.session_state:
            st.session_state.bot_think_start = time.time()
            st.rerun()  # Rerun to show "thinking" message
            
        # Check if bot has been "thinking" long enough (2 seconds)
        elapsed = time.time() - st.session_state.bot_think_start
        if elapsed < 2:
            # Still thinking, wait longer
            time.sleep(0.1)  # Small sleep to not block the UI
            st.rerun()
        else:
            # Bot has thought long enough, now make the move
            # Calculate bot's move
            bot_move = decide_bot_move(board)
            
            # Update the board with the bot's move
            board[bot_move] = BOT
            
            # Check for win condition
            if check_winner(board, BOT):
                st.session_state.game_over = True
                st.session_state.winner = BOT
                st.session_state.scores['bot'] += 1
            elif EMPTY not in board:
                st.session_state.game_over = True
                st.session_state.scores['ties'] += 1
            else:
                st.session_state.game_state = "player_turn"
                
            # Clean up the timer
            del st.session_state.bot_think_start
            st.rerun()

    # Show game status based on game state
    if st.session_state.game_over:
        if st.session_state.winner == PLAYER:
            status.success("🎉 Princess wins! 👑")
            st.balloons()
        elif st.session_state.winner == BOT:
            status.error("🦄 Unicorn wins! ✨")
        else:
            status.info("🤝 It's a draw!")
    elif st.session_state.game_state == "bot_thinking":
        status.warning("🦄 Unicorn is thinking...")
    elif st.session_state.game_state == "waiting_for_bot_trigger":
        status.info("🔄 Click 'Let the Unicorn Move' button below")
    else:
        status.info("👸 Princess's turn!")

    # Create the game grid
    for row in range(3):
        cols = st.columns([1, 1, 1])
        for col in range(3):
            index = row * 3 + col
            with cols[col]:
                cell_value = board[index]

                if cell_value == PLAYER:
                    # Princess cell
                    st.markdown(
                        f'<div style="background-color:#FFD1DC; color:black; border-radius:5px; padding:10px; text-align:center; font-size:24px;">{PLAYER}</div>',
                        unsafe_allow_html=True
                    )
                elif cell_value == BOT:
                    # Unicorn cell
                    st.markdown(
                        f'<div style="background-color:#D1F0FF; color:black; border-radius:5px; padding:10px; text-align:center; font-size:24px;">{BOT}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    # Empty cell - clickable for player
                    if st.button(
                        EMPTY,
                        key=f"cell_{index}",
                        use_container_width=True,
                        disabled=st.session_state.game_state != "player_turn" or st.session_state.game_over,
                    ):
                        # Handle player move
                        board[index] = PLAYER

                        # Check game conditions
                        if check_winner(board, PLAYER):
                            st.session_state.game_over = True
                            st.session_state.winner = PLAYER
                            st.session_state.scores['player'] += 1
                        elif EMPTY not in board:
                            st.session_state.game_over = True
                            st.session_state.scores['ties'] += 1
                        else:
                            # Switch to waiting for unicorn button to be pressed
                            st.session_state.game_state = "waiting_for_bot_trigger"

                        st.rerun()
    
    # Unicorn move button - only show when waiting for bot trigger
    if st.session_state.game_state == "waiting_for_bot_trigger":
        # Add custom CSS for green button
        st.markdown("""
        <style>
        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #4CAF50;
            color: white;
            border-color: #4CAF50;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            background-color: #45a049;
            border-color: #45a049;
        }
        </style>
        """, unsafe_allow_html=True)
        
        unicorn_col1, unicorn_col2, unicorn_col3 = st.columns([1, 2, 1])
        with unicorn_col2:
            if st.button("🦄 Let the Unicorn Move", 
                        use_container_width=True, 
                        key="unicorn_move",
                        type="primary"):
                st.session_state.game_state = "bot_thinking"
                st.rerun()

    # Reset button
    reset_col1, reset_col2, reset_col3 = st.columns([1, 2, 1])
    with reset_col2:
        if st.button("🔄 New Game", use_container_width=True):
            reset_board()
            st.rerun()

def decide_bot_move(board):
    """Decide the bot's move but don't apply it yet"""
    # Get available moves
    available = [i for i, val in enumerate(board) if val == EMPTY]

    if available:
        # Choose move based on difficulty
        if st.session_state.bot_difficulty == "easy":
            # Easy mode: completely random moves
            return random.choice(available)
        else:
            # Smart mode: strategic moves
            return find_best_move(board)
    return -1  # No moves available

def find_best_move(board):
    """Find the best move for the bot"""
    # Check if bot can win in next move
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = BOT
            if check_winner(board, BOT):
                board[i] = EMPTY
                return i
            board[i] = EMPTY

    # Check if player can win in next move and block
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = PLAYER
            if check_winner(board, PLAYER):
                board[i] = EMPTY
                return i
            board[i] = EMPTY

    # Take center if available
    if board[4] == EMPTY:
        return 4

    # Take corners if available
    corners = [0, 2, 6, 8]
    available_corners = [i for i in corners if board[i] == EMPTY]
    if available_corners:
        return random.choice(available_corners)

    # Take any available edge
    edges = [1, 3, 5, 7]
    available_edges = [i for i in edges if board[i] == EMPTY]
    if available_edges:
        return random.choice(available_edges)

    # Fallback - take any available move
    available = [i for i, val in enumerate(board) if val == EMPTY]
    return random.choice(available) if available else -1

if __name__ == "__main__":
    run()