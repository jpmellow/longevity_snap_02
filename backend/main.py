from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Longevity Snap Backend API is running!"}
