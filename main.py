from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from automation import run_automation

app = FastAPI(title="JobHunter Auto-Apply API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AutomationRequest(BaseModel):
    keywords: str

@app.get("/")
def read_root():
    return {"status": "ONLINE", "service": "JobHunter Auto-Apply CORE"}

@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    # In a real scenario, we save the file to use in Selenium
    return {"filename": file.filename, "status": "UPLOAD_SUCCESSFUL"}

@app.post("/start-automation")
async def start_automation(req: AutomationRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_automation, req.keywords)
    return {"status": "AUTOMATION_INITIATED", "keywords": req.keywords}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
