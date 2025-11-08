#!/usr/bin/env python3
"""
Dinosaur Pet - Interactive virtual pet application
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from pathlib import Path
import time

from dino_loader import DinoData, load_dinosaur, add_to_dinosaur
from renderer import create_canvas, clear_canvas, render_dinosaur, canvas_to_pil


class DinoPet:
    """Main application class."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Dinosaur Pet")
        self.root.geometry("800x600")
        
        # Current dinosaur
        self.dino: DinoData = None
        
        # Rendering state
        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas_buffer = create_canvas(self.canvas_width, self.canvas_height)
        
        # Animation state
        self.dino_x = self.canvas_width // 2
        self.dino_y = self.canvas_height // 2
        self.dino_flip = False
        self.dino_scale = 1.0
        
        # Current variants and frames for each part
        self.current_variants = {}
        self.current_frames = {}
        self.frame_counter = 0
        
        # Movement
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.target_x = self.dino_x
        self.target_y = self.dino_y
        
        # Timing
        self.last_update = time.time()
        self.last_hunger_decrease = time.time()
        
        # Build UI
        self.setup_ui()
        
        # Start animation loop
        self.animate()
    
    def setup_ui(self):
        """Create the user interface."""
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side: Canvas for dinosaur
        canvas_frame = tk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=2)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg='#87CEEB'  # Sky blue
        )
        self.canvas.pack()
        
        # Placeholder image
        self.photo_image = None
        self.canvas_image_id = None
        
        # Right side: Controls
        control_frame = tk.Frame(main_frame, width=200)
        control_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        control_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(control_frame, text="Dino Pet", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Dino name
        self.name_label = tk.Label(control_frame, text="No dino yet!", font=('Arial', 12))
        self.name_label.pack(pady=5)
        
        # Stats
        stats_frame = tk.LabelFrame(control_frame, text="Stats", padx=10, pady=10)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.hunger_label = tk.Label(stats_frame, text="Hunger: --")
        self.hunger_label.pack()
        
        # Actions
        actions_frame = tk.LabelFrame(control_frame, text="Actions", padx=10, pady=10)
        actions_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(actions_frame, text="🍎 Feed", command=self.feed, width=15).pack(pady=2)
        tk.Button(actions_frame, text="✨ Play", command=self.play, width=15).pack(pady=2)
        
        # Dino management
        dino_frame = tk.LabelFrame(control_frame, text="Dinosaur", padx=10, pady=10)
        dino_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(dino_frame, text="🥚 Hatch New", command=self.hatch_new, width=15).pack(pady=2)
        tk.Button(dino_frame, text="➕ Add Parts", command=self.add_parts, width=15).pack(pady=2)
        
        # Variant selector (dynamic)
        self.variant_frame = tk.LabelFrame(control_frame, text="Appearance", padx=10, pady=5)
        self.variant_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.variant_widgets = {}
    
    def update_variant_controls(self):
        """Update variant selection controls based on current dino."""
        # Clear existing widgets
        for widget in self.variant_frame.winfo_children():
            widget.destroy()
        self.variant_widgets.clear()
        
        if self.dino is None:
            return
        
        # Create controls for each part that has variants
        for part_name in self.dino.parts.keys():
            variants = self.dino.get_available_variants(part_name)
            if len(variants) <= 1:
                continue  # Skip if only one or no variants
            
            # Create label and dropdown
            frame = tk.Frame(self.variant_frame)
            frame.pack(fill=tk.X, pady=2)
            
            label = tk.Label(frame, text=f"{part_name.capitalize()}:", width=8, anchor='w')
            label.pack(side=tk.LEFT)
            
            var = tk.StringVar(value=str(self.current_variants.get(part_name, variants[0])))
            
            # Convert None to "default" for display
            display_variants = [str(v) if v is not None else "default" for v in variants]
            
            dropdown = tk.OptionMenu(
                frame,
                var,
                *display_variants,
                command=lambda val, pn=part_name: self.change_variant(pn, val)
            )
            dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            self.variant_widgets[part_name] = var
    
    def change_variant(self, part_name: str, variant_str: str):
        """Change the variant for a specific part."""
        # Convert "default" back to None
        variant = None if variant_str == "default" else variant_str
        self.current_variants[part_name] = variant
    
    def hatch_new(self):
        """Load a new dinosaur from file or directory."""
        path = filedialog.askopenfilename(
            title="Select dinosaur image",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if not path:
            # Try directory selection
            path = filedialog.askdirectory(title="Select dinosaur folder")
        
        if not path:
            return
        
        try:
            self.dino = load_dinosaur(Path(path))
            self.name_label.config(text=self.dino.name)
            
            # Reset state
            self.current_variants.clear()
            self.current_frames.clear()
            self.frame_counter = 0
            
            # Initialize variants to defaults
            for part_name in self.dino.parts.keys():
                variants = self.dino.get_available_variants(part_name)
                if variants:
                    self.current_variants[part_name] = variants[0]
            
            self.update_variant_controls()
            self.update_stats_display()
            
            messagebox.showinfo("Success", f"Hatched {self.dino.name}!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to hatch dinosaur: {e}")
    
    def add_parts(self):
        """Add parts to existing dinosaur."""
        if self.dino is None:
            messagebox.showwarning("No Dino", "Hatch a dinosaur first!")
            return
        
        path = filedialog.askopenfilename(
            title="Select part image",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if not path:
            path = filedialog.askdirectory(title="Select parts folder")
        
        if not path:
            return
        
        try:
            add_to_dinosaur(self.dino, Path(path))
            self.update_variant_controls()
            messagebox.showinfo("Success", "Parts added!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add parts: {e}")
    
    def feed(self):
        """Feed the dinosaur."""
        if self.dino is None:
            return
        
        self.dino.stats['hunger'] = min(100, self.dino.stats.get('hunger', 50) + 20)
        self.update_stats_display()
        
        # Bounce animation
        self.velocity_y = -5
    
    def play(self):
        """Play with the dinosaur."""
        if self.dino is None:
            return
        
        # Random movement
        import random
        self.target_x = random.randint(100, self.canvas_width - 100)
        self.target_y = random.randint(100, self.canvas_height - 100)
    
    def update_stats_display(self):
        """Update stats labels."""
        if self.dino is None:
            self.hunger_label.config(text="Hunger: --")
        else:
            hunger = self.dino.stats.get('hunger', 50)
            self.hunger_label.config(text=f"Hunger: {hunger}/100")
    
    def update_physics(self, dt: float):
        """Update dinosaur position and physics."""
        if self.dino is None:
            return
        
        # Move toward target
        dx = self.target_x - self.dino_x
        dy = self.target_y - self.dino_y
        dist = (dx**2 + dy**2)**0.5
        
        if dist > 5:
            speed = 50.0  # pixels per second
            self.velocity_x = (dx / dist) * speed
            self.velocity_y = (dy / dist) * speed
            
            # Update facing direction
            if dx > 0:
                self.dino_flip = False
            elif dx < 0:
                self.dino_flip = True
        else:
            self.velocity_x *= 0.9
            self.velocity_y *= 0.9
        
        # Apply velocity
        self.dino_x += self.velocity_x * dt
        self.dino_y += self.velocity_y * dt
        
        # Gravity for bounce
        self.velocity_y += 200 * dt  # gravity
        
        # Ground collision
        if self.dino_y > self.canvas_height - 100:
            self.dino_y = self.canvas_height - 100
            self.velocity_y *= -0.5  # bounce
            if abs(self.velocity_y) < 1:
                self.velocity_y = 0
        
        # Bounds
        self.dino_x = max(50, min(self.canvas_width - 50, self.dino_x))
        self.dino_y = max(50, min(self.canvas_height - 50, self.dino_y))
        
        # Animate frames (cycle through animation frames)
        if dist > 5:  # Only animate when moving
            self.frame_counter += dt * 10  # 10 fps for animation
            for part_name in self.current_frames.keys():
                part_frames = self.dino.get_part_frames(part_name, self.current_variants.get(part_name))
                if part_frames and part_frames.frame_count > 1:
                    self.current_frames[part_name] = int(self.frame_counter) % part_frames.frame_count
    
    def update_hunger(self):
        """Decrease hunger over time."""
        if self.dino is None:
            return
        
        current_time = time.time()
        if current_time - self.last_hunger_decrease > 5.0:  # Every 5 seconds
            self.dino.stats['hunger'] = max(0, self.dino.stats.get('hunger', 50) - 1)
            self.last_hunger_decrease = current_time
            self.update_stats_display()
    
    def render(self):
        """Render the current frame."""
        # Clear canvas
        clear_canvas(self.canvas_buffer, (135, 206, 235, 255))  # Sky blue
        
        # Render dinosaur if present
        if self.dino is not None:
            render_dinosaur(
                self.canvas_buffer,
                self.dino,
                self.dino_x,
                self.dino_y,
                self.current_variants,
                self.current_frames,
                flip_h=self.dino_flip,
                scale=self.dino_scale
            )
        
        # Convert to PhotoImage and display
        pil_image = canvas_to_pil(self.canvas_buffer)
        self.photo_image = ImageTk.PhotoImage(pil_image)
        
        if self.canvas_image_id is None:
            self.canvas_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
        else:
            self.canvas.itemconfig(self.canvas_image_id, image=self.photo_image)
    
    def animate(self):
        """Main animation loop."""
        current_time = time.time()
        dt = current_time - self.last_update
        self.last_update = current_time
        
        # Cap dt to avoid huge jumps
        dt = min(dt, 0.1)
        
        # Update
        self.update_physics(dt)
        self.update_hunger()
        
        # Render
        self.render()
        
        # Schedule next frame (60 FPS target)
        self.root.after(16, self.animate)


def main():
    root = tk.Tk()
    app = DinoPet(root)
    root.mainloop()


if __name__ == '__main__':
    main()
