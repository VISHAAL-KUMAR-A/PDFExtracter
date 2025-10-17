# Frontend - PDF Extraction Tool

React frontend application for the PDF Extraction Tool. Built with Vite for fast development and optimized production builds.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Run development server:**
   ```bash
   npm run dev
   ```

The app will be available at `http://localhost:5173`

## 📁 Project Structure

```
Frontend/my-react-app/
├── src/
│   ├── App.jsx                      # Main application component
│   ├── App.css                      # Global styles
│   ├── main.jsx                     # Application entry point
│   ├── index.css                    # Base styles
│   └── components/
│       ├── FileUpload.jsx           # File upload component
│       ├── FileUpload.css
│       ├── TemplateSelector.jsx     # Template selection component
│       ├── TemplateSelector.css
│       ├── ExtractionStatus.jsx     # Status display component
│       └── ExtractionStatus.css
├── public/
├── index.html
├── package.json
└── vite.config.js
```

## 🎨 Components

### App.jsx
Main application component that orchestrates the entire workflow:
- Manages application state
- Handles file upload and extraction process
- Coordinates communication with backend API

### FileUpload.jsx
File upload interface with drag-and-drop support:
- Multiple file selection
- Drag-and-drop functionality
- File list display with remove option
- PDF validation

### TemplateSelector.jsx
Template selection interface:
- Displays available extraction templates
- Radio button selection
- Template descriptions
- Fetches templates from backend API

### ExtractionStatus.jsx
Status and error display component:
- Shows extraction progress
- Displays success/error messages
- Animated status updates

## 🛠️ Available Scripts

```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run ESLint
npm run lint
```

## 📦 Dependencies

```json
{
  "react": "^19.1.1",
  "react-dom": "^19.1.1",
  "axios": "^1.6.5"
}
```

## 🎨 Styling

The application uses:
- Modern CSS3 with gradients and animations
- Responsive design for mobile and desktop
- Custom component-specific stylesheets
- Flexbox and Grid layouts

### Color Scheme
- Primary: `#667eea` to `#764ba2` (gradient)
- Success: `#4caf50`
- Error: `#f44336`
- Info: `#2196f3`

## 🔧 Configuration

### Backend API URL
Update the API URL in components if backend is hosted elsewhere:

```javascript
// In App.jsx and TemplateSelector.jsx
const API_URL = 'http://localhost:8000';
```

### Vite Configuration
Modify `vite.config.js` for custom build settings:

```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

## 🌐 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## 📱 Responsive Design

The application is fully responsive and supports:
- Desktop (1920x1080 and above)
- Tablet (768px - 1024px)
- Mobile (320px - 767px)

## 🧪 Testing

### Manual Testing Checklist
- [ ] Upload single PDF file
- [ ] Upload multiple PDF files
- [ ] Drag and drop files
- [ ] Switch between templates
- [ ] Remove uploaded files
- [ ] Extract data successfully
- [ ] Download generated Excel file
- [ ] Handle errors gracefully

## 🚀 Production Build

Build the application for production:

```bash
npm run build
```

The optimized files will be in the `dist/` directory.

### Deploy to Static Hosting

The built application can be deployed to:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront
- Any static hosting service

## 🐛 Common Issues

**Issue:** Cannot connect to backend
- Ensure backend is running on port 8000
- Check CORS configuration in backend

**Issue:** Files not uploading
- Check file size limits
- Ensure files are PDF format
- Check browser console for errors

**Issue:** Download not working
- Ensure backend is returning correct file type
- Check browser download settings

## 📝 Development Notes

- Uses React 19 with latest features
- Vite for fast HMR (Hot Module Replacement)
- No external UI library dependencies (custom components)
- Fetch API for HTTP requests
- Modern JavaScript (ES6+)

## 🎯 Future Enhancements

Potential improvements:
- Upload progress indicator
- File size validation before upload
- Preview extracted data before download
- History of previous extractions
- Batch processing queue
- WebSocket for real-time progress updates
