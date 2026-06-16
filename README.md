# PolyEngine Terminal Mode Engine ♟️

A lightweight, rule-enforced chess engine built from scratch in Python. The engine features an optimized inversion-radar scanning algorithm for check detection and uses a parallel-state simulation loop to validate legal moves.

Currently, the engine operates in a terminal sandbox environment, with architecture prepped for integration into a graphical interface (GUI).

---

## 🚀 Features

* **Complete Piece Physics:** Full movement and collision mechanics for Pawns, Rooks, Bishops, Knights, Queens, and Kings.
* **Inversion Radar Check Detection:** An efficient check validation system that casts rays outward from the King's coordinate to detect enemy threats dynamically.
* **Parallel State Simulation:** Automatically screens out illegal moves (like moving pinned pieces) by simulating future board states and filtering invalid paths before user execution.
* **Game Over Analytics:** Native recognition of both **Checkmate** and **Stalemate** conditions.
* **Time Travel:** Built-in `undo` stack to instantly reverse board positioning, turn tracking, and dynamic piece data.

---

## 🛠️ Project Structure

```text
├── engine.py          # Core game loop, piece validation, and state tracker
└── README.md          # Project documentation and roadmap
