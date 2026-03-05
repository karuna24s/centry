"""
This is the main entry point for the application.
Purpose: The entry point. Like application.rb and routes.rb combined.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.ai_logic import CentryBrain
from app.services.security_logic import SecurityScanner
import os

# 1. Initialize the App and Services
app = FastAPI(title="Centry Infrastructure Auditor")
brain = CentryBrain()
security_auditor = SecurityScanner()

# 2. Define Data Models
class AnalysisRequest(BaseModel):
    content: str
    context: str = "Generic Codebase"

# 3. Health Check (The "Ping" for your browser)
@app.get("/health")
async def health_check():
    return {"status": "Centry is online", "version": "1.0.1"}

# 4. The Core Logic: The "Analyze" Endpoint
@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    try:
        # Pass 1: Local Python Security Scan (Fast & Precise)
        security_findings = security_auditor.scan_content(request.content)

        # Pass 2: LLM Architectural Scan (Nuanced & Strategic)
        # This handles the N+1, Sidekiq, and scaling logic
        ai_feedback = brain.analyze_infrastructure(request.content, request.context)

        # Combine the Reports
        final_report = f"### 🏛️ Centry Architectural Audit\n\n{ai_feedback}\n\n"

        if security_findings:
            final_report += "--- 🛑 SECURITY ALERTS ---\n"
            final_report += "\n".join(security_findings)
        else:
            final_report += "--- ✅ No Hardcoded Secrets Detected ---"

        return {"analysis": final_report}

    except Exception as e:
        # Logging the error for the Uvicorn terminal
        print(f"Error during analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)