# Basic A2A Example

## File Structure

```
01_basic/
├── server/
│   └── tell_time_server.py     # A2A server implementation
├── client/
│   └── time_client.py          # A2A client implementation
├── pyproject.toml              # Project dependencies
└── uv.lock                     # Locked dependencies
```

## Setup

Initialize the UV environment and install dependencies:

```bash
uv sync
```

## Run

**Start the server** (in terminal 1):
```bash
uv run uvicorn server.tell_time_server:app --port 8000
```

**Run the client** (in terminal 2):
```bash
uv run python client/time_client.py
```
