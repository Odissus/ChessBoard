import sys
import os
import argparse

def modify_stackup(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_stackup = """        (stackup
            (layer "F.SilkS" (type "Top Silk Screen"))
            (layer "F.Paste" (type "Top Solder Paste"))
            (layer "F.Mask" (type "Top Solder Mask") (color "#333333FF") (thickness 0.01))
            (layer "F.Cu" (type "copper") (thickness 0.035))
            (layer "dielectric 1" (type "core")  (thickness 1.51) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
            (layer "B.Cu" (type "copper") (thickness 0.035))
            (layer "B.Mask" (type "Bottom Solder Mask") (color "#333333FF") (thickness 0.01))
            (layer "B.Paste" (type "Bottom Solder Paste"))
            (layer "B.SilkS" (type "Bottom Silk Screen"))
            (copper_finish "None")
            (dielectric_constraints no)
        )\n"""

    output = []
    in_setup = False
    has_stackup = any("(stackup" in line for line in lines)
    
    # If it already has a stackup, we need to skip the old one first
    skip_mode = False
    brace_count = 0

    for line in lines:
        # Detect start of setup
        if "(setup" in line:
            in_setup = True
            output.append(line)
            if not has_stackup:
                output.append(new_stackup)
            continue
        
        # If we are replacing an existing stackup
        if has_stackup and "(stackup" in line:
            skip_mode = True
            output.append(new_stackup)
        
        if skip_mode:
            brace_count += line.count('(')
            brace_count -= line.count(')')
            if brace_count <= 0:
                skip_mode = False
            continue

        output.append(line)

    with open(file_path, 'w') as f:
        f.writelines(output)
    print(f"Successfully updated stackup in {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace KiCad WRL models with aligned STEP models.")
    parser.add_argument("--pcb", required=True, help="Path to the .kicad_pcb file")
    args = parser.parse_args()
    abs_pcb = os.path.abspath(args.pcb)
    modify_stackup(abs_pcb) 