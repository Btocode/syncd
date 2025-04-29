# SyncD Backend

A FastAPI backend service for device management and authentication using Supabase and PostgreSQL.

## Features

- User authentication with Supabase
- Device management (register, update, delete)
- Secure token-based authentication
- PostgreSQL for device data storage (using Neon.tech)
- Database migrations with Alembic
- Comprehensive logging
- CORS support
- API documentation with Swagger UI
- CI/CD with GitHub Actions

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher (or Neon.tech account)
- Supabase project
- uv (recommended for faster dependency management)

## Installation

### Using uv (Recommended)

1. Clone the repository
2. Install dependencies using uv:
   ```bash
   uv venv
   uv pip install -e .
   ```

### Using pip (Manual)

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

### Environment Setup

1. Copy `.env_sample` to `.env` and update the values:
   ```bash
   cp .env_sample .env
   ```

2. Update the following environment variables in `.env`:
   - `POSTGRES_USER`: PostgreSQL username
   - `POSTGRES_PASSWORD`: PostgreSQL password
   - `POSTGRES_HOST`: PostgreSQL host
   - `POSTGRES_PORT`: PostgreSQL port
   - `POSTGRES_DB`: PostgreSQL database name
   - `DATABASE_URL`: Full PostgreSQL connection URL
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_KEY`: Your Supabase project API key
   - `CORS_ALLOWED_ORIGINS`: List of allowed origins for CORS

3. Create the PostgreSQL database:
   ```bash
   createdb syncd
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

## Running the Application

1. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   Or using uv:
   ```bash
   uv run fastapi dev app/main.py
   ```

2. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup`: Register a new user
- `POST /api/v1/auth/login`: Login user

### Device Management
- `POST /api/v1/devices`: Register a new device
- `GET /api/v1/devices`: Get user's devices
- `PUT /api/v1/devices/{device_id}`: Update device information
- `DELETE /api/v1/devices/{device_id}`: Delete a device

## Database Migrations

To create a new migration:
```bash
alembic revision -m "description of changes"
```

To apply migrations:
```bash
alembic upgrade head
```

To rollback migrations:
```bash
alembic downgrade -1  # Rollback one migration
alembic downgrade base  # Rollback all migrations
```

## Testing

Run tests using pytest:
```bash
pytest
```

## CI/CD Setup

This project uses GitHub Actions for continuous integration and deployment.

### CI Workflow

The CI workflow (`ci.yml`) runs on every push to main/master branches and on pull requests. It:

1. Sets up a Python 3.10 environment
2. Installs dependencies using uv
3. Sets up a PostgreSQL service container for testing
4. Runs database migrations
5. Executes tests
6. Runs linting checks with pre-commit

### CD Workflow

The CD workflow (`cd.yml`) runs on every push to main/master branches and can be manually triggered. It:

1. Sets up a Python 3.10 environment
2. Installs dependencies using uv
3. Runs database migrations
4. Deploys the application to Render

### Required GitHub Secrets

For the CI/CD workflows to function properly, you need to set up the following secrets in your GitHub repository:

- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase project API key
- `POSTGRES_USER`: PostgreSQL username for production
- `POSTGRES_PASSWORD`: PostgreSQL password for production
- `POSTGRES_HOST`: PostgreSQL host for production
- `POSTGRES_PORT`: PostgreSQL port for production
- `POSTGRES_DB`: PostgreSQL database name for production
- `DATABASE_URL`: Full PostgreSQL connection URL for production
- `RENDER_API_KEY`: Your Render API key
- `RENDER_SERVICE_ID`: Your Render service ID

### Local Development with Pre-commit

To ensure code quality, this project uses pre-commit hooks. To set them up:

1. Install pre-commit:
   ```bash
   pip install pre-commit
   ```

2. Install the pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. Run pre-commit on all files:
   ```bash
   pre-commit run --all-files
   ```

## Deployment to Render

This project is configured for deployment on Render.

### Manual Deployment

1. Create a Web Service on Render:
   - Connect your GitHub repository
   - Set Environment to Python
   - Set Build Command to `curl -LsSf https://astral.sh/uv/install.sh | sh && uv venv && uv build`
   - Set Start Command to `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. Configure environment variables in Render:
   - Add all required environment variables from `.env`
   - For sensitive information like passwords and API keys, use the "Secret" option
   - The `render.yaml` file is configured to use GitHub secrets for sensitive information

### Using Neon.tech for PostgreSQL

This project is configured to use Neon.tech for PostgreSQL, which offers a serverless PostgreSQL database with a generous free tier:

1. Create a Neon.tech account at https://neon.tech
2. Create a new project
3. Get your connection details from the Neon dashboard
4. Update your environment variables in Render with the Neon connection details:
   - `POSTGRES_USER`: Your Neon database user
   - `POSTGRES_PASSWORD`: Your Neon database password
   - `POSTGRES_HOST`: Your Neon database host (e.g., `ep-misty-dust-a4f24n0x-pooler.us-east-1.aws.neon.tech`)
   - `POSTGRES_PORT`: Your Neon database port (usually 5432)
   - `POSTGRES_DB`: Your Neon database name
   - `DATABASE_URL`: Your Neon connection string

### Setting Up Environment Variables in Render

For security best practices, sensitive information should be stored as secrets in Render:

1. In your Render dashboard, go to your web service
2. Navigate to the "Environment" tab
3. Add each environment variable from your `.env` file
4. For sensitive information (passwords, API keys, etc.), click the "Secret" toggle
5. The `render.yaml` file is configured to use GitHub secrets for sensitive information, so you don't need to add these values directly in the file

### Automated Deployment with GitHub Actions

The project is configured to automatically deploy to Render when changes are pushed to the main branch:

1. Get your Render API key and service ID
2. Add them as secrets to your GitHub repository
3. Push changes to the main branch to trigger deployment

## Security Considerations

- All endpoints (except signup/login) require authentication
- Tokens are stored in secure HTTP-only cookies
- CORS is configured for specific origins
- Comprehensive error handling and logging
- Input validation using Pydantic models
- SQL injection protection with SQLAlchemy
- Database connection pooling
- Sensitive credentials are stored as secrets in Render and GitHub

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.