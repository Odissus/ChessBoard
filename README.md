# About

An interactive chess board hardware design based on Arduino Nano ESP32 and KiCad.

| Top | Bottom |
| :---: | :---: |
| <img alt='PCB top render' src='https://github.com/Odissus/ChessBoard/releases/download/v1.0.0/Image_Top.png' /> | <img alt='PCB bottom render' src='https://github.com/Odissus/ChessBoard/releases/download/v1.0.0/Image_Bottom.png' /> |

It includes:

* Main schematic and PCB project files
* Local symbol, footprint, and 3D model libraries under `lib/`
* Manufacturing export artifacts under `jlcpcbProduction/`
* Utility scripts under `scripts/` for project-related automation

The goal is to keep everything needed to inspect, edit, and manufacture the board inside this repository.

## Setup

1. Install KiCad (recent stable version recommended).
2. Clone this repository.
3. Open `ChessBoard.kicad_pro` in KiCad.
4. Verify the project libraries resolve correctly (symbols, footprints, and 3D models under `lib/`).

Optional (for helper scripts):

1. Install Python 3.10+.
2. Create and activate a virtual environment.
3. Install script dependencies:

```bash
pip install -r scripts/requirements.txt
```

## Usage

Typical workflow:

1. Open the project in KiCad.
2. Edit schematics in `ChessBoard.kicad_sch` (and related sheets).
3. Update and route the PCB in `ChessBoard.kicad_pcb`.
4. Run DRC/ERC checks before export.
5. Generate manufacturing outputs and keep `jlcpcbProduction/` in sync when changes affect fabrication.

Optional helper scripts can be run from the repository root, for example:

```bash
python scripts/fix3D.py
python scripts/fixColours.py
python scripts/qr_detector.py
```

Review any generated or modified files before committing changes.
