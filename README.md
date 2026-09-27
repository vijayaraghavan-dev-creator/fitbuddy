# FitBuddy - AI Fitness Plan Generator

## Setup
1. Create and activate a virtual environment:
   python -m venv fitbuddy-env
   fitbuddy-env\Scripts\activate      (Windows)
   source fitbuddy-env/bin/activate   (Mac/Linux)

2. Install dependencies:
   pip install -r requirements.txt

3. Add your Gemini API key:
   Copy .env.example to .env and fill in GOOGLE_API_KEY.

4. (Optional) Add a background image at app/static/images/gym-bg.jpg

5. Run the server:
   uvicorn app.main:app --reload

6. Visit:
   http://127.0.0.1:8000        - main app
   http://127.0.0.1:8000/docs   - interactive API docs
   http://127.0.0.1:8000/view-all-users - admin dashboard
