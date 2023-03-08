import os
from xml.etree.ElementTree import Element, SubElement, tostring
import uuid

def create_svg_file(text,folder='caption_assets'):
        # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Set up the SVG namespace
    x=50.0
    y=270.45352
    svg_template=f"""
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="2000" height="1920" id="svg2985">
  <g id="layer1">
    <text style="font-size:20px;font-style:normal;font-weight:normal;line-height:100%;letter-spacing:0px;word-spacing:0px;fill:#c9b23a;fill-opacity:1;stroke:none;font-family:Sans;word-wrap: break-word;"
     x="80" y="900" id="tspan2995">
    {text}
    </text>
  </g>
</svg>"""

    unique_filename = str(uuid.uuid4())
    # Save the SVG to a file in the media_assets folder
    filename = f"{unique_filename}.svg"
    filepath = os.path.join(folder, filename)
    with open(filepath, "w") as f:
        f.write(svg_template)

    # Return the path to the SVG file
    return filepath

if __name__ =="__main__":
    text = "To address these challenges, farmers and agricultural organizations are adopting new technologies and practices to increase efficiency and sustainability."
    create_svg_file(text,"caption_assets")