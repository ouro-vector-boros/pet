# Getting Started with Dinosaur Pet 🦖

Hi! This guide will help you and your son start playing with Dinosaur Pet right away.

## Quick Start (5 minutes)

### Step 1: Install Python

If you don't have Python installed:

- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: Python is usually pre-installed, or use [python.org](https://www.python.org/downloads/)
- **Linux**: Usually pre-installed, or use your package manager

### Step 2: Install the Program

Open a terminal/command prompt and run:

```bash
# Navigate to the dino-pet-python folder
cd path/to/dino-pet-python

# Install requirements
pip install -r requirements.txt
```

### Step 3: Run It!

```bash
python dino_pet.py
```

A window will open with the dinosaur pet program!

### Step 4: Hatch Your First Dinosaur

1. Click the "🥚 Hatch New" button
2. Navigate to the `test_dino` folder (included)
3. Select the folder
4. Your dinosaur appears!

Now you can:
- Click "🍎 Feed" to feed it
- Click "✨ Play" to make it move
- Change its expression using the "Appearance" dropdown (happy/angry)

## Creating Your Own Dinosaurs

This is the fun part! You can create dinosaurs together.

### Super Simple Method

1. Draw a dinosaur in any drawing program (Paint, Procreate, etc.)
2. Save it as a PNG file (with transparency if possible)
3. Name it `my_dino.png`
4. Click "🥚 Hatch New" and select your file

Done! Your dinosaur is alive!

### Adding Expressions

Want your dinosaur to have different faces?

1. Create a folder called `my_awesome_dino`
2. Inside, create another folder called `head`
3. Draw different heads:
   - `happy.png` - smiling face
   - `angry.png` - grumpy face
   - `sleepy.png` - tired face
   - `silly.png` - goofy face
4. Also add `dino.png` for the body
5. Click "🥚 Hatch New" and select the `my_awesome_dino` folder

Now you can change expressions in the program!

### Making It Walk

Want walking animation?

1. In your dinosaur folder, create a `legs` folder
2. Draw the legs in different positions:
   - `walk_01.png` - legs in position 1
   - `walk_02.png` - legs in position 2
   - `walk_03.png` - legs in position 3

The legs will animate when your dinosaur moves!

## Tips for Drawing

- **Use transparency**: Save as PNG with transparent background
- **Make it asymmetric**: Put the eye on one side so you can tell when it flips
- **Keep it simple**: Start with basic shapes
- **Size**: 100-200 pixels is a good size
- **Have fun**: There's no wrong way to make a dinosaur!

## Ideas for Your Son

Here are some fun things to try together:

1. **Rainbow Dinosaur**: Make different colored body variants
   ```
   my_dino/
     dino/
       red.png
       blue.png
       green.png
   ```

2. **Mood Dinosaur**: Lots of different expressions
   ```
   my_dino/
     head/
       happy.png
       sad.png
       excited.png
       surprised.png
       silly.png
   ```

3. **Action Dinosaur**: Different leg animations
   ```
   my_dino/
     legs/
       walk_01.png, walk_02.png
       run_01.png, run_02.png
       jump_01.png, jump_02.png
   ```

4. **Fancy Dinosaur**: Add all the parts!
   ```
   my_dino/
     dino.png
     head/happy.png, angry.png
     legs/walk_01.png, walk_02.png
     arms/wave_01.png, wave_02.png
     tail/wag_01.png, wag_02.png
   ```

## Troubleshooting

**"It won't install"**
- Make sure Python is installed: `python --version`
- Try `pip3` instead of `pip`

**"I can't see my dinosaur"**
- Make sure the image has some color (not all transparent)
- Try the test_dino first to make sure the program works
- Check that your file is PNG format

**"The animations don't work"**
- Make sure files are named with numbers: `_01`, `_02`, etc.
- Numbers should be at the end of the filename

**"It's too slow"**
- Try smaller images (under 500x500 pixels)
- Close other programs

## For Parents

This program was designed to be:
- **Sensory-friendly**: No sudden sounds or flashing
- **Predictable**: Consistent behavior and controls
- **Creative**: Open-ended dinosaur creation
- **Collaborative**: Work together to create dinosaurs
- **Educational**: Learn about files, folders, and basic programming concepts

The file-based system teaches:
- File organization
- Naming conventions
- Cause and effect (change file → change dinosaur)
- Sequential thinking (animation frames)

## Next Steps

Once you're comfortable:
- Try editing `dino_pet.py` to change colors or behaviors
- Add new stats (happiness, energy)
- Create a collection of dinosaurs
- Share dinosaurs with friends (just share the folder!)

Have fun! 🦕✨
