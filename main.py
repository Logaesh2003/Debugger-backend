import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from logging import Logger
from pydantic import BaseModel
from agents.code_fixer import fix_code

class Code(BaseModel):
    code: str

logger = Logger("Info")

app = FastAPI(
    title="Debugger Backend",
    description="AI-powered code debugging and fixing service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "Debugger Backend is running"}

@app.post("/fix")
def fix_llm(payload: Code):
    """
    Receive error code from the extension, send to LLM, and return fixed code with explanation.
    
    Request Body:
        code: The code that needs to be fixed
        
    Response:
        explanation: Description of what was wrong and how it was fixed
        fix: The corrected code
    """
    logger.info("Received code fix request")
    print(f"Fixing code: {payload.code[:100]}...")  # Log first 100 chars
    
    try:
        result = fix_code(payload.code)
        return result
    except Exception as e:
        logger.error(f"Error fixing code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)