import { useState } from 'react'
import './App.css'
import FileUpload from './components/FileUpload'
import TemplateSelector from './components/TemplateSelector'
import ExtractionStatus from './components/ExtractionStatus'

function App() {
  const [selectedFiles, setSelectedFiles] = useState([])
  const [selectedTemplate, setSelectedTemplate] = useState('template1')
  const [isProcessing, setIsProcessing] = useState(false)
  const [extractionStatus, setExtractionStatus] = useState(null)
  const [error, setError] = useState(null)

  const handleFilesSelected = (files) => {
    setSelectedFiles(files)
    setError(null)
    setExtractionStatus(null)
  }

  const handleTemplateChange = (templateId) => {
    setSelectedTemplate(templateId)
  }

  const handleExtract = async () => {
    if (selectedFiles.length === 0) {
      setError('Please select at least one PDF file')
      return
    }

    setIsProcessing(true)
    setError(null)
    setExtractionStatus('Uploading files...')

    const formData = new FormData()
    selectedFiles.forEach(file => {
      formData.append('files', file)
    })
    formData.append('template_id', selectedTemplate)

    try {
      setExtractionStatus('Processing PDFs with AI...')
      
      const response = await fetch('http://localhost:8000/extract', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Extraction failed')
      }

      setExtractionStatus('Generating Excel file...')
      
      // Get the blob from response
      const blob = await response.blob()
      
      // Create download link
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `extracted_data_${Date.now()}.xlsx`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)

      setExtractionStatus('✓ Extraction completed successfully!')
      setSelectedFiles([])
    } catch (err) {
      setError(err.message || 'An error occurred during extraction')
      setExtractionStatus(null)
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>📄 PDF Extraction Tool</h1>
        <p className="subtitle">Extract structured data from PDF files using AI</p>
      </header>

      <main className="app-main">
        <div className="extraction-container">
          <TemplateSelector
            selectedTemplate={selectedTemplate}
            onTemplateChange={handleTemplateChange}
            disabled={isProcessing}
          />

          <FileUpload
            onFilesSelected={handleFilesSelected}
            selectedFiles={selectedFiles}
            disabled={isProcessing}
          />

          <button
            className="extract-button"
            onClick={handleExtract}
            disabled={isProcessing || selectedFiles.length === 0}
          >
            {isProcessing ? '⏳ Processing...' : '🚀 Extract Data'}
          </button>

          <ExtractionStatus
            status={extractionStatus}
            error={error}
          />
        </div>
      </main>

      <footer className="app-footer">
        <p>Powered by Gemini AI | Built with React & FastAPI</p>
      </footer>
    </div>
  )
}

export default App
