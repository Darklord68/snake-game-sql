# Snake Game (Python + MySQL)

A snake game built with Python, Tkinter/CustomTkinter and MySQL. It has three levels (Level 3 adds walls that multiply as you eat) and a top-5 leaderboard stored in a database.

## Requirements
- Python 3.9+
- MySQL Server
- Fonts: ARCADECLASSIC and Mexcellent 3D (download separately and install them on your system)

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Create the database: run `schema.sql` in MySQL.
3. Copy `.env.example` to `.env` and fill in your MySQL details.
4. Run the game: `python snake.py`

## Controls
Arrow keys to move. Eat the red food to grow. Don't hit the walls, the edges, or yourself.
