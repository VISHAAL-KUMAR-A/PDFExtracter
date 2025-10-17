# Backend API - PDF Extraction Tool

FastAPI backend for PDF data extraction using Google Gemini LLM.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## 📁 Project Structure

```
Backend/
├── main.py                 # FastAPI application and routes
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (Gemini API key)
├── services/
│   ├── __init__.py
│   ├── pdf_extractor.py    # PDF text extraction service
│   ├── llm_service.py      # Gemini LLM integration
│   └── excel_generator.py  # Excel file generation service
├── uploads/                # Temporary file storage (auto-created)
└── outputs/                # Generated Excel files (auto-created)
```

## 🔧 Services

### PDF Extractor (`pdf_extractor.py`)
- Extracts text from PDF files using pdfplumber
- Handles tables and multi-page documents
- Returns structured text with page numbers

### LLM Service (`llm_service.py`)
- Integrates with Google Gemini 1.5 Flash
- Processes extracted text according to selected template
- Returns structured JSON data

### Excel Generator (`excel_generator.py`)
- Converts structured data to Excel format
- Creates multiple tabs based on template
- Applies formatting and styling

## 🛠️ API Endpoints

See main README.md for detailed API documentation.

## ⚙️ Configuration

Set environment variables in `.env`:
```env
GEMINI_API_KEY=your_api_key_here
```

## 📦 Dependencies

- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `pdfplumber`: PDF extraction
- `openpyxl`: Excel generation
- `pandas`: Data manipulation
- `google-generativeai`: Gemini API
- `python-dotenv`: Environment management
- `python-multipart`: File upload handling

## 🧪 Testing the API

### Using cURL:
```bash
curl -X POST "http://localhost:8000/extract" \
  -F "files=@test.pdf" \
  -F "template_id=template1" \
  --output result.xlsx
```

### Using Python requests:
```python
import requests

with open('test.pdf', 'rb') as f:
    files = {'files': f}
    data = {'template_id': 'template1'}
    response = requests.post(
        'http://localhost:8000/extract',
        files=files,
        data=data
    )

with open('result.xlsx', 'wb') as out:
    out.write(response.content)
```

## 📝 Notes

- Uploaded files are temporarily stored and cleaned up after processing
- Generated Excel files are stored in `outputs/` directory
- The API supports multiple file uploads in a single request

