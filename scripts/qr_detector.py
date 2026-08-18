import re
import argparse
import os

sizes = [
    (5, 5),
    (8, 8),
    (10, 10),
]


def parse_pcb_for_silkscreen_elements(pcb_path):
    """Parses the .kicad_pcb file to find silkscreen elements and their bounding boxes."""
    with open(pcb_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # This pattern looks for (gr_text
    # Then matches everything until it finds a ')' 
    # that is at the start of a line or specific indentation.
    pattern = r"\(gr_rect"

    # Using re.DOTALL to allow '.' to match newlines
    # Using re.MULTILINE to allow '^' to match start of lines
    matches = re.finditer(pattern, content, flags=re.DOTALL)

    gr_rects = []

    for match in matches:
        start_index = match.start()
        end_index = match.end()
        parenthesis_count = 0
        for i in range(start_index + 1, len(content)):
            if content[i] == '(':
                parenthesis_count += 1
            elif content[i] == ')':
                if parenthesis_count == 0:
                    end_index = i + 1
                    break
                else:
                    parenthesis_count -= 1
        text = content[start_index:end_index]
        gr_rects.append(text)

    params = []
    valid_rects = []

    for gr_rect in gr_rects:
        if ("fill yes" in gr_rect or "fill solid" in gr_rect) and ('layer "F.SilkS"' in gr_rect or 'layer "B.SilkS"' in gr_rect):
            temp_params = []
            start_match = re.search(r'\(start\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\)', gr_rect)
            end_match = re.search(r'\(end\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\)', gr_rect)
            if start_match:
                x = float(start_match.group(1))
                y = float(start_match.group(2))
                temp_params.append((x, y))
            if end_match:
                x = float(end_match.group(1))
                y = float(end_match.group(2))
                temp_params.append((x, y))
            if len(temp_params) == 2:
                params.append(temp_params)
                valid_rects.append(gr_rect)
    
    valid_qr_code_areas = []
    for i, param in enumerate(params):
        width = abs(param[1][0] - param[0][0])
        height = abs(param[1][1] - param[0][1])
        for size in sizes:
            if abs(width - size[0]) < 0.001 and abs(height - size[1]) < 0.001:
                valid_qr_code_areas.append(valid_rects[i])
    return valid_qr_code_areas

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace KiCad WRL models with aligned STEP models.")
    parser.add_argument("--pcb", required=True, help="Path to the .kicad_pcb file")
    parser.add_argument("--crash-if-not-one", default=False, action='store_true', help="If set, the script will raise an error if it does not find exactly one valid QR code area.")
    args = parser.parse_args()
    abs_pcb = os.path.abspath(args.pcb)
    areas = parse_pcb_for_silkscreen_elements(abs_pcb)
    if args.crash_if_not_one and len(areas) != 1:
        raise ValueError(f"Expected exactly one valid QR code area, but found {len(areas)}.")