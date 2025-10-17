import './ExtractionStatus.css'

function ExtractionStatus({ status, error }) {
  if (!status && !error) {
    return null
  }

  return (
    <div className="extraction-status">
      {error && (
        <div className="status-message error">
          <span className="status-icon">❌</span>
          <div>
            <strong>Error:</strong> {error}
          </div>
        </div>
      )}

      {status && (
        <div className={`status-message ${status.includes('✓') ? 'success' : 'info'}`}>
          <span className="status-icon">
            {status.includes('✓') ? '✅' : '⏳'}
          </span>
          <div>{status}</div>
        </div>
      )}
    </div>
  )
}

export default ExtractionStatus

