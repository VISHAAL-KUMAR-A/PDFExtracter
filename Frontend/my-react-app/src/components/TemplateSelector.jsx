import { useState, useEffect } from 'react'
import './TemplateSelector.css'

function TemplateSelector({ selectedTemplate, onTemplateChange, disabled }) {
  const [templates, setTemplates] = useState([
    {
      id: 'template1',
      name: 'Template 1 - Private Equity Funds (Detailed)',
      description: 'Extracts fund and investment vehicle information, fund manager details, financial positions, LP cashflows, and company investments'
    },
    {
      id: 'template2',
      name: 'Template 2 - Private Equity Funds (Executive)',
      description: 'Extracts executive portfolio summary, schedule of investments, statements of operations, cashflows, PCAP statements, and portfolio company profiles'
    }
  ])

  useEffect(() => {
    // Optionally fetch templates from backend
    fetch('http://localhost:8000/templates')
      .then(res => res.json())
      .then(data => {
        if (data.templates) {
          setTemplates(data.templates)
        }
      })
      .catch(err => {
        console.log('Using default templates')
      })
  }, [])

  return (
    <div className="template-selector-section">
      <h2>🎯 Select Extraction Template</h2>
      <div className="template-options">
        {templates.map((template) => (
          <div
            key={template.id}
            className={`template-card ${selectedTemplate === template.id ? 'selected' : ''} ${disabled ? 'disabled' : ''}`}
            onClick={() => !disabled && onTemplateChange(template.id)}
          >
            <div className="template-header">
              <input
                type="radio"
                name="template"
                value={template.id}
                checked={selectedTemplate === template.id}
                onChange={() => onTemplateChange(template.id)}
                disabled={disabled}
              />
              <h3>{template.name}</h3>
            </div>
            <p className="template-description">{template.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default TemplateSelector

