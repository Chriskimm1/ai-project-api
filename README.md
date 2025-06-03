# ai-project

This is a FastAPI application.

## Getting Started

### Prerequisites
- Docker installed on your machine

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

### Project Structure
- `app/` - Main application code
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration

---

For development without Docker, install dependencies with `pip install -r requirements.txt` and run with `uvicorn app.main:app --reload`.

## Endpoints

- **Users**
  - `POST /users`: Create a new user
  - `GET /users`: Retrieve a list of users
  - `GET /users/{user_id}`: Retrieve a specific user by ID
  - `PUT /users/{user_id}`: Update a specific user by ID
  - `DELETE /users/{user_id}`: Delete a specific user by ID

## License

This project is licensed under the MIT License.