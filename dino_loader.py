"""
Dinosaur image loader with support for:
- Single images (dino.png)
- Variants (dino/a.png, dino/b.png)
- Animation frames (legs_01.png, legs_02.png)
- Nested variants with frames (legs/blue_01.png, legs/green_01.png)
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
from PIL import Image
import numpy as np


class DinoImage:
    """Represents a single image with its data and anchor point."""
    
    def __init__(self, path: Path, rgba_data: np.ndarray, anchor: Optional[Tuple[float, float]] = None):
        self.path = path
        self.rgba_data = rgba_data  # Shape: (height, width, 4)
        self.height, self.width = rgba_data.shape[:2]
        
        # Default anchor is center
        if anchor is None:
            self.anchor = (self.width / 2.0, self.height / 2.0)
        else:
            self.anchor = anchor
    
    @classmethod
    def from_file(cls, path: Path) -> 'DinoImage':
        """Load image from file path."""
        img = Image.open(path).convert('RGBA')
        rgba_data = np.array(img, dtype=np.uint8)
        return cls(path, rgba_data)


class DinoPartFrames:
    """Represents animation frames for a dinosaur part (e.g., legs, head)."""
    
    def __init__(self, name: str, variant: Optional[str] = None):
        self.name = name  # e.g., 'legs', 'head'
        self.variant = variant  # e.g., 'blue', 'happy', None for default
        self.frames: List[DinoImage] = []
    
    def add_frame(self, image: DinoImage):
        """Add a frame to this animation sequence."""
        self.frames.append(image)
    
    def get_frame(self, index: int) -> DinoImage:
        """Get frame by index, wrapping around."""
        if not self.frames:
            raise ValueError(f"No frames available for {self.name}")
        return self.frames[index % len(self.frames)]
    
    @property
    def frame_count(self) -> int:
        return len(self.frames)


class DinoData:
    """Complete dinosaur data structure."""
    
    def __init__(self, name: str, base_path: Path):
        self.name = name
        self.base_path = base_path
        
        # Parts organized by: part_name -> variant -> DinoPartFrames
        self.parts: Dict[str, Dict[Optional[str], DinoPartFrames]] = {}
        
        # Stats (simple dict for extensibility)
        self.stats = {'hunger': 50}
    
    def add_part(self, part_name: str, variant: Optional[str], image: DinoImage, frame_num: Optional[int] = None):
        """Add an image to a part, creating structures as needed."""
        if part_name not in self.parts:
            self.parts[part_name] = {}
        
        if variant not in self.parts[part_name]:
            self.parts[part_name][variant] = DinoPartFrames(part_name, variant)
        
        self.parts[part_name][variant].add_frame(image)
    
    def get_part_frames(self, part_name: str, variant: Optional[str] = None) -> Optional[DinoPartFrames]:
        """Get frames for a specific part and variant."""
        if part_name not in self.parts:
            return None
        
        # Try requested variant first
        if variant in self.parts[part_name]:
            return self.parts[part_name][variant]
        
        # Fall back to None variant (default)
        if None in self.parts[part_name]:
            return self.parts[part_name][None]
        
        # Return any available variant
        if self.parts[part_name]:
            return next(iter(self.parts[part_name].values()))
        
        return None
    
    def get_available_variants(self, part_name: str) -> List[Optional[str]]:
        """Get all available variants for a part."""
        if part_name not in self.parts:
            return []
        return list(self.parts[part_name].keys())


def parse_filename(filename: str) -> Tuple[str, Optional[str], Optional[int]]:
    """
    Parse filename to extract base name, variant, and frame number.
    
    Examples:
        'dino.png' -> ('dino', None, None)
        'legs_01.png' -> ('legs', None, 1)
        'head_happy.png' -> ('head', 'happy', None)
        'legs_blue_03.png' -> ('legs', 'blue', 3)
    
    Returns:
        (base_name, variant, frame_number)
    """
    stem = Path(filename).stem
    
    # Try to match pattern: name_variant_number or name_number
    # Pattern: base(_variant)?(_number)?
    
    # First, check for trailing number
    frame_match = re.search(r'_(\d+)$', stem)
    frame_num = None
    if frame_match:
        frame_num = int(frame_match.group(1))
        stem = stem[:frame_match.start()]
    
    # Now check for variant (anything after first underscore)
    parts = stem.split('_', 1)
    base_name = parts[0]
    variant = parts[1] if len(parts) > 1 else None
    
    return base_name, variant, frame_num


def load_dinosaur(path: Path) -> DinoData:
    """
    Load a dinosaur from a directory or single file.
    
    Supports:
    - Single file: dino.png
    - Directory with variants: dino/a.png, dino/b.png
    - Animation frames: legs_01.png, legs_02.png
    - Nested structure: legs/blue_01.png, legs/blue_02.png
    """
    path = Path(path)
    
    if path.is_file():
        # Single file - treat as 'dino' part
        dino = DinoData(path.stem, path.parent)
        img = DinoImage.from_file(path)
        dino.add_part('dino', None, img)
        return dino
    
    elif path.is_dir():
        # Directory - scan for all images
        dino = DinoData(path.name, path)
        
        # Recursively find all PNG files
        for img_path in sorted(path.rglob('*.png')):
            relative = img_path.relative_to(path)
            
            # Determine part name and variant from directory structure
            if len(relative.parts) == 1:
                # Top level: dino.png, legs_01.png, etc.
                base_name, variant, frame_num = parse_filename(relative.name)
                part_name = base_name
            else:
                # Nested: dino/a.png, legs/blue_01.png
                part_name = relative.parts[0]
                
                # The rest of the path determines variant and frame
                sub_path = Path(*relative.parts[1:])
                base_name, variant, frame_num = parse_filename(sub_path.name)
                
                # If there's a subdirectory, use it as variant
                if len(relative.parts) > 2:
                    variant = relative.parts[1]
            
            # Load image
            img = DinoImage.from_file(img_path)
            dino.add_part(part_name, variant, img, frame_num)
        
        return dino
    
    else:
        raise ValueError(f"Path does not exist: {path}")


def add_to_dinosaur(dino: DinoData, new_path: Path, part_name: Optional[str] = None):
    """
    Incrementally add images to an existing dinosaur.
    
    If adding a second 'dino' image, it will be converted to a variant.
    """
    new_path = Path(new_path)
    
    if new_path.is_file():
        # Single file
        if part_name is None:
            part_name, variant, frame_num = parse_filename(new_path.name)
        else:
            variant, frame_num = None, None
        
        img = DinoImage.from_file(new_path)
        
        # Check if this creates a variant situation
        if part_name in dino.parts and None in dino.parts[part_name]:
            # Convert existing default to a variant
            existing = dino.parts[part_name][None]
            if variant is None:
                variant = 'default'
            
            # Move existing to 'original' variant
            dino.parts[part_name]['original'] = existing
            del dino.parts[part_name][None]
        
        dino.add_part(part_name, variant, img, frame_num)
    
    elif new_path.is_dir():
        # Load all images from directory
        for img_path in sorted(new_path.rglob('*.png')):
            relative = img_path.relative_to(new_path)
            base_name, variant, frame_num = parse_filename(relative.name)
            
            img = DinoImage.from_file(img_path)
            dino.add_part(base_name, variant, img, frame_num)
