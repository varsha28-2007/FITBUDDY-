"""Pydantic models used to validate request data."""
from pydantic import BaseModel


class UserInput(BaseModel):
    username: str
    user_id: int
    age: int
    weight: float
    goal: str
    intensity: str


class FeedbackRequest(BaseModel):
    user_id: int
    feedback: str


class WorkoutRequest(BaseModel):
    goal: str
    intensity: str
