# Dinosaur Pet 🦕

A cross-platform Python desktop application for creating and caring for virtual dinosaur pets. Designed with neurodivergent children in mind, featuring intuitive file-based dinosaur creation and efficient graphics rendering.

## Features

- **Modular Image System**: Build dinosaurs from separate parts (head, legs, arms, tail, body)
- **Animation Support**: Frame-based animations (e.g., `legs_01.png`, `legs_02.png`)
- **Variant System**: Multiple appearances for each part (e.g., `head/happy.png`, `head/angry.png`)
- **Efficient Rendering**: Direct RGBA manipulation with NumPy for smooth performance
- **Simple Stats**: Extensible stats system (currently: hunger)
- **Interactive Pet**: Feed, play, and watch your dinosaur move around
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python dino_pet.py
```

## Requirements

- Python 3.8+
- NumPy
- Pillow (PIL)
- tkinter (usually included with Python)

## Creating Your Dinosaur

### Quick Start

The simplest dinosaur is just a single PNG file:

```
my_dino.png
```

Click "🥚 Hatch New" and select this file.

### Adding Parts

Create a folder structure like this:

```
my_dino/
  dino.png          # Main body
  head/
    happy.png       # Happy expression
    angry.png       # Angry expression
  legs/
    walk_01.png     # Walking animation frame 1
    walk_02.png     # Walking animation frame 2
```

Click "🥚 Hatch New" and select the folder.

### File Naming Conventions

#### Single Images
- `dino.png` - Main body
- `head.png` - Single head image
- `legs.png` - Single legs image
- `arms.png` - Single arms image
- `tail.png` - Single tail image

#### Variants (Folder-based)
```
head/
  happy.png
  angry.png
  sleepy.png
```

#### Animation Frames (Numbered)
- `legs_01.png`, `legs_02.png`, `legs_03.png`
- Frame numbers can be any length: `_01`, `_001`, etc.

#### Combined: Variants with Animation
```
legs/
  walk_01.png
  walk_02.png
  run_01.png
  run_02.png
  run_03.png
```

Or with color variants:
```
legs/
  blue_01.png
  blue_02.png
  green_01.png
  green_02.png
```

### Incremental Creation

You can start simple and add complexity:

1. Start with `dino.png` (single image)
2. Add a second image → automatically becomes variants (`dino/a.png`, `dino/b.png`)
3. Add more parts using "➕ Add Parts"

### Image Requirements

- **Format**: PNG with transparency (RGBA)
- **Anchor Point**: Currently center of image (w/2, h/2)
- **Size**: Any size, but keep it reasonable (100-500px typical)
- **Asymmetry**: Add left/right or top/bottom asymmetry so flipping is visible

## Usage

### Controls

- **🥚 Hatch New**: Load a new dinosaur from file or folder
- **➕ Add Parts**: Add more images to your current dinosaur
- **🍎 Feed**: Increase hunger by 20 points
- **✨ Play**: Make your dinosaur move to a random location
- **Appearance**: Change variants (appears when multiple variants available)

### Stats

- **Hunger**: Decreases by 1 every 5 seconds
- Feed your dinosaur to keep it happy!

### Behavior

- Dinosaurs move around randomly
- They bounce when fed
- They face the direction they're moving
- Animation frames cycle when moving

## Technical Details

### Architecture

- **dino_loader.py**: Image loading and data structures
  - Handles all file naming conventions
  - Organizes parts, variants, and frames
  - Cross-platform path handling with `pathlib`

- **renderer.py**: Efficient graphics rendering
  - Direct NumPy RGBA manipulation
  - Alpha compositing for layered images
  - Nearest-neighbor interpolation (fast)
  - Double-buffered rendering

- **dino_pet.py**: Main GUI application
  - Tkinter-based interface
  - 60 FPS animation loop
  - Physics simulation (movement, gravity, bounce)

### Performance Optimizations

- Direct RGBA byte manipulation (no per-pixel object creation)
- NumPy vectorized operations for alpha compositing
- Efficient canvas clearing and compositing
- Double buffering to prevent flicker

### Rendering Pipeline

1. Clear canvas to background color
2. Render parts in order: tail → dino → legs → arms → head
3. For each part:
   - Get current variant and frame
   - Apply transformations (flip, scale)
   - Composite onto canvas using alpha blending
4. Convert NumPy array to PIL Image
5. Display in Tkinter Canvas

### Anchor Points

Currently, all images use their center point (w/2, h/2) as the anchor. This is where the image attaches to the skeleton. Future versions will support custom anchor points per image.

## Example: Test Dinosaur

A test dinosaur is included in `test_dino/`:

```
test_dino/
  dino.png              # Green rectangular body with tail
  head/
    happy.png           # Smiling face
    angry.png           # Angry face
  legs/
    walk_01.png         # Walking frame 1
    walk_02.png         # Walking frame 2
```

Load it with "🥚 Hatch New" → select `test_dino` folder.

## Extending the Program

### Adding New Stats

Edit `dino_loader.py`:

```python
self.stats = {
    'hunger': 50,
    'happiness': 75,
    'energy': 100
}
```

### Adding New Parts

The system automatically recognizes any part name:
- `wings.png` or `wings/` folder
- `horns.png` or `horns/` folder
- Any name you want!

Update `renderer.py` render order if needed:

```python
render_order = ['tail', 'wings', 'dino', 'legs', 'arms', 'head', 'horns']
```

### Custom Anchor Points

Future enhancement - will support per-image anchor points for proper skeletal attachment (e.g., head anchor at neck position).

## Design Philosophy

This program was designed for children (ages 8-9) with ADHD/autism:

- **Intuitive**: No complex menus or configuration files
- **Visual**: See your dinosaur immediately
- **Flexible**: Start simple, add complexity gradually
- **Forgiving**: No wrong way to create a dinosaur
- **Engaging**: Interactive and animated
- **Child-friendly language**: "Hatch" instead of "Import", "Add Parts" instead of "Merge Assets"

## Troubleshooting

### "No module named 'PIL'"
```bash
pip install Pillow
```

### "No module named 'numpy'"
```bash
pip install numpy
```

### Images not loading
- Check file format (must be PNG)
- Check file names (case-sensitive on Linux/macOS)
- Check folder structure matches examples

### Dinosaur not visible
- Make sure images have non-transparent pixels
- Check image size (very large images may be off-screen)
- Try the included `test_dino` first

## Future Enhancements

- Custom anchor points for skeletal attachment
- Rotation support
- Bilinear/bicubic interpolation
- Save/load dinosaur state
- Multiple dinosaurs on screen
- Mini-games
- Sound effects
- Export dinosaur as GIF animation

## License

Free to use and modify for personal and educational purposes.

---

Made with ❤️ for dinosaur-loving kids everywhere! 🦖
