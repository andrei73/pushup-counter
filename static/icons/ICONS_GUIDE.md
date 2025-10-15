# PWA Icons Guide

## Icons Needed

You need to create icons in the following sizes. All should be PNG format with transparent or colored background.

### Required Sizes:
- icon-72x72.png
- icon-96x96.png
- icon-128x128.png
- icon-144x144.png
- icon-152x152.png
- icon-192x192.png
- icon-384x384.png
- icon-512x512.png
- apple-touch-icon.png (180x180)
- favicon.ico (32x32)

## Quick Ways to Generate Icons

### Option 1: Use an Icon Generator (Easiest)
Visit: https://realfavicongenerator.net/
1. Upload a 512x512 image
2. Configure settings
3. Download all sizes automatically

### Option 2: Use PWA Asset Generator
```bash
npm install -g pwa-asset-generator
pwa-asset-generator your-logo.png ./icons
```

### Option 3: Manual Creation
Use any design tool (Figma, Photoshop, Canva) to create a 512x512 icon, then resize for other dimensions.

## Design Suggestions

For a pushup counter app, consider:
- 💪 Flexed bicep icon
- 📊 Graph going up
- 🏆 Trophy
- ❤️ Heart with pulse (matches your logo)
- 🔥 Flame (for streaks)

Use your brand colors:
- Primary: #667eea (purple)
- Secondary: #764ba2 (darker purple)
- Accent: #10b981 (green)

## Temporary Solution

For now, you can use a solid colored square with text/emoji:
- Background: #667eea
- Text: "💪" or "PC" (Pushup Counter)
- This works fine until you create custom icons!

## iOS Specific

Apple Touch Icon (apple-touch-icon.png):
- Size: 180x180
- Should NOT be transparent
- Add slight padding/margin
- Apple adds rounded corners automatically

