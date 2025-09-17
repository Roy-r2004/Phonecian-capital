#!/usr/bin/env python3
"""
FastAPI Web Interface for TAM Estimation Prompt Testing Agent
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
from datetime import datetime
from typing import List, Optional
import asyncio
import threading

from tam_qwen_agent import QwenTAMAgent, PromptTestResult
from dcf_agent import DCFAgent, DCFTestResult
from config import QWEN_CONFIG, GEMINI_CONFIG, AVAILABLE_MODELS, TEST_COMPANIES

app = FastAPI(title="TAM Prompt Testing Agent", version="1.0.0")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="templates"), name="static")

# Initialize the TAM agent
agent = QwenTAMAgent(
    api_key=QWEN_CONFIG["api_key"],
    base_url=QWEN_CONFIG["base_url"],
    model=QWEN_CONFIG["model"]
)

# Initialize the DCF agent (default to Qwen)
dcf_agent = DCFAgent(
    api_key=QWEN_CONFIG["api_key"],
    base_url=QWEN_CONFIG["base_url"],
    model=QWEN_CONFIG["model"]
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with TAM testing interface"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "test_companies": TEST_COMPANIES,
        "available_models": AVAILABLE_MODELS,
        "current_model": "qwen"
    })

@app.get("/dcf", response_class=HTMLResponse)
async def dcf_home(request: Request):
    """DCF testing interface"""
    return templates.TemplateResponse("dcf.html", {
        "request": request,
        "available_models": AVAILABLE_MODELS,
        "current_model": "qwen"
    })

@app.post("/test-single")
async def test_single_prompt(
    company_context: str = Form(...),
    model_choice: str = Form("qwen"),
    verbose: bool = Form(False)
):
    """Test TAM prompt with a single company context"""
    try:
        # Get the selected model configuration
        if model_choice not in AVAILABLE_MODELS:
            raise HTTPException(status_code=400, detail="Invalid model selection")
        
        model_config = AVAILABLE_MODELS[model_choice]
        
        # Update the global agent with selected model
        agent.api_key = model_config["api_key"]
        agent.base_url = model_config["base_url"]
        agent.model = model_config["model"]
        
        # Run test in a separate thread with timeout to avoid blocking
        result = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(
                None, agent.test_prompt, company_context
            ),
            timeout=60  # 1 minute timeout
        )
        
        return JSONResponse({
            "success": True,
            "result": {
                "test_id": result.test_id,
                "timestamp": result.timestamp.isoformat(),
                "quality_score": result.quality_score,
                "response_length": len(result.response),
                "validation_scores": result.validation_scores,
                "missing_requirements": result.missing_requirements,
                "recommendations": result.recommendations,
                "market_metrics": result.market_metrics,
                "response_preview": result.response,
                "model_used": model_choice
            }
        })
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout - TAM analysis is taking too long to respond. Please try again.")
    except Exception as e:
        print(f"Error in test_single_prompt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"TAM analysis failed: {str(e)}")

@app.post("/test-dcf")
async def test_dcf_prompt(
    company_context: str = Form(...),
    model_choice: str = Form("qwen"),
    verbose: bool = Form(False)
):
    """Test DCF prompt with AI model"""
    try:
        # Get the selected model configuration
        if model_choice not in AVAILABLE_MODELS:
            raise HTTPException(status_code=400, detail="Invalid model selection")
        
        model_config = AVAILABLE_MODELS[model_choice]
        
        # Update the DCF agent with selected model
        dcf_agent.api_key = model_config["api_key"]
        dcf_agent.base_url = model_config["base_url"]
        dcf_agent.model = model_config["model"]
        
        # Run DCF test in a separate thread with timeout
        result = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(
                None, dcf_agent.test_prompt, company_context
            ),
            timeout=90  # 1.5 minute timeout for DCF analysis
        )
        
        return JSONResponse({
            "success": True,
            "result": {
                "test_id": result.test_id,
                "timestamp": result.timestamp.isoformat(),
                "quality_score": result.quality_score,
                "response_length": len(result.response),
                "validation_scores": result.validation_scores,
                "missing_requirements": result.missing_requirements,
                "recommendations": result.recommendations,
                "financial_metrics": result.financial_metrics,
                "response_preview": result.response,
                "model_used": model_choice
            }
        })
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timeout - DCF analysis is taking too long to respond. Please try again.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results/{test_id}")
async def get_test_result(test_id: str):
    """Get detailed results for a specific test"""
    try:
        # Find the test result
        result = None
        for test_result in agent.test_results:
            if test_result.test_id == test_id:
                result = test_result
                break
        
        if not result:
            raise HTTPException(status_code=404, detail="Test result not found")
        
        return JSONResponse({
            "success": True,
            "result": {
                "test_id": result.test_id,
                "timestamp": result.timestamp.isoformat(),
                "prompt_used": result.prompt_used,
                "response": result.response,
                "quality_score": result.quality_score,
                "validation_scores": result.validation_scores,
                "missing_requirements": result.missing_requirements,
                "recommendations": result.recommendations
            }
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export-results")
async def export_results():
    """Export all TAM test results as JSON"""
    try:
        data = []
        for result in agent.test_results:
            data.append({
                "test_id": result.test_id,
                "timestamp": result.timestamp.isoformat(),
                "quality_score": result.quality_score,
                "validation_scores": result.validation_scores,
                "missing_requirements": result.missing_requirements,
                "recommendations": result.recommendations,
                "market_metrics": result.market_metrics,
                "response_length": len(result.response)
            })
        
        return JSONResponse({
            "success": True,
            "export_timestamp": datetime.now().isoformat(),
            "total_tests": len(data),
            "results": data
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export-dcf-results")
async def export_dcf_results():
    """Export all DCF test results as JSON"""
    try:
        data = []
        for result in dcf_agent.test_results:
            data.append({
                "test_id": result.test_id,
                "timestamp": result.timestamp.isoformat(),
                "quality_score": result.quality_score,
                "validation_scores": result.validation_scores,
                "missing_requirements": result.missing_requirements,
                "recommendations": result.recommendations,
                "financial_metrics": result.financial_metrics,
                "response_length": len(result.response)
            })
        
        return JSONResponse({
            "success": True,
            "export_timestamp": datetime.now().isoformat(),
            "total_dcf_tests": len(data),
            "results": data
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "model": QWEN_CONFIG["model"],
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
