# ai-project

This is a FastAPI application with user management and authentication.

## Getting Started

### Prerequisites
- Docker installed on your machine
- Python 3.11+ (if running locally)

### Build and Run with Docker

1. Build the Docker image:
   ```sh
   docker build -t ai-project .
   ```

2. Run the Docker container:
   ```sh
   docker run -p 8000:8000 ai-project
   ```

3. Access the API at: [http://localhost:8000](http://localhost:8000)

### Running Locally (without Docker)

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Start the server:
   ```sh
   uvicorn app.main:app --reload
   ```

### Project Structure
- `app/models/user.py` - SQLAlchemy models, Pydantic schemas, and DB session logic
- `app/api/users.py` - User CRUD API endpoints
- `app/api/auth.py` - Authentication endpoints (login, password hashing, etc.)
- `app/main.py` - FastAPI app entry point and router includes
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration

### API Endpoints

#### Users
- `POST /users/` - Create a new user (checks for duplicate email, generates UUID for id)
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get a user by UUID
- `PUT /users/{user_id}` - Update a user by UUID
- `DELETE /users/{user_id}` - Delete a user by UUID

#### Auth
- `POST /auth/token` - Login endpoint (OAuth2, returns a bearer token)

### Notes
- All database logic is in `models/user.py`.
- All authentication logic is in `api/auth.py`.
- All user CRUD logic is in `api/users.py`.
- Passwords are hashed before storage and never returned in API responses.
- Internal database IDs (`internal_id`) are not exposed in API responses.
- User IDs are UUID strings for public use.
- Requires `passlib[bcrypt]` and `python-multipart` for authentication support.