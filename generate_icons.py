#!/usr/bin/env python3
"""
Simple script to generate placeholder PWA icons.
Requires: pip install pillow

Creates basic colored squares with emoji/text as temporary icons.
Replace these with professionally designed icons later!
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("Please install Pillow: pip install pillow")
    exit(1)

# Icon sizes needed
SIZES = [72, 96, 128, 144, 152, 180, 192, 384, 512]

# Colors (your app's theme)
BG_COLOR = (102, 126, 234)  # #667eea purple
TEXT_COLOR = (255, 255, 255)  # white

# Output directory
OUTPUT_DIR = 'static/icons'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_icon(size, text="💪"):
    """Create a simple icon with text/emoji on colored background."""
    
    # Create image with colored background
    img = Image.new('RGB', (size, size), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Try to add text (might not work with emoji on all systems)
    try:
        # Calculate font size (roughly 60% of image size)
        font_size = int(size * 0.6)
        
        # Try to use a system font
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Use default font if no truetype available
                font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        # Draw text
        draw.text((x, y), text, fill=TEXT_COLOR, font=font)
    except Exception as e:
        print(f"Warning: Could not add text to {size}x{size} icon: {e}")
    
    return img

def main():
    print("🎨 Generating PWA icons...")
    print(f"Output directory: {OUTPUT_DIR}")
    print()
    
    for size in SIZES:
        filename = f"icon-{size}x{size}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Create icon
        icon = create_icon(size)
        
        # Save
        icon.save(filepath, 'PNG')
        print(f"✅ Created: {filename}")
    
    # Create apple-touch-icon (180x180)
    apple_icon = create_icon(180)
    apple_icon.save(os.path.join(OUTPUT_DIR, 'apple-touch-icon.png'), 'PNG')
    print(f"✅ Created: apple-touch-icon.png")
    
    # Create favicon (32x32 as PNG, then convert to ICO if possible)
    favicon = create_icon(32, "💪")
    favicon_path = os.path.join(OUTPUT_DIR, 'favicon.png')
    favicon.save(favicon_path, 'PNG')
    print(f"✅ Created: favicon.png")
    
    # Try to create favicon.ico
    try:
        favicon.save(os.path.join(OUTPUT_DIR, 'favicon.ico'), 'ICO')
        print(f"✅ Created: favicon.ico")
    except:
        print(f"⚠️  Could not create favicon.ico, using PNG instead")
    
    print()
    print("🎉 Done! All icons created.")
    print()
    print("These are placeholder icons. For production:")
    print("1. Use a design tool (Figma, Canva, etc.)")
    print("2. Create a professional 512x512 icon")
    print("3. Use https://realfavicongenerator.net/ to generate all sizes")
    print()

if __name__ == '__main__':
    main()

