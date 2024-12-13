# NIST AI Security Assessment Tool

An automated security assessment tool that analyzes documents against the NIST Cybersecurity Framework using AI. The tool provides detailed security analysis, risk assessment, and actionable recommendations.

## Features

- PDF document analysis using PyMuPDF
- NIST Framework scoring across all five core functions (Identify, Protect, Detect, Respond, Recover)
- Detailed security risk and gap analysis
- Prioritized recommendations with implementation complexity
- Support for both file upload and URL-based PDF processing
- FastAPI backend with full CORS support

## Prerequisites

- Python 3.8+
- OpenAI API key
- Required Python packages (see Installation)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd nist-ai-assessment
```

2. Install required packages:
```bash
pip install fastapi uvicorn pymupdf llama-index openai requests
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Project Structure

```
├── main.py           # FastAPI application and endpoints
├── analysis.py       # Core analysis logic and NIST framework assessment
├── reader.py         # PDF document processing
├── nistai_prompt.py  # System prompts for AI analysis
```

## Usage

1. Start the server:
```bash
python main.py
```

2. The server will start on `http://0.0.0.0:8080` with two main endpoints:

- `/nistai` - Upload PDF file directly
- `/nistai_url` - Analyze PDF from URL

## API Endpoints

### POST /nistai
Upload a PDF file for analysis:
```bash
curl -X POST -F "file=@document.pdf" http://localhost:8080/nistai
```

### POST /nistai_url
Analyze a PDF from URL:
```bash
curl -X POST -d "pdf_url=https://example.com/document.pdf" http://localhost:8080/nistai_url
```

## Response Format

The tool returns a JSON response with:
- Executive Summary
- Security Risks Analysis
- Security Gaps Assessment
- NIST Framework Scores (1-5 scale)
- Prioritized Recommendations

## Error Handling

The application includes comprehensive error handling for:
- Invalid file formats
- URL access issues
- Processing errors
- API failures

## Logging

Detailed logging is implemented with both console and file output (nistai.log).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.



This README provides a comprehensive overview of your project, including installation instructions, usage examples, and project structure. Feel free to modify any sections to better match your specific needs or add additional information as required.

