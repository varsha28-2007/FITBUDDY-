"""Workout plan generation using the Gemini Pro model."""
from .config import get_client, PRO_MODEL_NAME


def generate_workout_gemini(user_input: dict) -> str:
    prompt = f"""
You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for someone with the goal of **{user_input['goal']}**, and who prefers **{user_input['intensity']}** intensity workouts.

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)
"""
    try:
        client = get_client()
        response = client.models.generate_content(model=PRO_MODEL_NAME, contents=prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
