import csv
import os

SCORES_FILE = "scores.csv"


def save_score(player_name, quiz_name, score, total_questions):
    if total_questions == 0:
        percentage = 0.0
    else:
        percentage = (score / total_questions) * 100

    file_exists = os.path.exists(SCORES_FILE)

    with open(SCORES_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "Player Name", "Quiz Name", "Score", "Total", "Percentage"
            ])

        writer.writerow([
            player_name, quiz_name, score, total_questions,
            f"{percentage:.1f}%"
        ])


def get_all_scores():
    if not os.path.exists(SCORES_FILE):
        return []

    try:
        with open(SCORES_FILE, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception:
        return []


def get_top_10_leaderboard():
    scores = get_all_scores()

    if not scores:
        return []

    def sort_key(x):
        try:
            return float(x["Percentage"].replace("%", ""))
        except (ValueError, KeyError, AttributeError):
            return 0.0

    sorted_scores = sorted(scores, key=sort_key, reverse=True)

    return sorted_scores[:10]