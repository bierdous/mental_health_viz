# mental_health_viz
Visualization of a mental health dataset for the Visualization course at FI MUNI

**Deployed at:** https://mental-health-viz.onrender.com/

# Local Deployment Guide
## Prerequisites
- Python 3.9 or higher installed
- Git installed

## 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

## 2. Create a Virtual Environment (only once)
```bash
python -m venv venv
```

## 3. Activate the Virtual Environment (at each terminal launch)
- **Linux/Mac:**
```bash
source venv/bin/activate
```
- **Windows:**
```bash
venv\Scripts\activate
```

## 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## 5. Run the App
```bash
python app.py
```
The app will start on `http://127.0.0.1:8050`.

## 6. (Optional) Test Production Setup
Render uses Gunicorn in production. You can test locally:
```bash
gunicorn app:server --bind 0.0.0.0:8080
```
Visit `http://localhost:8080`.

## 7. Update Dependencies for Collaboration
If you add or update packages, regenerate `requirements.txt`:
```bash
pip freeze > requirements.txt
```
Commit and push the updated file so your collaborator can sync.

## Notes
- Always activate the virtual environment before running the app.
- Do **NOT** commit the `venv` folder. Use `.gitignore` to exclude it.
