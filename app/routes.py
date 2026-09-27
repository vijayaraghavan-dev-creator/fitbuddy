import os

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import save_user, save_plan, update_plan, get_original_plan, get_all_users, get_all_plans
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "app", "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
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
    save_user(
        user_id=user_id,
        name=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
    )

    plan = generate_workout_gemini({"goal": goal, "intensity": intensity})
    nutrition_tip = generate_nutrition_tip_with_flash(goal)
    save_plan(user_id, plan)

    return templates.TemplateResponse(request, "result.html", {
        "username": username,
        "user_id": user_id,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity,
        "workout_plan": plan,
        "nutrition_tip": nutrition_tip,
    })


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...),
):
    original = get_original_plan(user_id)

    if not original:
        return templates.TemplateResponse(request, "result.html", {
            "error": "Original plan not found for this user.",
        })

    updated = update_workout_plan(original, feedback)
    update_plan(user_id, updated)

    return templates.TemplateResponse(request, "result.html", {
        "user_id": user_id,
        "workout_plan": original,
        "updated_plan": updated,
        "feedback_submitted": True,
    })


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    users = get_all_users()
    plans = get_all_plans()
    plans_by_user = {p.user_id: p for p in plans}

    user_data = []
    for user in users:
        plan = plans_by_user.get(user.id)
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

    return templates.TemplateResponse(request, "all_users.html", {
        "users": user_data,
    })