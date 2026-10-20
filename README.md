# Employee Directory Search System

A full-stack employee directory application that lets users search employees by name or department. Built with React, Vite, FastAPI, SQLAlchemy, and MySQL.

## Features

- Search employees by name or department
- Debounced search to reduce unnecessary API requests
- Responsive interface with loading, empty, and error states
- Input validation and consistent error responses
- Layered backend architecture separating routes, services, repositories, schemas, and models
- Automated backend tests
- Indexed database search with a maximum of 50 results

## Tech Stack

- **Frontend:** React, Vite, JavaScript, CSS
- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** MySQL
- **Testing:** pytest

## Project Structure

```text
employee-directory/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exception_handlers.py
│   │   └── main.py
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
├── database/
│   ├── schema.sql
│   └── performance_test.sql
├── frontend/
│   ├── src/
│   ├── .env.example
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

## Prerequisites

Install the following before running the application:

- Python
- Node.js and npm
- MySQL Server

## Database Setup

1. Start MySQL Server.
2. Open MySQL Workbench and execute `database/schema.sql` to create the database, employee table, indexes, and sample records.
3. Copy `backend/.env.example` to `backend/.env`.
4. Update the database credentials in `backend/.env` to match your local MySQL configuration.

The sample records are fictional and intended for local testing.

## Backend Setup

From the project root, open a terminal and run:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The backend will run at `http://127.0.0.1:8000`.

- **API documentation:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/health

Keep the backend terminal running.

## Frontend Setup

Open a second terminal from the project root:

```powershell
cd frontend
npm install
```

Copy `frontend/.env.example` to `frontend/.env` if the local environment file does not already exist.

Ensure the API URL points to the running backend. For example:

```dotenv
VITE_API_BASE_URL=http://localhost:8000
```

Start the frontend:

```powershell
npm run dev
```

Open the local URL shown by Vite, usually `http://localhost:5173`.

## API Endpoint

### Search Employees

`GET /employees?search=rah`

Searches employee names and departments using prefix matching. For example, `rah` can match names beginning with Rahul, while `eng` can match the Engineering department.

The API returns at most 50 employees, ordered by employee ID.

### HTTP Status Codes

| Status                     | Description                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------- |
| `200 OK`                   | Search completed successfully, including when no employees match                   |
| `404 Not Found`            | Requested route does not exist                                                     |
| `422 Unprocessable Entity` | Search input exceeds the allowed 100-character limit or otherwise fails validation |
| `503 Service Unavailable`  | Database search fails due to a handled database error                              |

## Running Tests

From the backend directory, activate the virtual environment and run:

```powershell
python -m pytest -v
```

The tests cover health checks, employee search behavior, empty results, input validation, route handling, query construction, and database-error handling.

## Performance and Design Decisions

- **Debounced search:** A 300 ms debounce reduces requests while users type.
- **Request cancellation:** `AbortController` cancels outdated frontend requests.
- **Database indexes:** B-tree indexes are defined on the `name` and `department` columns.
- **Prefix matching:** Queries use patterns such as `LIKE 'rah%'`, allowing MySQL to use index range scans where the optimizer determines they are suitable.
- **Query plan verification:** `EXPLAIN` was used to inspect the search query. The observed plan showed index range scans using both `idx_employees_name` and `idx_employees_department`.
- **Result limit:** The API returns no more than 50 employees per request.
- **Parameterized queries:** SQLAlchemy binds query values rather than concatenating user input into SQL.
- **Layered architecture:** Routing, business logic, database access, models, and response schemas are kept separate.

The query plan was verified against a small local dataset. Actual performance will depend on data volume, distribution, and the MySQL optimizer's choices.

To rerun the index and query-plan checks, execute `database/performance_test.sql` after setting up the database.

## Configuration and Security

- Do not commit actual `.env` files or database passwords.
- Use `.env.example` files as configuration templates.
- Configure your own local MySQL credentials.
- Do not include real or sensitive employee information in sample data.
