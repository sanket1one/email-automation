# Email Automation API

**Email Automation API** is a FastAPI-based web server for sending emails with optional PDF attachments. It leverages OAuth2 for secure Gmail integration and uses background tasks for asynchronous email sending.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
- [Running the Project](#running-the-project)
  - [Locally](#locally)
  - [Using Docker](#using-docker)
- [API Endpoints](#api-endpoints)
  - [Send Email Endpoint](#send-email-endpoint)
- [Expected Behavior](#expected-behavior)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **FastAPI Framework**: Modern, high-performance API development.
- **Email Sending**: Supports plain text and HTML emails.
- **Attachments**: Optionally attach PDF files.
- **OAuth2 Authentication**: Uses Gmail OAuth2 for secure SMTP authentication.
- **Background Tasks**: Processes email sending asynchronously.
- **Docker Support**: Easily deploy with Docker and Docker Compose.

## Getting Started

### Prerequisites

- Python 3.8 or above (Python 3.10 recommended)
- [pip](https://pip.pypa.io/en/stable/)
- [Docker](https://www.docker.com/) (optional, for containerized deployment)

### Environment Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/email-automation.git
   cd email-automation
   ```

2. **Configure environment variables:**

    Create a `.env` file with:

    ```bash
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    FROM_EMAIL=your-email@gmail.com
    OAUTH2_CLIENT_ID=your_client_id_here
    OAUTH2_CLIENT_SECRET=your_client_secret_here
    OAUTH2_REFRESH_TOKEN=your_refresh_token_here
    OAUTH2_TOKEN_URI=https://oauth2.googleapis.com/token
    ```

3. ** Running project Locally **

    All the configurating in currated in the `start_fastapi.sh` file

    ```bash
    cd app/
    sh start_fastapi.sh
    ```

4. ** Running project using Docker ** 

    Build and run the Docker image:

    ```bash
    docker-compose up -d --build
    ```

## API Endpoints

### Send Email Endpoint (POST /send-email/)
Sends emails with optional PDF attachments. Accepts JSON or multipart/form-data.

    **Example JSON Request:**
    ```bash
    curl -X POST "http://127.0.0.1:8000/send-email/" \
    -H "Content-Type: application/json" \
    --data-binary '{"recipient": "recipient@example.com", "subject": "Test Email", "body": "<h1>Hello!</h1>"}'
    ```

## Expected Behavior
- Valid requests return: `{"message": "Email is being sent"}`
- Emails are sent asynchronously via Gmail's SMTP
- Logs show success/error messages during delivery

## Troubleshooting
- **OAuth2 Issues**: Verify credentials and enable the Gmail API
- **Port Conflicts**: Change port 8000 if occupied
- **Attachment Errors**: Ensure valid PDF (or adjust logic for other file types)

## Contributing
Contributions are welcome! Fork the repository and submit pull requests.

## Acknowledgements
- FastAPI
- Gmail API
- Google OAuth2
- Open-source community
