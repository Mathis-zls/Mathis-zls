#!/usr/bin/env python3
import os
import sys

# Create directories
os.makedirs(".github/scripts", exist_ok=True)
os.makedirs("assets", exist_ok=True)

# Create blank.png SVG content
blank_svg = """<svg width="50" height="50" xmlns="http://www.w3.org/2000/svg">
  <rect width="50" height="50" fill="#f5f5f5" stroke="#ddd" stroke-width="2"/>
</svg>"""

# Create x-mark.png SVG content
x_svg = """<svg width="50" height="50" xmlns="http://www.w3.org/2000/svg">
  <rect width="50" height="50" fill="#f5f5f5" stroke="#ddd" stroke-width="2"/>
  <line x1="10" y1="10" x2="40" y2="40" stroke="#ff5555" stroke-width="5" stroke-linecap="round"/>
  <line x1="40" y1="10" x2="10" y2="40" stroke="#ff5555" stroke-width="5" stroke-linecap="round"/>
</svg>"""

# Create o-mark.png SVG content
o_svg = """<svg width="50" height="50" xmlns="http://www.w3.org/2000/svg">
  <rect width="50" height="50" fill="#f5f5f5" stroke="#ddd" stroke-width="2"/>
  <circle cx="25" cy="25" r="15" fill="none" stroke="#5555ff" stroke-width="5"/>
</svg>"""

# Save SVG files
with open("assets/blank.png", "w") as f:
    f.write(blank_svg)
    
with open("assets/x-mark.png", "w") as f:
    f.write(x_svg)
    
with open("assets/o-mark.png", "w") as f:
    f.write(o_svg)

print("Asset files created successfully!")