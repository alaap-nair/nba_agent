# NBA Agent

A small LangChain-based assistant for checking NBA stats and schedules.

## Features
- **Command-line chat** via `chat.py`.
- **Streamlit web app** using `app.py`.
- Tools for player stats, team schedules, and standings located in `tools.py`.
- **New:** Team roster lookup via the `nba_roster` tool.
- **New:** Team arena lookup via the `nba_arena` tool.
- The stats tool now also exposes shooting percentages (FG%, 3P%, FT%) when available.
- Local caching of API requests under `cache.py`.

## Architecture

```mermaid
graph TD
    A[User Input] --> B{Interface}
    
    B -->|Terminal| C[chat.py]
    B -->|Web| D[app.py]
    
    C --> E[LangChain Agent]
    D --> E
    
    E --> F{Query Type}
    
    F -->|Player Stats| G[StatsTool]
    F -->|Team Schedule| H[ScheduleTool] 
    F -->|Standings| I[StandingsTool]
    
    G --> J{Data Source}
    H --> J
    I --> J
    
    J -->|Cache| K[Local Cache]
    J -->|API| L[balldontlie.io]
    
    K --> M[Response]
    L --> N[cache.set] --> M
    
    M --> O{Output Format}
    O -->|Terminal| P[Console]
    O -->|Web| Q[Streamlit Charts/Tables]
    
    style A fill:#e1f5fe
    style E fill:#f3e5f5
    style G fill:#e8f5e8
    style H fill:#e8f5e8
    style I fill:#e8f5e8
    style K fill:#fff8e1
    style L fill:#ffebee
```

## Usage
Run the interactive chat in your terminal:
```bash
python chat.py
```

Launch the web interface:
```bash
bash start_web.sh
```

### Tests
Execute the test suite with:
```bash
python run_judgment_tests.py [all|evaluation|tracing|performance]
```

## Repository Layout
- `agent.py` – agent factory for LangChain
- `chat.py` – terminal chat interface
- `app.py` – Streamlit application
- `tools.py` – stats and schedule tools
- `start_web.sh` – helper script to start the web app

