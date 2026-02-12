def answer_similarity(ans1: dict, ans2: dict) -> float:
   
    #Calculate similarity between two answer maps.
    #similarity = same_answers / compared_questions
   
    if not ans1 or not ans2:
        return 0.0

    common_questions = set(ans1.keys()) & set(ans2.keys())
    if not common_questions:
        return 0.0

    same = 0
    for q in common_questions:
        if ans1[q] == ans2[q]:
            same += 1

    return same / len(common_questions)
