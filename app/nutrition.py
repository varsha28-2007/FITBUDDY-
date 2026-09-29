"""Optional nutrition-specific helpers."""

GOAL_HINTS = {
    "weight loss": "Focus on a mild calorie deficit, high protein and plenty of fibre.",
    "muscle gain": "Aim for a slight calorie surplus with protein at every meal.",
    "general fitness": "Eat balanced meals and stay hydrated through the day.",
}


def quick_hint(goal: str) -> str:
    goal = (goal or "").lower()
    for key, hint in GOAL_HINTS.items():
        if key in goal:
            return hint
    return GOAL_HINTS["general fitness"]
