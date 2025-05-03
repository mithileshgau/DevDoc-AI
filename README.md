# DevDoc AI

DevDoc AI is a web-based application designed to generate high-quality documentation for source code files. It leverages advanced AI models to analyze code and produce detailed, structured documentation in Markdown format. The application supports multiple programming languages and provides an intuitive interface for uploading files, previewing documentation, and downloading it as a Markdown file.

## Features

- **Multi-language Support**: Automatically detects programming languages based on file extensions and generates language-specific documentation.
- **Code Chunking**: Handles large files by splitting them into manageable chunks for documentation generation.
- **AI-Powered Documentation**: Uses the Gemini API to generate accurate and structured documentation.
- **Web Interface**: Upload multiple files, preview generated documentation, and download it as a Markdown file.
- **Customizable Styles**: Frontend styled with modern CSS for a clean and responsive user experience.

## Project Structure

### Backend

The backend is built with Flask and provides APIs for processing uploaded files and generating documentation.

- **`app.py`**: Entry point for the Flask application. Configures routes and CORS settings.
- **`routes/upload.py`**: Handles file uploads and invokes the documentation generation service.
- **`services/`**: Contains core logic for documentation generation, code chunking, and language detection.
    - **`documentation.py`**: Main service for generating documentation.
    - **`code_chunking.py`**: Splits large code files into chunks for processing.
    - **`get_language_prompt.py`**: Determines the programming language based on file extensions.
    - **`load_prompt.py`**: Loads prompt templates for AI-based documentation generation.
- **`prompts/documentation_prompt.txt`**: Template for generating structured documentation.
- **`config.py`**: Configuration file for environment variables and application settings.
- **`requirements.txt`**: Lists Python dependencies.

### Frontend

The frontend is a React-based application that provides a user-friendly interface for interacting with the backend.

- **`src/App.js`**: Main application component that handles file uploads and displays generated documentation.
- **`src/components/`**: Contains reusable components like `FileUpload`, `DocumentationAccordion`, and `MarkdownPreview`.
- **`src/utils/`**: Utility functions, including `downloadMarkdown.js` for downloading documentation.
- **`src/styles/`**: Custom styles for the application.
- **`public/`**: Static files, including `index.html` and `manifest.json`.

## Installation

### Prerequisites

- Python 3.10+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file: `API_KEY=<your_gemini_api_key>`
4. Run the Flask server: `python app.py`

### Frontend Setup

1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm start`

## Usage

1. Start both the backend and frontend servers.
2. Open the frontend in your browser at `http://localhost:3000`.
3. Upload one or more source code files.
4. Preview the generated documentation in the accordion interface.
5. Download the documentation as a Markdown file.

## Supported Languages

- Python
- JavaScript/TypeScript
- Java
- Go
- Ruby
- C#
- PHP
- And more...

## Limitations

- Requires an active API key for the Gemini API.
- Large files may take longer to process due to chunking and API response times.