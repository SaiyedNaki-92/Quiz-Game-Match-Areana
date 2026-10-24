def check_answer(selected_answer, correct_answer):
    return selected_answer.strip().upper() == correct_answer.strip().upper()


def calculate_score(answers):
    return sum(
        1 for selected, correct in answers
        if check_answer(selected, correct)
    )


def calculate_percentage(score, total_questions):
    if total_questions == 0:
        return 0.0
    return (score / total_questions) * 100

