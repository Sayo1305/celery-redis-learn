# Redis Learning Project

A FastAPI application that demonstrates asynchronous PDF generation using Celery with Redis as the message broker and result backend.

## 🚀 Features

- **FastAPI Web Framework**: Modern, fast web framework for building APIs
- **Celery Task Queue**: Asynchronous task processing for PDF generation
- **Redis Integration**: Message broker and result backend for Celery
- **PDF Generation**: Dynamic PDF creation from user data using pdfkit
- **Background Tasks**: Non-blocking PDF generation with task status tracking
- **File Management**: Automatic file cleanup after download

## 📋 Prerequisites

- Python 3.8+
- Redis server
- wkhtmltopdf (for PDF generation)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd redis_learn
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install wkhtmltopdf**
   - **macOS**: `brew install wkhtmltopdf`
   - **Ubuntu/Debian**: `sudo apt-get install wkhtmltopdf`
   - **Windows**: Download from [wkhtmltopdf website](https://wkhtmltopdf.org/downloads.html)

5. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   BROKER_URL=redis://localhost:6379/0
   BACKEND_URL=redis://localhost:6379/0
   ```

6. **Start Redis server**
   ```bash
   redis-server
   ```

## 🚀 Running the Application

1. **Start the Celery worker** (in a separate terminal)
   ```bash
   celery -A app.celery_app worker --loglevel=info
   ```

2. **Start the FastAPI server**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 📚 API Endpoints

### 1. Health Check
- **GET** `/`
- Returns a simple health check message

### 2. Generate PDF
- **POST** `/generate_pdf`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "name": "John Doe",
    "desc": "User description",
    "password": "secure_password"
  }
  ```
- **Response**:
  ```json
  {
    "status": "ok",
    "message": "PDF generation started",
    "task": "task_id_here"
  }
  ```

### 3. Check Task Status
- **GET** `/task_status/{task_id}`
- Returns the current status of a PDF generation task
- **Response**:
  ```json
  {
    "task_id": "task_id_here",
    "status": "SUCCESS",
    "result": "/path/to/generated/file.pdf"
  }
  ```

### 4. Download PDF
- **GET** `/download/{task_id}`
- Downloads the generated PDF file
- Automatically deletes the file after download

## 🔧 Project Structure

```
redis_learn/
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── routes.py        # API route definitions
│   ├── task.py          # Celery task for PDF generation
│   └── celery_app.py    # Celery configuration
├── env/                 # Virtual environment
├── output/              # Generated PDF files (created automatically)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🎯 Usage Example

1. **Start the services**:
   ```bash
   # Terminal 1: Start Redis
   redis-server
   
   # Terminal 2: Start Celery worker
   celery -A app.celery_app worker --loglevel=info
   
   # Terminal 3: Start FastAPI server
   uvicorn app.main:app --reload
   ```

2. **Generate a PDF**:
   ```bash
   curl -X POST "http://localhost:8000/generate_pdf" \
        -H "Content-Type: application/json" \
        -d '{
          "email": "john@example.com",
          "name": "John Doe",
          "desc": "Software Developer",
          "password": "mypassword123"
        }'
   ```

3. **Check task status**:
   ```bash
   curl "http://localhost:8000/task_status/{task_id}"
   ```

4. **Download the PDF**:
   ```bash
   curl "http://localhost:8000/download/{task_id}" --output report.pdf
   ```

## 🔍 Task Status Values

- `PENDING`: Task is waiting to be executed
- `STARTED`: Task is currently being processed
- `SUCCESS`: Task completed successfully
- `FAILURE`: Task failed with an error
- `RETRY`: Task is being retried

## 🛡️ Error Handling

The application includes comprehensive error handling:
- Invalid task IDs return appropriate error messages
- Missing files return 404 errors
- Failed tasks return 500 errors
- Background file cleanup prevents disk space issues

## 🧪 Testing

You can test the API using the interactive documentation at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BROKER_URL` | Redis broker URL for Celery | `redis://localhost:6379/0` |
| `BACKEND_URL` | Redis backend URL for Celery results | `redis://localhost:6379/0` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Troubleshooting

### Common Issues

1. **Redis connection error**: Make sure Redis server is running
2. **PDF generation fails**: Ensure wkhtmltopdf is installed and accessible
3. **Celery worker not starting**: Check Redis connection and environment variables
4. **File not found errors**: Ensure the `output` directory exists and is writable

### Debug Mode

To run in debug mode with more verbose logging:
```bash
celery -A app.celery_app worker --loglevel=debug
uvicorn app.main:app --reload --log-level debug
``` 
