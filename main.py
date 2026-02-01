import uvicorn
from fastapi import FastAPI
from logging import Logger
from pydantic import BaseModel

class Code(BaseModel):
    code: str

logger = Logger("Info")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/fix")
def fix_llm(payload: Code):
    logger.info("Fix code")
    print("Fixing code")
    return {
        "explanation": "It looks like you have a syntax error. I added a missing semicolon.",
        "fix": payload.code.strip() + "; // Fixed by Debugger Extension"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)