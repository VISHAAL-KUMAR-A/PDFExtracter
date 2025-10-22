# 📄 PDF Extraction Tool Using LLM

A powerful web application that extracts structured data from PDF files using AI (OpenAI GPT-4o-mini) and outputs the results in Excel format. Built with React frontend and FastAPI backend.

## 🎯 Project Overview

This tool allows users to:
- Upload single or multiple PDF files
- Select between two extraction templates for Private Equity Fund documents
- Process PDFs using OpenAI GPT-4o-mini for intelligent data extraction
- Download extracted data as formatted Excel (.xlsx) files

## 🏗️ Architecture

```
PDFExtraction/
├── Backend/                    # FastAPI backend
│   ├── main.py                # Main API application
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   └── services/              # Service modules
│       ├── pdf_extractor.py   # PDF text extraction
│       ├── llm_service.py     # OpenAI LLM integration
│       └── excel_generator.py # Excel file generation
│
├── Frontend/                  # React frontend
│   └── my-react-app/         # Vite + React application
│       ├── src/
│       │   ├── App.jsx       # Main application component
│       │   ├── components/   # React components
│       │   └── ...
│       └── package.json      # Node dependencies
│
├── templates/                 # Template documentation
│   ├── Template_1_Description.md
│   └── Template_2_Description.md
│
├── examples/                  # Sample files
│   ├── sample_pdfs/          # Test PDF files
│   └── output/               # Example Excel outputs
│
└── README.md                  # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Git

### Backend Setup

1. **Navigate to the Backend directory:**
   ```bash
   cd Backend
   ```

2. **Create a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   The `.env` file is already created with the OpenAI API key. If you need to change it:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the backend server:**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the Frontend directory:**
   ```bash
   cd Frontend/my-react-app
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```
   
   The frontend will be available at `http://localhost:5173`

## 📖 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy"
}
```

#### 2. Get Available Templates
```http
GET /templates
```
**Response:**
```json
{
  "templates": [
    {
      "id": "template1",
      "name": "Template 1 - Private Equity Funds (Detailed)",
      "description": "Extracts fund and investment vehicle information..."
    },
    {
      "id": "template2",
      "name": "Template 2 - Private Equity Funds (Executive)",
      "description": "Extracts executive portfolio summary..."
    }
  ]
}
```

#### 3. Extract Data from PDFs
```http
POST /extract
```

**Request:**
- Content-Type: `multipart/form-data`
- Body Parameters:
  - `files`: One or more PDF files (required)
  - `template_id`: Either `"template1"` or `"template2"` (required)

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/extract" \
  -F "files=@document1.pdf" \
  -F "files=@document2.pdf" \
  -F "template_id=template1" \
  --output extracted_data.xlsx
```

**Example using Python:**
```python
import requests

files = [
    ('files', open('document1.pdf', 'rb')),
    ('files', open('document2.pdf', 'rb'))
]
data = {'template_id': 'template1'}

response = requests.post(
    'http://localhost:8000/extract',
    files=files,
    data=data
)

with open('extracted_data.xlsx', 'wb') as f:
    f.write(response.content)
```

**Response:**
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Body: Excel file (binary)

**Error Responses:**
```json
{
  "detail": "Invalid template_id. Must be 'template1' or 'template2'"
}
```

## 🎯 Extraction Templates

### Template 1: Private Equity Funds (Detailed)

Extracts comprehensive information including:
- Fund and Investment Vehicle Information
- Fund Manager Details
- Financial Position
- LP Investor Cashflows
- Fund Companies
- Company Valuations
- Company Financials
- Investment History

**Excel Output Tabs:**
1. Fund Information
2. Fund Manager
3. Financial Position
4. LP Investors
5. Fund Companies
6. Company Valuations
7. Company Financials
8. Investment History

See [Template 1 Description](templates/Template_1_Description.md) for detailed field specifications.

### Template 2: Private Equity Funds (Executive)

Extracts executive-level information including:
- Executive Portfolio Summary
- Schedule of Investments
- Statement of Operations
- Statement of Cashflows
- PCAP Statement
- Portfolio Companies Profile
- Portfolio Companies Financials
- Footnotes

