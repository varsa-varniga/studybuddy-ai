from fastapi import FastAPI

app = FastAPI(title="StudyBuddy AI Backend")

@app.get("/")
def home():
    return {"message": "Backend is running "}