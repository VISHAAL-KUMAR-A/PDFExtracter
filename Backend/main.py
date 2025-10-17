from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from typing import List
import uuid
from pathlib import Path

from services.pdf_extractor import PDFExtractor
from services.llm_service import LLMService
from services.excel_generator import ExcelGenerator

app = FastAPI(title="PDF Extraction API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize services
pdf_extractor = PDFExtractor()
llm_service = LLMService()
excel_generator = ExcelGenerator()


@app.get("/")
async def root():
    return {
        "message": "PDF Extraction API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "extract": "/extract (POST)",
            "templates": "/templates (GET)"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/templates")
async def get_templates():
    """Get available extraction templates"""
    return {
        "templates": [
            {
                "id": "template1",
                "name": "Template 1 - Private Equity Funds (Detailed)",
                "description": "Extracts fund and investment vehicle information, fund manager details, financial positions, LP cashflows, and company investments"
            },
            {
                "id": "template2",
                "name": "Template 2 - Private Equity Funds (Executive)",
                "description": "Extracts executive portfolio summary, schedule of investments, statements of operations, cashflows, PCAP statements, and portfolio company profiles"
            }
        ]
    }


@app.post("/extract")
async def extract_pdf(
    files: List[UploadFile] = File(...),
    template_id: str = Form(...)
):
    """
    Extract data from PDF files using selected template

    Args:
        files: List of PDF files to process
        template_id: Either 'template1' or 'template2'

    Returns:
        FileResponse: Excel file with extracted data
    """
    if template_id not in ["template1", "template2"]:
        raise HTTPException(
            status_code=400, detail="Invalid template_id. Must be 'template1' or 'template2'")

    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    # Validate file types
    for file in files:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400, detail=f"Invalid file type: {file.filename}. Only PDF files are allowed.")

    # Generate unique session ID
    session_id = str(uuid.uuid4())
    session_dir = UPLOAD_DIR / session_id
    session_dir.mkdir(exist_ok=True)

    try:
        # Save uploaded files
        pdf_paths = []
        for file in files:
            file_path = session_dir / file.filename
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            pdf_paths.append(file_path)

        # Extract text from PDFs
        extracted_texts = []
        for pdf_path in pdf_paths:
            text = pdf_extractor.extract_text(pdf_path)
            extracted_texts.append({
                "filename": pdf_path.name,
                "text": text
            })

        # Process with LLM based on template
        structured_data = llm_service.extract_data(
            extracted_texts, template_id)

        # Generate Excel file
        output_filename = f"extracted_data_{session_id}.xlsx"
        output_path = OUTPUT_DIR / output_filename
        excel_generator.generate_excel(
            structured_data, template_id, output_path)

        # Clean up uploaded files
        shutil.rmtree(session_dir, ignore_errors=True)

        return FileResponse(
            path=output_path,
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        # Clean up on error
        if session_dir.exists():
            shutil.rmtree(session_dir, ignore_errors=True)
        raise HTTPException(
            status_code=500, detail=f"Error processing PDFs: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
