# game/logic.py

def check_text(guess, answer):
    return "🟩" if guess == answer else "⬛"

def check_list(guess_list, answer_list):
    if set(guess_list) == set(answer_list):
        return "🟩"
    if set(guess_list) & set(answer_list):
        return "🟨"
    return "⬛"

def evaluate_guess(guess, answer, year_guess, year_answer):
    return {
        "gender": check_text(guess["gender"], answer["gender"]),
        "positions": check_list(guess["positions"], answer["positions"]),
        "species": check_list(guess["species"], answer["species"]),
        "resource": check_text(guess["resource"], answer["resource"]),
        "range_type": check_list(guess["range_type"], answer["range_type"]),
        "regions": check_list(guess["regions"], answer["regions"]),
        "year": (
            "🟩" if year_guess == year_answer
            else "🔼" if year_guess < year_answer
            else "🔽"
        )
    }
