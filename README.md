# JWT Auth Service (FastAPI)

A simple JWT-based authentication API built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features
- User registration with either `email` or `phone`
- Login with JWT access and refresh tokens
- Refresh token flow (`/auth/refresh`)
- Authenticated profile endpoint (`/auth/me`)
- Change password endpoint (`/auth/change-password`)
- Health check endpoint (`/auth/health`)

## Project Structure
```text
app/
  api/        # FastAPI routers
  core/       # settings + security helpers
  db/         # SQLAlchemy models + session + CRUD
  service/    # auth business logic + schemas + validators
shared/       # shared logger
```

## Requirements
- Python 3.10+
- PostgreSQL database

Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment Variables
Create a `.env` file in the project root (`E:\Courses\JWT`) or copy from `.env.example`.

### `.env` structure
```env
# Database
DATABASE_URL="postgresql+psycopg2://<user>:<password>@<host>:5432/<db_name>?sslmode=require"

# JWT
JWT_SECRET="replace_with_a_long_random_secret"
JWT_ALGORITHM="HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES="60"
JWT_REFRESH_TOKEN_EXPIRE_DAYS="30"

# Optional (not used by current code)
CLIENT_ID=""
CLIENT_SECRET=""
```

### Variable reference
- `DATABASE_URL`: SQLAlchemy PostgreSQL connection string.
- `JWT_SECRET`: Secret key used to sign/verify JWT tokens.
- `JWT_ALGORITHM`: JWT algorithm (current code expects `HS256`).
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiry in minutes.
- `JWT_REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiry in days.
- `CLIENT_ID`: Reserved for future Google OAuth integration (currently unused).
- `CLIENT_SECRET`: Reserved for future Google OAuth integration (currently unused).

## Run the Service
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API docs:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints
Base prefix: `/auth`

- `GET /health` - Service health check
- `POST /register` - Register user
- `POST /login` - Login and receive access/refresh tokens
- `POST /refresh` - Issue fresh tokens using refresh token
- `POST /logout` - Stateless logout response
- `POST /change-password` - Change password using access token
- `GET /me` - Get current user from access token

## Notes
- On startup, tables are created automatically via `Base.metadata.create_all(bind=engine)`.
- Registration rules:
  - Provide exactly one of `email` or `phone`
  - Phone must be 10 digits
  - Password cannot be empty
