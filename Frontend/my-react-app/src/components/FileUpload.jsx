import { useRef } from 'react'
import './FileUpload.css'

function FileUpload({ onFilesSelected, selectedFiles, disabled }) {
  const fileInputRef = useRef(null)

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files)
    onFilesSelected(files)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    if (disabled) return
    
    const files = Array.from(e.dataTransfer.files).filter(
      file => file.type === 'application/pdf'
    )
    if (files.length > 0) {
      onFilesSelected(files)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  const handleClick = () => {
    if (!disabled) {
      fileInputRef.current?.click()
    }
  }

  const removeFile = (index) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index)
    onFilesSelected(newFiles)
  }

  return (
    <div className="file-upload-section">
      <h2>📁 Upload PDF Files</h2>
      
      <div
        className={`upload-area ${disabled ? 'disabled' : ''}`}
        onClick={handleClick}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          multiple
          onChange={handleFileChange}
          disabled={disabled}
          style={{ display: 'none' }}
        />
        
        <div className="upload-icon">📤</div>
        <p className="upload-text">
          Click to browse or drag & drop PDF files here
        </p>
        <p className="upload-hint">Supports multiple files</p>
      </div>

      {selectedFiles.length > 0 && (
        <div className="selected-files">
          <h3>Selected Files ({selectedFiles.length})</h3>
          <ul className="file-list">
            {selectedFiles.map((file, index) => (
              <li key={index} className="file-item">
                <span className="file-icon">📄</span>
                <span className="file-name">{file.name}</span>
                <span className="file-size">
                  ({(file.size / 1024 / 1024).toFixed(2)} MB)
                </span>
                {!disabled && (
                  <button
                    className="remove-button"
                    onClick={() => removeFile(index)}
                    title="Remove file"
                  >
                    ✕
                  </button>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default FileUpload

