from fastapi import FastAPI

app = FastAPI(title="Autonomous PM Agent API")

@app.get("/")
def health_check():
    return {"status": "Backend is running"}
