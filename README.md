# About

An interactive chess board hardware design based on Arduino Nano ESP32 and KiCad.

| Top | Bottom |
| :---: | :---: |
| <img alt='PCB top render' src='https://github.com/Odissus/ChessBoard/releases/download/v1.0.0/Image_Top.png' /> | <img alt='PCB bottom render' src='https://github.com/Odissus/ChessBoard/releases/download/v1.0.0/Image_Bottom.png' /> |

> [!TIP]
> If you're just interested in manufacturing your own board, see the quick-start section below

It includes:

* Main schematic and PCB project files
* Local symbol, footprint, and 3D model libraries under `lib/`
* Manufacturing export artifacts under `jlcpcbProduction/`
* Utility scripts under `scripts/` for project-related automation

The goal is to keep everything needed to inspect, edit, and manufacture the board inside this repository.

This PCB is based on [Concept Bytes design](https://concept-bytes.com/products/openchess-pcb), along with their [GitHub repository](https://github.com/Concept-Bytes/Open-Chess). The design is new, although heavily insipired by their work and their guides should work in getting you set up on the embedded development side.

This design is optimised for [JLCPCB](https://jlcpcb.com/) production.

# Quick start

1. Head over to releases, and grab the `JLCPCB_Gerber.zip`, `JLCPCB_Bill_of_materials.csv` and `JLCPCB_Positions.csv` files from the latest release.
1. Heaver over to [JLCPCB](https://jlcpcb.com/) to get and instant PCB quote.
1. Upload the `JLCPCB_Gerber.zip`, let JLC process it.
1. Select your desired `PCB colour` (in PCB Specifications) - they're all free
1. Under High-spec Options, select `Mark on PCB` to `2D barcode Only`.
    1. For `Prefix`, choose a sensible name like `ChessBoard`
    1. For `2D Barcode Size` you must select `10*10mm`
    1. For `2D Barcode Position` select `Specify Position`
1. Select PCB Asembly - there is a choice here
    1. Default - economic. You'll have to source the `74HC595N` shift register yourself from a supplier like Mouser, DigiKey, Farnel or Amazon. Ensure you're buing a DIP-16. This should be relatively easy to solder and will reduce the costs by around 40%.
        1. For `PCBA Type`, select `Economic`
        1. For `Assembly Side`, select `Top Side`
        1. Unless you need 5 assembled boards, reduce `PCBA Qty` to `2`
        1. For `Tooling holes` select `Added by Customer`
    1. Standard. JLC will put the shift register in for you. I have not included edge rails or fiducials in the design.
        1. For `PCBA Type`, select `Standard`
        1. For `Assembly Side`, select `Both Sides`
        1. Unless you need 5 assembled boards, reduce `PCBA Qty` to `2`
        1. For `Edge Rails/Fiducials` select `Added by JLCPCB`. Their engineer will modify the design slightly to include the extra rails.
        1. In the `PCB Remark` section above, add in a note that you'd like to have V-cuts to create snappable edge rails.
1. Review your PCB, and click next
1. Upload `JLCPCB_Bill_of_materials.csv` as your BOM file and `JLCPCB_Positions.csv` as your CPL file. Let JLC process the files.
1. You should get the following different parts (assuming you're making 2 boards):
    - (2 * 64 = ) 128 LEDs 
    - (2 * 8 = ) 16 Resistors
    - (2 * 64 = ) 128 Hall effect sensors 
    - (2 * 1 = ) 2 Shift registers (this will only appear if you pick assembly on both sides)
1. Verify component placement i.e. does any part look out of place. If all is well, select next to get your final manufacture quote.
1. Profit?

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
