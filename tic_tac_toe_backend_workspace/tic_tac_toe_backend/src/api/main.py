from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
import uuid


# Tic Tac Toe models
class NewGameRequest(BaseModel):
    """Request model to create a new game."""
    player_name: str = Field(
        ..., description="Name of player creating the game"
    )


class JoinGameRequest(BaseModel):
    """Request model for a player to join a game."""
    player_name: str = Field(
        ..., description="Name of player joining the game"
    )


class MoveRequest(BaseModel):
    """Request model to make a move on the board."""
    player_id: str = Field(
        ..., description="Player's unique identifier"
    )
    row: int = Field(
        ..., ge=0, le=2, description="Row (0-2)"
    )
    col: int = Field(
        ..., ge=0, le=2, description="Column (0-2)"
    )


class PlayerInfo(BaseModel):
    """Information about a player."""
    player_id: str = Field(
        ..., description="Player's unique identifier"
    )
    name: str = Field(
        ..., description="Player's name"
    )
    symbol: Literal['X', 'O'] = Field(
        ..., description="Symbol assigned to player (X or O)"
    )


class GameState(BaseModel):
    """Complete game state to return to front-end."""
    game_id: str = Field(
        ..., description="Unique game ID"
    )
    board: List[List[Optional[Literal['X', 'O']]]] = Field(
        ..., description="3x3 board state (X, O or None)"
    )
    players: List[PlayerInfo] = Field(
        ..., description="Players in game"
    )
    current_turn: Optional[str] = Field(
        None, description="Player ID whose turn it is, null if not game in progress"
    )
    winner: Optional[str] = Field(
        None, description="Player ID that won, or 'draw'"
    )
    game_status: Literal['waiting', 'in_progress', 'finished'] = Field(
        ..., description="'waiting', 'in_progress', or 'finished'"
    )


# In-memory database (for demo/development purposes)
games: Dict[str, dict] = {}

app = FastAPI(
    title="Tic Tac Toe Backend API",
    description=(
        "FastAPI backend for Tic Tac Toe game. Create/join games, submit moves, and fetch "
        "board & game state."
    ),
    version="1.0.0",
    openapi_tags=[
        {"name": "Games", "description": "Endpoints to create, join, fetch, and play Tic Tac Toe games"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"], summary="Health check", description="Simple health check endpoint")
def health_check():
    """Returns a message if the service is healthy."""
    return {"message": "Healthy"}


# Games API

# PUBLIC_INTERFACE
@app.post(
    "/games",
    summary="Create a new tic tac toe game",
    description="Creates a new game and returns the game state. Player is assigned as X.",
    response_model=GameState,
    tags=["Games"]
)
def create_game(request: NewGameRequest):
    """
    Creates a new Tic Tac Toe game.

    The first player is assigned 'X'.
    Returns the initial game state.
    """
    game_id = str(uuid.uuid4())
    player_id = str(uuid.uuid4())
    player_info = {
        "player_id": player_id,
        "name": request.player_name,
        "symbol": "X"
    }
    game_data = {
        "game_id": game_id,
        "board": [[None for _ in range(3)] for _ in range(3)],
        "players": [player_info],
        "current_turn": player_id,
        "winner": None,
        "game_status": "waiting"
    }
    games[game_id] = game_data
    return _serialize_game_state(game_data)


# PUBLIC_INTERFACE
@app.post(
    "/games/{game_id}/join",
    summary="Join an existing game",
    description=(
        "Joins an existing game (must be waiting for a second player). "
        "Player is assigned O."
    ),
    response_model=GameState,
    tags=["Games"]
)
def join_game(game_id: str, request: JoinGameRequest):
    """
    A player joins an existing waiting game.

    The new player is assigned 'O'.
    Returns updated game state.
    """
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if len(game["players"]) >= 2:
        raise HTTPException(status_code=400, detail="Game already has two players")
    player_id = str(uuid.uuid4())
    player_info = {"player_id": player_id, "name": request.player_name, "symbol": "O"}
    game["players"].append(player_info)
    game["game_status"] = "in_progress"
    # X always goes first, so don't change current_turn.
    return _serialize_game_state(game)


# PUBLIC_INTERFACE
@app.get(
    "/games/{game_id}",
    summary="Fetch Tic Tac Toe game state",
    description="Returns full board state, players, whose turn, and winner/state info.",
    response_model=GameState,
    tags=["Games"]
)
def fetch_game(game_id: str):
    """
    Returns the full state of the game including board, players, and status.
    """
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return _serialize_game_state(game)


# PUBLIC_INTERFACE
@app.post(
    "/games/{game_id}/move",
    summary="Submit a move",
    description="Player submits a move at row/col. Returns updated game state.",
    response_model=GameState,
    tags=["Games"]
)
def submit_move(game_id: str, request: MoveRequest):
    """
    Accepts a player's move (row/col).
    Validates rules, updates state, checks for win/draw, and returns new state.
    """
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game["game_status"] != "in_progress":
        raise HTTPException(status_code=400, detail="Game not in progress")

    player = next((p for p in game["players"] if p["player_id"] == request.player_id), None)
    if not player:
        raise HTTPException(status_code=403, detail="Player not part of this game")

    if player["player_id"] != game["current_turn"]:
        raise HTTPException(status_code=403, detail="It's not your turn")

    symbol = player["symbol"]
    board = game["board"]

    # Validate move
    if request.row < 0 or request.row > 2 or request.col < 0 or request.col > 2:
        raise HTTPException(status_code=400, detail="Move out of bounds")
    if board[request.row][request.col] is not None:
        raise HTTPException(status_code=400, detail="Cell is already occupied")

    # Apply move
    board[request.row][request.col] = symbol

    # Check for win/draw
    winner_symbol = _check_winner(board)
    if winner_symbol is not None:
        winner_player = next(
            (p for p in game["players"] if p["symbol"] == winner_symbol),
            None
        )
        game["winner"] = winner_player["player_id"] if winner_player else None
        game["game_status"] = "finished"
        game["current_turn"] = None
    elif all(cell is not None for row in board for cell in row):
        game["winner"] = "draw"
        game["game_status"] = "finished"
        game["current_turn"] = None
    else:
        # Change turn
        player_ids = [p["player_id"] for p in game["players"]]
        next_player_idx = (player_ids.index(request.player_id) + 1) % 2
        game["current_turn"] = player_ids[next_player_idx]
        game["winner"] = None
    return _serialize_game_state(game)


# Helper functions
def _check_winner(board: List[List[Optional[str]]]) -> Optional[str]:
    """Returns 'X' or 'O' if either wins, else None"""
    lines = []
    # Rows, Columns, Diagonals
    lines.extend(board)  # Rows
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])  # Cols
    lines.append([board[i][i] for i in range(3)])  # Main diagonal
    lines.append([board[i][2 - i] for i in range(3)])  # Anti-diagonal
    for line in lines:
        if line[0] and line.count(line[0]) == 3:
            return line[0]
    return None


def _serialize_game_state(game: dict) -> GameState:
    """Serializes the internal game object for front-end consumption."""
    return GameState(
        game_id=game["game_id"],
        board=game["board"],
        players=[PlayerInfo(**p) for p in game["players"]],
        current_turn=game["current_turn"],
        winner=game["winner"],
        game_status=game["game_status"]
    )