**Excel Output Tabs:**
1. Executive Summary
2. Schedule of Investments
3. Operations Statement
4. Cashflow Statement
5. PCAP Statement
6. Portfolio Companies
7. Portfolio Financials
8. Footnotes

See [Template 2 Description](templates/Template_2_Description.md) for detailed field specifications.

## 🔄 How to Switch Between Templates

### In the Frontend (UI):
1. Open the application at `http://localhost:5173`
2. Select the desired template using the radio buttons
3. Upload your PDF files
4. Click "Extract Data"

### Using the API:
Simply change the `template_id` parameter in your request:
- Use `"template1"` for Template 1
- Use `"template2"` for Template 2

## 🧪 Testing

### Using the Web Interface

1. Start both backend and frontend servers
2. Open `http://localhost:5173` in your browser
3. Select a template
4. Upload test PDF files from the `examples/sample_pdfs/` directory
5. Click "Extract Data"
6. Download and review the generated Excel file

### Using API Testing Tools

**Postman:**
1. Create a new POST request to `http://localhost:8000/extract`
2. Select "Body" → "form-data"
3. Add key `files` (type: File) and select PDF file(s)
4. Add key `template_id` (type: Text) with value `template1` or `template2`
5. Click "Send"
6. Save the response as an .xlsx file

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **pdfplumber**: PDF text and table extraction
- **openai**: OpenAI GPT-4o-mini integration
- **openpyxl**: Excel file generation
- **python-dotenv**: Environment variable management

### Frontend
- **React**: UI library
- **Vite**: Build tool and dev server
- **CSS3**: Styling with modern features

### AI Model
- **OpenAI GPT-4o-mini**: For intelligent data extraction

## 📋 Features

### Backend Features
- ✅ RESTful API with FastAPI
- ✅ Multiple PDF file processing
- ✅ Intelligent text extraction with table detection
- ✅ LLM-based structured data extraction
- ✅ Formatted Excel file generation with multiple tabs
- ✅ CORS support for frontend integration
- ✅ Error handling and validation

### Frontend Features
- ✅ Modern, responsive UI design
- ✅ Drag-and-drop file upload
- ✅ Multiple file selection
- ✅ Template selection interface
- ✅ Real-time extraction status
- ✅ Automatic file download
- ✅ Error handling and user feedback

## 🔧 Configuration

### Environment Variables

Create or modify `Backend/.env`:
```env
OPEN_API_KEY=your_open_api_key
```

### CORS Configuration

Modify `Backend/main.py` to add allowed origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📝 Sample Data

Place your test PDF files in:
```
examples/sample_pdfs/
```

Generated Excel files will be available in:
```
Backend/outputs/
```

## 🐛 Troubleshooting

### Backend Issues

**Issue:** Module not found errors
```bash
# Solution: Ensure virtual environment is activated and dependencies are installed
pip install -r requirements.txt
```

**Issue:** OpenAI API errors
```bash
# Solution: Check your API key in .env file
# Ensure the API key has proper permissions
```

**Issue:** Port 8000 already in use
```bash
# Solution: Change the port in main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Frontend Issues

**Issue:** Cannot connect to backend
```bash
# Solution: Ensure backend is running on port 8000
# Check CORS configuration in backend
```

**Issue:** Build errors
```bash
# Solution: Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🚀 Deployment

### Backend Deployment

For production deployment, consider:
- Using Gunicorn with Uvicorn workers
- Setting up proper environment variables
- Implementing rate limiting
- Adding authentication
- Using a production database for logging

### Frontend Deployment

Build the production version:
```bash
cd Frontend/my-react-app
npm run build
```

The built files will be in the `dist/` directory.

## 📄 License

This project is created as an internship task.

## 👥 Credits

- **LLM**: OpenAI GPT-4o-mini
- **PDF Processing**: pdfplumber
- **Excel Generation**: openpyxl
- **Frontend**: React + Vite
- **Backend**: FastAPI

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Check the logs in the backend console

---

**Note:** This tool is designed for Private Equity Fund document extraction. The accuracy of extraction depends on the quality and structure of the input PDF files. Uses OpenAI GPT-4o-mini for reliable and fast data extraction.

