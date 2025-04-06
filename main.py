import streamlit as st
from modes import solo_mode, local_two_player, online_multiplayer

st.set_page_config(page_title="Princess Tac Toe", layout="centered")
st.title("✨ Princess Tac Toe 👸🦄")

# Game mode selector
mode = st.radio(
    "Choose your royal game mode:",
    ["Solo vs Bot", "Local Two Player", "Online Multiplayer"]
)

# Route to selected mode
if mode == "Solo vs Bot":
    solo_mode.run()
elif mode == "Local Two Player":
    st.info("🛋️ Local mode coming soon!")
    # local_two_player.run()
elif mode == "Online Multiplayer":
    st.info("🌐 Online multiplayer coming soon!")
    # online_multiplayer.run()
