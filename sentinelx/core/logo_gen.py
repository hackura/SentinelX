import os

def generate_svg_logo(output_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.svg")):
    # Ensure assets directory exists
    dir_name = os.path.dirname(output_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    # Simple SVG template
    svg_content = r"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="600" height="150" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="100%" height="100%" fill="#111111" rx="15" ry="15"/>
  
  <!-- Text Shadow -->
  <text x="50%" y="65%" font-family="Courier New, monospace" font-size="60" 
        font-weight="bold" fill="#000000" text-anchor="middle" opacity="0.5" 
        transform="translate(4,4)">SENTINELX</text>
  
  <!-- Main Text with Gradient -->
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#ff0000;stop-opacity:1" /> <!-- Red -->
      <stop offset="50%" style="stop-color:#9900ff;stop-opacity:1" /> <!-- Purple -->
      <stop offset="100%" style="stop-color:#0000ff;stop-opacity:1" /> <!-- Blue -->
    </linearGradient>
  </defs>
  <text x="50%" y="65%" font-family="Courier New, monospace" font-size="60" 
        font-weight="bold" fill="url(#grad1)" text-anchor="middle">SENTINELX</text>
        
  <!-- Version Tag -->
  <text x="85%" y="85%" font-family="Arial, sans-serif" font-size="14" 
        fill="#aaaaaa" text-anchor="end">v2.0</text>
</svg>"""

    with open(output_path, "w") as f:
        f.write(svg_content)

    return os.path.abspath(output_path)

if __name__ == "__main__":
    path = generate_svg_logo()
    print(f"Logo generated at: {path}")
