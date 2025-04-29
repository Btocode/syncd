# SyncD Backend

A FastAPI backend service for device management and authentication using Supabase and PostgreSQL.

## Features

- User authentication with Supabase
- Device management (register, update, delete)
- Secure token-based authentication
- PostgreSQL for device data storage
- Database migrations with Alembic
- Comprehensive logging
- CORS support
- API documentation with Swagger UI

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher
- Supabase project
- uv (optional, for faster dependency management)

## Installation

### Using Setup Scripts (Recommended)

1. Clone the repository
2. Run the development setup script:
   ```bash
   ./scripts/dev_setup.sh
   ```
   This script will:
   - Create a virtual environment
   - Install dependencies using uv
   - Set up the .env file
   - Create the database
   - Run migrations

### Using uv (Manual)

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

1. Start the server (from the backend directory):
   ```bash
   cd backend  # Make sure you're in the backend directory
   uvicorn app.main:app --reload
   ```
   Or from any directory:
   ```bash
   uvicorn app.main:app --reload --app-dir backend
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

## Security Considerations

- All endpoints (except signup/login) require authentication
- Tokens are stored in secure HTTP-only cookies
- CORS is configured for specific origins
- Comprehensive error handling and logging
- Input validation using Pydantic models
- SQL injection protection with SQLAlchemy
- Database connection pooling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.