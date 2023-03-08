import os
from xml.etree.ElementTree import Element, SubElement, tostring
import uuid

def create_svg_file(text,folder='caption_assets'):
        # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # text1 = text
    # text2 = ""
    # Set up the SVG namespace
    svg_template=f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   inkscape:version="1.2.2 (732a01da63, 2022-12-09)"
   sodipodi:docname="template.svg"
   id="svg2985"
   height="1080"
   width="1920"
   version="1.1"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs8">
    <linearGradient
       inkscape:collect="always"
       id="linearGradient2607">
      <stop
         style="stop-color:#000000;stop-opacity:1;"
         offset="0"
         id="stop2603" />
      <stop
         style="stop-color:#000000;stop-opacity:0;"
         offset="1"
         id="stop2605" />
    </linearGradient>
    <filter
       inkscape:collect="always"
       style="color-interpolation-filters:sRGB"
       id="filter2576"
       x="-5.1326297e-05"
       y="-0.00090981733"
       width="1.0001027"
       height="1.0018196">
      <feGaussianBlur
         inkscape:collect="always"
         stdDeviation="0.040626866"
         id="feGaussianBlur2578" />
    </filter>
    <linearGradient
       inkscape:collect="always"
       xlink:href="#linearGradient2607"
       id="linearGradient2609"
       x1="-706.2847"
       y1="855.49687"
       x2="1193.6088"
       y2="855.49687"
       gradientUnits="userSpaceOnUse" />
  </defs>
  <sodipodi:namedview
     id="namedview6"
     pagecolor="#ffffff"
     bordercolor="#000000"
     borderopacity="0.25"
     inkscape:showpageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="0"
     inkscape:deskcolor="#d1d1d1"
     showgrid="false"
     inkscape:zoom="0.63020833"
     inkscape:cx="1028.2314"
     inkscape:cy="576"
     inkscape:window-width="1920"
     inkscape:window-height="1009"
     inkscape:window-x="1912"
     inkscape:window-y="-8"
     inkscape:window-maximized="1"
     inkscape:current-layer="layer1" />
  <g
     id="layer1"
     transform="matrix(0.98145208,0,0,1.5990767,626.44431,-493.69103)">
    <a
       id="a2572"
       style="mix-blend-mode:normal;fill:#0e2960;fill-opacity:0.889401;stroke:none;filter:url(#filter2576);image-rendering:pixelated"
       transform="translate(92.155576,14.884622)">
      <title
         id="title2574">subtitlebox</title>
      <rect
         style="fill:#0e2960;fill-opacity:0.889401;stroke:none;stroke-width:0.845484"
         id="rect5525"
         width="1899.6982"
         height="107.16929"
         x="-706.18719"
         y="801.91223"
         ry="41.796021"
         rx="41.796021" />
    </a>
    <text
       style="font-style:normal;font-weight:normal;font-size:14.7625px;line-height:100%;font-family:Sans;letter-spacing:0px;word-spacing:0px;white-space:pre;inline-size:1234.17;fill:#ffd42a;fill-opacity:0.941176;stroke:none;stroke-width:0.667821"
       x="347.60501"
       y="917.86157"
       text-anchor="middle"
       id="text2"
       transform="matrix(1.5270729,0,0,1.3903789,-212.10771,-443.309)"
       xml:space="preserve">
       <tspan
         x="347.60501"
         y="917.86157"
         id="tspan2626">
</tspan><tspan
         x="347.60501"
         y="932.62406"
         id="tspan2628">       
</tspan>
<tspan
         x="350.0"
         y="950.0"
         id="tspan2632">
<tspan
   style="font-weight:bold;font-size:15px;font-family:sans-serif;-inkscape-font-specification:'sans-serif Bold'"
   id="tspan2630">{text}
</tspan>
</tspan>
   </text>
  </g>
</svg>
"""

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