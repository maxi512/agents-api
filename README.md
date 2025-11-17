# Agent API

A FastAPI application that uses OpenAI Agents SDK to query heroes and villains from a database and external API. The system intelligently routes queries to either a local SQLite database (for heroes) or the Superhero API (for villains).

## Features

- **Intelligent Query Routing**: Automatically determines whether to query the local database (heroes) or external API (villains)
- **Natural Language SQL Generation**: Converts natural language queries into SQL using AI
- **Multi-Agent Architecture**: Separate agents for SQL generation, API parsing, and hero/villain queries
- **FastAPI REST API**: Simple HTTP endpoint for querying heroes and villains

## Prerequisites

- Python >= 3.14
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key
- Superhero API key (get one at [superheroapi.com](https://superheroapi.com))

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd agent-api
   ```

2. **Install dependencies using uv**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   
   Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   SUPERHERO_API_KEY=your_superhero_api_key_here
   ```

   Or export them in your shell:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key_here
   export SUPERHERO_API_KEY=your_superhero_api_key_here
   ```

## Running the Application

1. **Start the FastAPI server**:
   ```bash
   uv run uvicorn main:app --reload
   ```

   The server will start on `http://localhost:8000` by default.

2. **Access the API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Usage

### Query Heroes/Villains

Make a GET request to the `/heroes` endpoint with a query parameter:

```bash
curl "http://localhost:8000/heroes?query=find%20Batman"
```

Or using the interactive docs at `http://localhost:8000/docs`, enter a query like:
- `"find Batman"` - Returns Batman from the database
- `"all Marvel heroes"` - Returns all Marvel heroes from the database
- `"find Joker"` - Returns Joker from the Superhero API (villain)
- `"show me Spider-Man"` - Returns Spider-Man from the database

### Example Responses

**Single Hero Query:**
```json
[
  {
    "id": 1,
    "name": "Batman",
    "real name": "Bruce Wayne",
    "universe": "DC comics"
  }
]
```

**Multiple Heroes Query:**
```json
[
  {
    "id": 1,
    "name": "Batman",
    "real name": "Bruce Wayne",
    "universe": "DC comics"
  },
  {
    "id": 2,
    "name": "Superman",
    "real name": "Clark Kent",
    "universe": "DC comics"
  }
]
```

## Project Structure

```
agent-api/
├── agents/              # Agent implementations
│   ├── hero_agent.py   # Main hero/villain query agent
│   ├── sql_agent.py    # SQL query generation agent
│   ├── parse_api_agent.py  # API response parsing agent
│   └── tools.py        # Function tools (execute_sql, call_api)
├── heroes_data.py      # Database initialization
├── heroes_api.py       # Superhero API client
├── models.py           # Pydantic models
├── main.py             # FastAPI application entry point
├── heroes.csv          # Source data for heroes database
└── heroes.db           # SQLite database (auto-generated)
```

## How It Works

1. **Database Initialization**: On startup, the application loads heroes from `heroes.csv` into a SQLite database.

2. **Query Processing**: When a query is received:
   - The `HeroAgent` determines if the query is for a hero (database) or villain (API)
   - For heroes: Uses `SQLAgent` to generate SQL, then executes it
   - For villains: Calls the Superhero API, then uses `ParseAPIAgent` to parse the response

3. **Response Format**: All responses are returned as a list of `HeroModel` objects with consistent structure.

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run ruff format .
```

### Linting

```bash
uv run ruff check .
```

## API Endpoints

### GET `/heroes`

Query heroes or villains using natural language.

**Parameters:**
- `query` (string, required): Natural language query (e.g., "find Batman", "all Marvel heroes")

**Response:**
- `200 OK`: List of `HeroModel` objects
- `400 Bad Request`: Error message if query fails

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key for the Agents SDK | Yes |
| `SUPERHERO_API_KEY` | Your Superhero API key | Yes |

## License

[Add your license here]

