import streamlit as st


def add_custom_style():
    st.markdown("""
        <style>
        /* Main background */
        .stApp {
            background: linear-gradient(135deg, #0b1020, #171936);
            color: #ffffff;
        }

        /* Main content width */
        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
        }

        /* Headings */
        h1, h2, h3 {
            color: #ffffff;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #5146e5, #8b5cf6);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 18px;
            font-weight: bold;
            transition: 0.2s;
        }

        .stButton > button:hover {
            background: linear-gradient(90deg, #6d63ff, #a78bfa);
            color: white;
            border: none;
        }

        /* Player score cards */
        [data-testid="stMetric"] {
            background-color: #1c2442;
            padding: 18px;
            border: 1px solid #343d68;
            border-radius: 14px;
        }

        [data-testid="stMetricLabel"] {
            color: #c4caff;
        }

        [data-testid="stMetricValue"] {
            color: #a78bfa;
        }

        /* Progress bar */
        [data-testid="stProgressBar"] > div > div {
            background-color: #8b5cf6;
        }

        /* Input fields */
        .stTextInput input {
            background-color: #1c2442;
            color: white;
            border-radius: 8px;
        }

        /* Select box */
        div[data-baseweb="select"] {
            background-color: #1c2442;
            border-radius: 8px;
        }

        /* Radio options */
        .stRadio label {
            color: #e5e7eb;
        }

        /* Divider */
        hr {
            border-color: #343d68;
        }

        /* Tables */
        [data-testid="stDataFrame"] {
            border: 1px solid #343d68;
            border-radius: 10px;
        }

        /* Information messages */
        [data-testid="stAlert"] {
            border-radius: 10px;
        }

        /* Winner banner */
        .winner-title {
            background: linear-gradient(90deg, #5146e5, #a855f7);
            padding: 24px;
            border-radius: 16px;
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            color: white;
            margin: 15px 0;
        }

        /* Small description */
        .muted-text {
            text-align: center;
            color: #aab4d6;
            font-size: 14px;
        }
        </style>
    """, unsafe_allow_html=True)


def show_home():
    st.markdown(
        """
        <div style="text-align:center; padding:15px 0 25px 0;">
            <div style="font-size:48px;">🎮</div>
            <h1 style="color:#a78bfa; margin-bottom:5px;">
                MATCH ARENA
            </h1>
            <p style="color:#b9c4e8; font-size:16px;">
                THINK FAST &nbsp; • &nbsp; PLAY SMART &nbsp; • &nbsp; WIN
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_player_cards(player1, player2, score1, score2):
    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        st.markdown(
            f"""
            <div style="
                background:#1c2442;
                border:1px solid #3b82f6;
                border-radius:14px;
                padding:18px;
                text-align:center;
            ">
                <div style="font-size:30px;">🔵</div>
                <div style="color:#bfdbfe;font-size:18px;">
                    {player1}
                </div>
                <div style="color:white;font-size:36px;font-weight:bold;">
                    {score1}
                </div>
                <div style="color:#94a3b8;font-size:12px;">
                    PLAYER 1
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style="text-align:center; padding-top:35px;">
                <div style="
                    color:#f0abfc;
                    font-size:27px;
                    font-weight:bold;
                ">VS</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="
                background:#1c2442;
                border:1px solid #a855f7;
                border-radius:14px;
                padding:18px;
                text-align:center;
            ">
                <div style="font-size:30px;">🟣</div>
                <div style="color:#e9d5ff;font-size:18px;">
                    {player2}
                </div>
                <div style="color:white;font-size:36px;font-weight:bold;">
                    {score2}
                </div>
                <div style="color:#94a3b8;font-size:12px;">
                    PLAYER 2
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def show_question(question, round_number, total_rounds, topic):
    st.markdown(
        f"""
        <div style="
            background:#171e38;
            border:1px solid #343d68;
            border-radius:12px;
            padding:12px;
            margin:20px 0 10px 0;
        ">
            <div style="
                color:#a78bfa;
                text-align:center;
                font-size:13px;
                font-weight:bold;
            ">
                {topic}
            </div>
            <div style="
                color:white;
                text-align:center;
                font-size:18px;
                margin-top:8px;
            ">
                ROUND {round_number} / {total_rounds}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(round_number / total_rounds)

    st.markdown(
        f"""
        <div style="
            background:#1c2442;
            border:1px solid #343d68;
            border-radius:15px;
            padding:25px 20px;
            margin:15px 0;
            color:white;
            font-size:22px;
            font-weight:bold;
            text-align:center;
        ">
            ❓ {question}
        </div>
        """,
        unsafe_allow_html=True
    )


def show_leaderboard(scores):
    st.subheader("🏆 Leaderboard")

    if scores is not None and len(scores) > 0:
        st.dataframe(
            scores,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No scores yet. Play a match to appear here!")


def show_match_history(records):
    st.subheader("📜 Match History")

    if records:
        st.dataframe(
            records,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No previous matches available.")