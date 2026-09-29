"""All FastAPI routes: web pages (HTML) and JSON APIs."""
import os

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .config import BASE_DIR
from .database import (
    SessionLocal, User, WorkoutPlan,
    save_user, save_plan, update_plan, get_original_plan, get_user,
)
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .schemas import UserInput, FeedbackRequest, WorkoutRequest
from .updated_plan import update_workout_plan

router = APIRouter()

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


# ---------------------------------------------------------------- Web pages
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Displays the user form via index.html"""
    return templates.TemplateResponse(request, "index.html", {})


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    """Processes user input and generates a personalised workout plan."""
    data = UserInput(username=username, user_id=user_id, age=age,
                     weight=weight, goal=goal, intensity=intensity)

    plan = generate_workout_gemini({"goal": data.goal, "intensity": data.intensity})
    tip = generate_nutrition_tip_with_flash(data.goal)

    save_user(data.user_id, data.username, data.age, data.weight, data.goal, data.intensity)
    save_plan(data.user_id, plan)

    return templates.TemplateResponse(request, "result.html", {
        "request": request,
        "username": data.username,
        "user_id": data.user_id,
        "age": data.age,
        "weight": data.weight,
        "goal": data.goal,
        "intensity": data.intensity,
        "workout_plan": plan,
        "nutrition_tip": tip,
        "message": None,
    })


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: int = Form(...), feedback: str = Form(...)):
    """Updates the workout plan based on user feedback."""
    original = get_original_plan(user_id)
    user = get_user(user_id)
    if not original or not user:
        return HTMLResponse(
            "<h3>No plan found for this User ID. Please generate a plan first.</h3>"
            "<a href='/'>Back to home</a>",
            status_code=404,
        )

    updated = update_workout_plan(original, feedback)
    update_plan(user_id, updated)
    tip = generate_nutrition_tip_with_flash(user.goal)

    return templates.TemplateResponse(request, "result.html", {
        "request": request,
        "username": user.name,
        "user_id": user.id,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
        "workout_plan": updated,
        "nutrition_tip": tip,
        "message": "Your plan has been updated based on your feedback!",
    })


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    """Admin dashboard: all users and their original / updated plans."""
    db = SessionLocal()
    users = db.query(User).all()
    user_data = []
    for user in users:
        plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
        user_data.append({
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "original_plan": plan.original_plan if plan else "N/A",
            "updated_plan": plan.updated_plan if plan and plan.updated_plan else "Not updated",
        })
    db.close()
    return templates.TemplateResponse(request, "all_users.html", {
        "request": request,
        "users": user_data,
    })


# ---------------------------------------------------------------- JSON APIs (test at /docs)
@router.post("/generate-workout/gemini")
async def generate_gemini_workout(request: WorkoutRequest):
    """API: Generate workout using Gemini Pro."""
    try:
        result = generate_workout_gemini({"goal": request.goal, "intensity": request.intensity})
        return {"model": "gemini-pro", "workout_plan": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nutrition-tip")
def get_flash_tip(goal: str):
    """API: Generate nutrition tip using Gemini Flash."""
    tip = generate_nutrition_tip_with_flash(goal)
    return {"goal": goal, "nutrition_tip": tip}


@router.post("/generate-plan")
def generate_plan(user_data: UserInput):
    """API: Save user info & generate plan."""
    try:
        save_user(user_data.user_id, user_data.username, user_data.age,
                  user_data.weight, user_data.goal, user_data.intensity)
        plan = generate_workout_gemini({"goal": user_data.goal, "intensity": user_data.intensity})
        save_plan(user_data.user_id, plan)
        return {"message": "Workout plan generated and saved successfully!", "workout_plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


@router.post("/update-plan/{user_id}", response_model=dict)
def update_user_plan(user_id: int, data: FeedbackRequest):
    """API: Update workout plan based on user feedback."""
    original = get_original_plan(user_id)
    if not original:
        return {"error": "Original plan not found for this user."}
    updated = update_workout_plan(original, data.feedback)
    update_plan(user_id, updated)
    return {"updated_plan": updated}
