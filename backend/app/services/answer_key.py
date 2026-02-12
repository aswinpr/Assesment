def generate_answer_key_from_answers(answers: dict):
    """
    Deterministic synthetic answer key.
    Pattern: A, B, C, D repeating.
    """

    if not answers:
        return {}

    pattern = ["A", "B", "C", "D"]
    key = {}

    # Sort question ids for stable ordering
    sorted_questions = sorted(answers.keys())

    for index, q_id in enumerate(sorted_questions):
        key[q_id] = pattern[index % 4]

    return key
