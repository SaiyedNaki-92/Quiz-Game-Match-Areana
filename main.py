import streamlit as st
import random
import csv
import os
from datetime import datetime

from questions import questions
from quiz_logic import check_answer
from scoreboard import save_score, get_top_10_leaderboard
from ui import (
    add_custom_style,
    show_home,
    show_player_cards,
    show_question,
    show_leaderboard,
    show_match_history
)


MATCH_FILE = "match_records.csv"


st.set_page_config(
    page_title="Match Arena",
    page_icon="🎮",
    layout="wide"
)

add_custom_style()


# Save completed match details
def save_match(player1, player2, score1, score2, total, topic):
    file_exists = os.path.exists(MATCH_FILE)

    if score1 > score2:
        winner = player1
    elif score2 > score1:
        winner = player2
    else:
        winner = "Draw"

    with open(MATCH_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists or os.path.getsize(MATCH_FILE) == 0:
            writer.writerow([
                "Date", "Player 1", "Player 2",
                "Score 1", "Score 2", "Total Questions",
                "Topic", "Winner"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            player1, player2, score1, score2, total, topic, winner
        ])


# Read previous matches
def get_match_history():
    if not os.path.exists(MATCH_FILE):
        return []

    try:
        with open(MATCH_FILE, "r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except (OSError, csv.Error):
        return []


# Start a new game
def start_new_game(player1, player2, topic):
    available_questions = questions[topic]
    total_questions = min(5, len(available_questions))

    st.session_state.game_started = True
    st.session_state.game_finished = False
    st.session_state.game_saved = False

    st.session_state.player1 = player1
    st.session_state.player2 = player2
    st.session_state.topic = topic

    st.session_state.game_questions = random.sample(
        available_questions, total_questions
    )

    st.session_state.round_number = 0
    st.session_state.score1 = 0
    st.session_state.score2 = 0
    st.session_state.answers = {}
    st.session_state.phase = "player1"


# Reset the game
def reset_game():
    keys_to_remove = [
        "game_started", "game_finished", "game_saved",
        "player1", "player2", "topic", "game_questions",
        "round_number", "score1", "score2", "answers", "phase"
    ]

    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]


# Initialize the game
if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "game_finished" not in st.session_state:
    st.session_state.game_finished = False


# Display application heading
show_home()


# HOME SCREEN
if not st.session_state.game_started:

    st.markdown("## ⚔️ Ready for the Battle?")
    st.write("Challenge a friend and compete to get the highest score.")

    col1, col2 = st.columns(2)

    with col1:
        player1 = st.text_input(
            "🔵 Player 1 Name",
            value="Player 1"
        )

    with col2:
        player2 = st.text_input(
            "🟣 Player 2 Name",
            value="Player 2"
        )

    topic = st.selectbox(
        "📚 Select Quiz Topic",
        list(questions.keys())
    )

    if st.button(
        "⚔️ START BATTLE",
        type="primary",
        use_container_width=True
    ):
        if not player1.strip() or not player2.strip():
            st.error("Please enter both player names.")

        elif player1.strip().lower() == player2.strip().lower():
            st.error("Please enter two different player names.")

        elif not questions.get(topic):
            st.error("No questions are available for this topic.")

        else:
            start_new_game(
                player1.strip(),
                player2.strip(),
                topic
            )
            st.rerun()

    st.divider()

    show_leaderboard(get_top_10_leaderboard())

    st.divider()

    show_match_history(get_match_history())


# GAME SCREEN
elif not st.session_state.game_finished:

    player1 = st.session_state.player1
    player2 = st.session_state.player2
    topic = st.session_state.topic

    game_questions = st.session_state.game_questions
    round_index = st.session_state.round_number
    total_rounds = len(game_questions)

    # Check whether all questions are completed
    if round_index >= total_rounds:
        st.session_state.game_finished = True
        st.rerun()

    question_data = game_questions[round_index]

    question_text = question_data["question"]
    options = question_data["options"]
    correct_answer = question_data["answer"]

    show_player_cards(
        player1,
        player2,
        st.session_state.score1,
        st.session_state.score2
    )

    show_question(
        question_text,
        round_index + 1,
        total_rounds,
        topic
    )

    # PLAYER 1 TURN
    if st.session_state.phase == "player1":

        st.markdown(f"### 🔵 {player1}'s Turn")
        st.info("Choose your answer, then pass the device to Player 2.")

        with st.form(key=f"player1_form_{round_index}"):

            answer1 = st.radio(
                "Select your answer:",
                list(options.keys()),
                format_func=lambda key: f"{key}. {options[key]}"
            )

            submitted = st.form_submit_button(
                "LOCK ANSWER 🔒",
                use_container_width=True
            )

        if submitted:
            st.session_state.answers[round_index] = {
                "player1": answer1
            }

            st.session_state.phase = "player2"
            st.rerun()

    # PLAYER 2 TURN
    elif st.session_state.phase == "player2":

        st.markdown(f"### 🟣 {player2}'s Turn")
        st.info("Player 1 has locked their answer. Now it's your turn.")

        with st.form(key=f"player2_form_{round_index}"):

            answer2 = st.radio(
                "Select your answer:",
                list(options.keys()),
                format_func=lambda key: f"{key}. {options[key]}"
            )

            submitted = st.form_submit_button(
                "LOCK ANSWER 🔒",
                use_container_width=True
            )

        if submitted:
            answer1 = st.session_state.answers[round_index]["player1"]

            st.session_state.answers[round_index]["player2"] = answer2

            if check_answer(answer1, correct_answer):
                st.session_state.score1 += 1

            if check_answer(answer2, correct_answer):
                st.session_state.score2 += 1

            st.session_state.phase = "reveal"
            st.rerun()

    # SHOW ROUND RESULTS
    elif st.session_state.phase == "reveal":

        answer1 = st.session_state.answers[round_index]["player1"]
        answer2 = st.session_state.answers[round_index]["player2"]

        st.markdown("## 📢 Round Results")

        st.success(
            f"Correct answer: {correct_answer}. "
            f"{options[correct_answer]}"
        )

        col1, col2 = st.columns(2)

        with col1:
            if check_answer(answer1, correct_answer):
                st.success(f"🔵 {player1}: Correct! +1 point")
            else:
                st.error(f"🔵 {player1}: Incorrect")

        with col2:
            if check_answer(answer2, correct_answer):
                st.success(f"🟣 {player2}: Correct! +1 point")
            else:
                st.error(f"🟣 {player2}: Incorrect")

        show_player_cards(
            player1,
            player2,
            st.session_state.score1,
            st.session_state.score2
        )

        if st.button(
            "NEXT ROUND ➜",
            type="primary",
            use_container_width=True
        ):
            st.session_state.round_number += 1
            st.session_state.phase = "player1"
            st.rerun()


# FINAL RESULTS
else:

    player1 = st.session_state.player1
    player2 = st.session_state.player2

    score1 = st.session_state.score1
    score2 = st.session_state.score2

    total = len(st.session_state.game_questions)
    topic = st.session_state.topic

    # Save results only once
    if not st.session_state.game_saved:

        save_score(player1, topic, score1, total)
        save_score(player2, topic, score2, total)

        save_match(
            player1,
            player2,
            score1,
            score2,
            total,
            topic
        )

        st.session_state.game_saved = True

    st.balloons()

    if score1 > score2:
        st.markdown(
            f'<div class="winner-title">🏆 {player1} WINS!</div>',
            unsafe_allow_html=True
        )

    elif score2 > score1:
        st.markdown(
            f'<div class="winner-title">🏆 {player2} WINS!</div>',
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            '<div class="winner-title">🤝 IT’S A DRAW!</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<p class="muted-text">MATCH COMPLETE • FINAL SCORE</p>',
        unsafe_allow_html=True
    )

    show_player_cards(player1, player2, score1, score2)

    col1, col2 = st.columns(2)

    with col1:
        accuracy1 = score1 / total * 100 if total else 0
        st.metric(f"{player1}'s Accuracy", f"{accuracy1:.0f}%")

    with col2:
        accuracy2 = score2 / total * 100 if total else 0
        st.metric(f"{player2}'s Accuracy", f"{accuracy2:.0f}%")

    if st.button(
        "🔄 PLAY AGAIN",
        type="primary",
        use_container_width=True
    ):
        reset_game()
        st.rerun()

    st.divider()

    show_leaderboard(get_top_10_leaderboard())

    st.divider()

    show_match_history(get_match_history())
    