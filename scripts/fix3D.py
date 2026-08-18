import os
import re
import argparse
import pyvista as pv
import numpy as np
import cadquery as cq
from vtkmodules.vtkIOImport import vtkVRMLImporter

def get_wrl_data(path):
    """Extract center and bounding box size from WRL via VTK."""
    try:
        importer = vtkVRMLImporter()
        importer.SetFileName(path)
        importer.Update()
        renderer = importer.GetRenderer()
        actors = renderer.GetActors()
        actors.InitTraversal()
        
        meshes = []
        for _ in range(actors.GetNumberOfItems()):
            actor = actors.GetNextActor()
            if actor and actor.GetMapper():
                poly = actor.GetMapper().GetInput()
                if poly:
                    meshes.append(pv.wrap(poly))
        
        if not meshes: return None, None
        combined = meshes[0].merge(meshes[1:]) if len(meshes) > 1 else meshes[0]
        b = combined.bounds
        center = np.array([(b[0]+b[1])/2, (b[2]+b[3])/2, (b[4]+b[5])/2])
        size = np.array([b[1]-b[0], b[3]-b[2], b[5]-b[4]])
        return center, size
    except Exception as e:
        print(f"  [!] Error reading WRL: {e}")
        return None, None

def calculate_step_offset(step_path, wrl_path):
    """Returns the (x, y, z) offset needed for the STEP model."""
    try:
        w_center, w_size = get_wrl_data(wrl_path)
        if w_center is None: return None

        step_obj = cq.importers.importStep(step_path)
        bb = step_obj.val().BoundingBox()
        s_center = np.array([bb.center.x, bb.center.y, bb.center.z])
        s_size = np.array([bb.xlen, bb.ylen, bb.zlen])

        scale_factor = s_size[0] / w_size[0]
        target_center_mm = w_center * scale_factor
        
        offset = target_center_mm - s_center
        return offset
    except Exception as e:
        print(f"  [!] Geometry Error: {e}")
        return None

def process_pcb(pcb_path, kiprjmod_path):
    if not os.path.exists(pcb_path):
        print(f"PCB file not found: {pcb_path}")
        return

    with open(pcb_path, 'r') as f:
        lines = f.readlines()

    modified_count = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        
        wrl_match = re.search(r'\(model\s+"([^"]+\.wrl)"', line)
        
        if wrl_match:
            wrl_path_raw = wrl_match.group(1)
            # Use the passed kiprjmod_path for resolution
            local_wrl_path = wrl_path_raw.replace('${KIPRJMOD}', kiprjmod_path)
            local_step_path = os.path.splitext(local_wrl_path)[0] + ".step"
            step_rel_path = os.path.splitext(wrl_path_raw)[0] + ".step"

            if os.path.exists(local_step_path):
                print(f"Replacing WRL with STEP: {os.path.basename(local_step_path)}")
                offset = calculate_step_offset(local_step_path, local_wrl_path)
                
                if offset is not None:
                    start_index = i
                    brace_depth = line.count('(') - line.count(')')
                    end_index = -1
                    
                    for j in range(i + 1, len(lines)):
                        brace_depth += lines[j].count('(')
                        brace_depth -= lines[j].count(')')
                        if brace_depth <= 0:
                            end_index = j
                            break
                    
                    if end_index != -1:
                        step_block = (
                            f'    (model "{step_rel_path}"\n'
                            f'      (offset (xyz {offset[0]:.6f} {offset[1]:.6f} {offset[2]:.6f}))\n'
                            f'      (scale (xyz 1 1 1))\n'
                            f'      (rotate (xyz 0 0 0))\n'
                            f'    )\n'
                        )
                        
                        del lines[start_index : end_index + 1]
                        lines.insert(start_index, step_block)
                        
                        modified_count += 1
                        print(f"  -> Swap successful. Offset: {offset}")
                        i = start_index
        i += 1

    if modified_count > 0:
        with open(pcb_path, 'w') as f:
            f.writelines(lines)
        print(f"\nSuccess: Replaced {modified_count} WRL models in {pcb_path}")
    else:
        print("\nNo WRL models found to replace.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace KiCad WRL models with aligned STEP models.")
    parser.add_argument("--kiprjmod", required=True, help="Path to the project root (${KIPRJMOD})")
    parser.add_argument("--pcb", required=True, help="Path to the .kicad_pcb file")
    
    args = parser.parse_args()

    # Resolve paths to absolute to avoid relative path confusion in Docker/Actions
    abs_kiprjmod = os.path.abspath(args.kiprjmod)
    abs_pcb = os.path.abspath(args.pcb)

    process_pcb(abs_pcb, abs_kiprjmod)