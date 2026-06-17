# PolyEngine Terminal Mode Engine ♟️

A lightweight, rule-enforced chess engine built entirely from scratch in Python, featuring deep integration with an adversarial Grandmaster-level Stockfish instance running via system-level IPC pipes. 

The engine utilizes an optimized **Inversion-Radar Scanning Algorithm** for dynamic check validation and applies a **Parallel-State Simulation Loop** to isolate and prune illegal candidate moves.

---

## 🚀 Features

* **Complete Piece Physics:** Full analytical movement and geometric collision mechanics across all standard chess variants (Pawns, Rooks, Bishops, Knights, Queens, and Kings).
* **Inversion Radar Check Detection:** An optimized check-screening framework that casts continuous multi-directional rays outward from the active King’s current coordinate grid to flag enemy intercept vectors dynamically.
* **Parallel State Simulation:** Prunes candidate move pathways automatically (such as handling pinned pieces) by performing temporary deep-state projections and filtering out invalid endpoints before committing to the stack.
* **Stockfish Co-Processing Node:** A built-in, zero-dependency background subprocess link to coordinate game-state vectors with a local Linux Stockfish execution core over standard Universal Chess Interface (UCI) channels.
* **Game Over Analytics:** Comprehensive post-analysis tracking to automatically isolate deadlocks, identifying **Checkmate** and **Stalemate** conditions perfectly.
* **Time Travel Stack:** Deep snapshot logging to preserve historical coordinates, turn registries, and capture variables, allowing instant step-back operations (`undo`).

---

## 🛠️ Project Structure

```text
├── engine.py          # Core engine loop, UCI serialization, and game-state array
└── README.md          # Project ecosystem documentation


```


## 🕹️ Game Architecture & State Matrix
The core structural grid relies on an $8 \times 8$ nested matrix mapping standard ranks and files to index coordinates:White Pieces: Represented by uppercase characters (P, N, B, R, Q, K).Black Pieces: Represented by lowercase characters (p, n, b, r, q, k).Empty Squares: Marked by primitive dots (.).

## 💻 Setup & Installation

1. PrerequisitesEnsure your Linux system has an updated Python 3.12+ package layer installed:

```
sudo apt update
sudo apt install
python3 python3-full

```
2. Dependency-Free Stockfish IntegrationTo avoid Python package variance or version drift (AttributeError flags), PolyEngine interacts directly with your operating system's native compiled Stockfish instance over background subprocess execution channels. Install it to your system paths globally:
```
 sudo apt install stockfish
 ```
Note: This automatically provisions your workspace at /usr/games/stockfish with a binary optimized specifically for your local CPU instruction set (bypassing AVX2 mismatch core dumps).🏃 Run the EngineFire up the engine loop straight from your terminal:

```
 python3 engine.py
```
Player Mechanics & CommandsAlgebraic Moves: Input moves by specifying start and destination coordinates combined (e.g., e2e4 transitions your King's Pawn forward).Undo State: Type undo during your active turn to rewind both your last move and Stockfish’s calculation response simultaneously.Terminate: Type quit to cleanly tear down sub-processes and exit back to terminal space.
## ⚙️ Development & Troubleshooting 
#Notes: Virtual Environments & System Management (PEP 668)Modern distributions prevent global package installs. If you ever need to append external pip dependencies locally, spin up and activate your sandboxed space inside the directory:Bashpython3 -m venv env
source env/bin/activate
Version Control Best Practices (.gitignore)To prevent large binary files or bloated vendor dependency packages from hitting GitHub's 100MB strict transmission limit, ensure your root contains a .gitignore tracking matrix:Plaintextstockfish*
env/
venv/
__pycache__/
*.exe
If a large binary is trapped in your local history cache causing push rejections, reset your indexing pointer out of memory safely via:Bashgit reset --mixed HEAD~1
git rm --cached stockfish-ubuntu-x86-64-avx2


## 🗺️ Roadmap & Evolution Matrix

### 🟢 Phase 1: Core Mechanics & Geometry (Complete)
* **Matrix Array Mapping & Piece Geometry**
  * *Implementation:* Established the foundational 8x8 nested array tracking grid, defining strict algebraic vector boundaries for individual pieces.
* **Inversion Raycasting Radar**
  * *Implementation:* Developed a dynamic directional matrix calculation engine that projects threat vectors outward from the King's position to instantly identify check conditions.
* **Volatile Future-State Filters**
  * *Implementation:* Built a simulation loop that clones the active board state to test candidate moves, pruning pathways that leave pieces pinned or expose the King to check.

### 🟡 Phase 2: Engine Integration & State Architecture (Complete)
* **Dual-Turn Rewind Stack Engine**
  * *Implementation:* Implemented a historical state logger monitoring capture mutations, allowing seamless multi-turn state rewinds (`undo`).
* **Zero-Dependency Linux IPC Interacting Node**
  * *Implementation:* Developed native pipeline communications via `subprocess` directly to the `/usr/games/stockfish` binary, allowing zero-package Universal Chess Interface (UCI) state handshakes.

### 🔵 Phase 3: Desktop Interface & Advanced FIDE Rules (Upcoming)
* **Graphical Desktop UI Integration**
  * *Implementation:* Transformed coordinate-based terminal strings into an active canvas view with visual sprite mapping and drag-and-drop mechanics using Pygame.
* **Advanced FIDE Validation Matrices**
  * *Implementation:* Completed full rule compliance by mapping internal tracking markers for transient pawn captures (**En Passant**), pawn replacement indexing (**Promotion**), and dual-coordinate safety evaluations (**Castling**).

---

### 📈 Current Engine Development Progress

| Milestone Block | Status | Sub-System Focus |
| :--- | :---: | :--- |
| **Phase 1: Vector Geometry** | `COMPLETED` | Board Mapping, Raycasting Radar, Pinned Piece Screening |
| **Phase 2: Subprocess Core** | `COMPLETED` | Move Stack Memory, Direct Native IPC Stockfish Processing |
| **Phase 3: GUI Canvas** | `UPCOMING` | Pygame Grid Conversion, Advanced Rule Matrices |
| **Phase 4: Optimization** | `UPCOMING` | Bitboard Bitwise Math, Engine Alpha-Beta Pruning |
