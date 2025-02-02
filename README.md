# Real-Time Collaborative Code Editor

A FastAPI-based collaborative code editor with real-time collaboration and AI-assisted debugging capabilities.

## Architecture

### Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Caching/Message Broker**: Redis
- **Containerization**: Docker
- **AI Integration**: OpenAI API

### Key Components

1. **Authentication System**
   - JWT-based authentication
   - Role-based access control
   - Secure password hashing

2. **Real-Time Collaboration**
   - WebSocket connections for live updates
   - Cursor position tracking
   - Concurrent editing support
   - Conflict resolution

3. **File Management**
   - CRUD operations for code files
   - File sharing and collaboration
   - Access control and permissions

4. **AI Debugging Assistant**
   - Real-time code analysis
   - Error detection and suggestions
   - Performance optimization tips

### Data Models

1. **User**
   ```python
   class User:
       id: int
       email: str
       username: str
       hashed_password: str
       is_active: bool
       code_files: List[CodeFile]
       editing_sessions: List[EditingSession]
   ```

2. **CodeFile**
   ```python
   class CodeFile:
       id: int
       name: str
       content: str
       language: str
       owner_id: int
       created_at: datetime
       updated_at: datetime
       owner: User
       editing_sessions: List[EditingSession]
   ```

3. **EditingSession**
   ```python
   class EditingSession:
       id: int
       code_file_id: int
       user_id: int
       role: UserRole (OWNER/COLLABORATOR)
       cursor_position: int
       last_active: datetime
   ```

## Setup and Installation

### Prerequisites
- Docker and Docker Compose
- Git

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/collaborative-code-editor.git
   cd collaborative-code-editor
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   ```
   Update the following variables in `.env`:
   - `SECRET_KEY`: Your secret key for JWT
   - `OPENAI_API_KEY`: Your OpenAI API key
   - Other configuration as needed

3. Start the application:
   ```bash
   chmod +x scripts/start.sh
   ./scripts/start.sh
   ```

The application will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- pgAdmin: http://localhost:5050

### Available Services

- **FastAPI Application**: Port 8000
  - Main application server
  - WebSocket endpoints
  - REST API endpoints

- **PostgreSQL**: Port 5432
  - Primary database
  - Persistent storage

- **Redis**: Port 6379
  - Real-time message broker
  - Caching layer

- **pgAdmin**: Port 5050
  - Database management interface
  - Default credentials:
    - Email: admin@admin.com
    - Password: admin

## API Endpoints

### Authentication
- `POST /api/v1/auth/register`: Register new user
- `POST /api/v1/auth/login`: Login and get JWT token
- `GET /api/v1/auth/me`: Get current user info

### Code Files
- `POST /api/v1/files/`: Create new file
- `GET /api/v1/files/`: List user's files
- `GET /api/v1/files/{file_id}`: Get file details
- `PUT /api/v1/files/{file_id}`: Update file
- `DELETE /api/v1/files/{file_id}`: Delete file

### Collaboration
- `POST /api/v1/files/{file_id}/invite`: Invite collaborator
- `WebSocket /api/v1/collaboration/ws/{file_id}`: Real-time collaboration

## Development

### Project Structure 
```
collaborative-code-editor/
├── alembic/ # Database migrations
├── app/
│ ├── api/ # API endpoints
│ ├── core/ # Core configurations
│ ├── db/ # Database setup
│ ├── models/ # SQLAlchemy models
│ ├── schemas/ # Pydantic schemas
│ ├── services/ # Business logic
│ └── main.py # Application entry point
├── tests/ # Test cases
├── docker-compose.yml # Docker services config
├── Dockerfile # Application container config
└── requirements.txt # Python dependencies
```

### Adding New Features

1. Create new models in `app/models/`
2. Create corresponding schemas in `app/schemas/`
3. Add new endpoints in `app/api/`
4. Update database migrations:
   ```bash
   docker compose exec web alembic revision --autogenerate -m "description"
   docker compose exec web alembic upgrade head
   ```

## Production Deployment

For production deployment:

1. Update environment variables:
   - Use strong SECRET_KEY
   - Set proper CORS origins
   - Use secure database credentials

2. Enable HTTPS:
   - Set up SSL certificates
   - Configure reverse proxy (nginx)

3. Set up monitoring:
   - Configure health checks
   - Set up logging
   - Monitor resource usage

4. Scale services:
   - Increase service replicas
   - Configure load balancing
   - Set up database replication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Testing

See [TESTING.md](TESTING.md) for more information on running tests.