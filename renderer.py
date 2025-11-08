"""
Efficient rendering engine for dinosaur pets.
Direct RGBA manipulation with numpy for performance.
"""

import numpy as np
from typing import Tuple, Optional
from dino_loader import DinoImage
import math


def create_canvas(width: int, height: int) -> np.ndarray:
    """Create a blank RGBA canvas."""
    # Use uint8 for efficiency, initialize to transparent
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    canvas[:, :, 3] = 0  # Fully transparent
    return canvas


def clear_canvas(canvas: np.ndarray, color: Tuple[int, int, int, int] = (0, 0, 0, 0)):
    """Clear canvas to a solid color."""
    canvas[:, :, 0] = color[0]
    canvas[:, :, 1] = color[1]
    canvas[:, :, 2] = color[2]
    canvas[:, :, 3] = color[3]


def composite_image(
    canvas: np.ndarray,
    image: DinoImage,
    x: float,
    y: float,
    flip_h: bool = False,
    flip_v: bool = False,
    rotation: float = 0.0,
    scale: float = 1.0
):
    """
    Composite an image onto the canvas at the given position.
    
    Position (x, y) is where the image's anchor point will be placed.
    Uses nearest-neighbor interpolation for now.
    
    Args:
        canvas: Target RGBA array
        image: DinoImage to composite
        x, y: Position in canvas coordinates (anchor point)
        flip_h: Flip horizontally
        flip_v: Flip vertically
        rotation: Rotation in degrees (not implemented yet)
        scale: Scale factor
    """
    src = image.rgba_data
    
    # Apply transformations
    if flip_h:
        src = np.fliplr(src)
    if flip_v:
        src = np.flipud(src)
    
    # Calculate position (anchor-relative)
    anchor_x, anchor_y = image.anchor
    
    # Top-left corner in canvas coordinates
    dst_x = int(x - anchor_x * scale)
    dst_y = int(y - anchor_y * scale)
    
    # Source dimensions
    src_h, src_w = src.shape[:2]
    
    # Scaled dimensions (for now, just use integer scaling)
    scaled_w = int(src_w * scale)
    scaled_h = int(src_h * scale)
    
    # Simple nearest-neighbor scaling if needed
    if scale != 1.0:
        # Create scaled version using numpy indexing
        x_indices = (np.arange(scaled_w) / scale).astype(int)
        y_indices = (np.arange(scaled_h) / scale).astype(int)
        src = src[np.ix_(y_indices, x_indices)]
        src_h, src_w = src.shape[:2]
    
    # Canvas dimensions
    canvas_h, canvas_w = canvas.shape[:2]
    
    # Calculate overlap region
    src_x_start = max(0, -dst_x)
    src_y_start = max(0, -dst_y)
    src_x_end = min(src_w, canvas_w - dst_x)
    src_y_end = min(src_h, canvas_h - dst_y)
    
    dst_x_start = max(0, dst_x)
    dst_y_start = max(0, dst_y)
    dst_x_end = dst_x_start + (src_x_end - src_x_start)
    dst_y_end = dst_y_start + (src_y_end - src_y_start)
    
    # Check if there's any overlap
    if src_x_end <= src_x_start or src_y_end <= src_y_start:
        return
    
    # Extract regions
    src_region = src[src_y_start:src_y_end, src_x_start:src_x_end]
    dst_region = canvas[dst_y_start:dst_y_end, dst_x_start:dst_x_end]
    
    # Alpha compositing (over operation)
    # dst = src * alpha_src + dst * (1 - alpha_src)
    
    alpha_src = src_region[:, :, 3:4].astype(np.float32) / 255.0
    alpha_dst = dst_region[:, :, 3:4].astype(np.float32) / 255.0
    
    # Composite RGB
    rgb_src = src_region[:, :, :3].astype(np.float32)
    rgb_dst = dst_region[:, :, :3].astype(np.float32)
    
    rgb_out = rgb_src * alpha_src + rgb_dst * (1.0 - alpha_src)
    
    # Composite alpha
    alpha_out = alpha_src + alpha_dst * (1.0 - alpha_src)
    
    # Write back to canvas
    canvas[dst_y_start:dst_y_end, dst_x_start:dst_x_end, :3] = rgb_out.astype(np.uint8)
    canvas[dst_y_start:dst_y_end, dst_x_start:dst_x_end, 3:4] = (alpha_out * 255.0).astype(np.uint8)


def render_dinosaur(
    canvas: np.ndarray,
    dino_data,  # DinoData
    x: float,
    y: float,
    current_variants: dict,
    current_frames: dict,
    flip_h: bool = False,
    scale: float = 1.0
):
    """
    Render a complete dinosaur with all its parts.
    
    Args:
        canvas: Target canvas
        dino_data: DinoData object
        x, y: Position for the dinosaur
        current_variants: Dict mapping part_name -> variant_name
        current_frames: Dict mapping part_name -> frame_index
        flip_h: Flip horizontally
        scale: Scale factor
    """
    # Render order (back to front)
    render_order = ['tail', 'dino', 'legs', 'arms', 'head']
    
    for part_name in render_order:
        variant = current_variants.get(part_name)
        frame_idx = current_frames.get(part_name, 0)
        
        part_frames = dino_data.get_part_frames(part_name, variant)
        if part_frames is None:
            continue
        
        if part_frames.frame_count == 0:
            continue
        
        image = part_frames.get_frame(frame_idx)
        composite_image(canvas, image, x, y, flip_h=flip_h, scale=scale)


def canvas_to_pil(canvas: np.ndarray):
    """Convert numpy canvas to PIL Image for display."""
    from PIL import Image
    return Image.fromarray(canvas, mode='RGBA')
