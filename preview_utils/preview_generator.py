"""
Watermarked Image Preview Generator

This script creates watermarked previews of images with configurable watermark positions,
opacity, and size. It resizes images (longest side) and preserves  EXIF metadata
"""

import os
import yaml
from pathlib import Path
from PIL import Image, ExifTags

def load_config(config_path):
    """Load YAML configuration file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_position_coords(image_size, watermark_size, x_pos, y_pos):
    """
    Calculate watermark position coordinates based on position strings.
    
    Args:
        image_size: (width, height) of the image
        watermark_size: (width, height) of the watermark
        x_pos: 'left', 'center', 'right', or numeric value
        y_pos: 'top', 'middle', 'bottom', or numeric value
    
    Returns:
        (x, y) coordinates for watermark placement
    """
    img_w, img_h = image_size
    wm_w, wm_h = watermark_size
    
    # Calculate X coordinate
    if x_pos == 'left':
        x = wm_w // 5
    elif x_pos == 'center' or x_pos == 'middle':
        x = (img_w - wm_w) // 2
    elif x_pos == 'right':
        x = img_w - wm_w + (wm_w // 5)
    else:
        x = int(x_pos)
    
    # Calculate Y coordinate
    if y_pos == 'top':
        y = wm_h // 2
    elif y_pos == 'middle' or y_pos == 'center':
        y = (img_h - wm_h) // 2
    elif y_pos == 'bottom':
        y = img_h - int(wm_h * 1.5)
    else:
        y = int(y_pos)
    
    return (x, y)


def calculate_adaptive_watermark_scale(image_size, watermark_size, base_scale=1.0, target_percentage=0.15):
    """
    Calculate watermark scale to maintain consistent relative size across orientations.
    
    Args:
        image_size: (width, height) of the image
        watermark_size: (width, height) of the watermark
        base_scale: Base scale factor from config
        target_percentage: Target watermark size as percentage of image diagonal
    
    Returns:
        Calculated scale factor
    """
    img_w, img_h = image_size
    wm_w, wm_h = watermark_size
    
    # Calculate image diagonal
    image_diagonal = (img_w ** 2 + img_h ** 2) ** 0.5
    
    # Calculate watermark diagonal
    watermark_diagonal = (wm_w ** 2 + wm_h ** 2) ** 0.5
    
    # Calculate scale needed to achieve target percentage of image diagonal
    target_watermark_diagonal = image_diagonal * target_percentage
    adaptive_scale = target_watermark_diagonal / watermark_diagonal
    
    # Apply base scale factor
    final_scale = adaptive_scale * base_scale
    
    return final_scale


def load_watermark(watermark_path, scale=1.0, image_size=None, target_percentage=0.15):
    """
    Load watermark (SVG or PNG) and scale it adaptively based on image size.
    
    Args:
        watermark_path: Path to watermark file (SVG or PNG)
        scale: Base scale factor for watermark size
        image_size: (width, height) of target image for adaptive scaling
        target_percentage: Target watermark size as percentage of image diagonal
    
    Returns:
        PIL Image object
    """
    watermark_path = Path(watermark_path)
    extension = watermark_path.suffix.lower()
    
    if extension in ['.png', '.jpg', '.jpeg']:
        # Load PNG/JPEG directly
        watermark = Image.open(watermark_path)
        
        # Calculate adaptive scale if image size is provided
        if image_size is not None:
            adaptive_scale = calculate_adaptive_watermark_scale(
                image_size, watermark.size, scale, target_percentage
            )
        else:
            adaptive_scale = scale
        
        # Scale if needed
        if adaptive_scale != 1.0:
            new_width = int(watermark.width * adaptive_scale)
            new_height = int(watermark.height * adaptive_scale)
            watermark = watermark.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    else:
        raise ValueError(f"Unsupported watermark format: {extension}. Use .png, .jpg, or .jpeg")
    
    return watermark


def apply_watermark(image, watermark, position, opacity):
    """
    Apply watermark to image at specified position with opacity.
    
    Args:
        image: PIL Image object
        watermark: PIL Image object (watermark)
        position: (x, y) tuple for watermark placement
        opacity: Float 0-1 for watermark opacity
    
    Returns:
        PIL Image with watermark applied
    """
    # Convert image to RGBA if needed
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Ensure watermark has alpha channel
    if watermark.mode != 'RGBA':
        watermark = watermark.convert('RGBA')
    
    # Adjust watermark opacity
    watermark_with_opacity = watermark.copy()
    alpha = watermark_with_opacity.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    watermark_with_opacity.putalpha(alpha)
    
    # Create a copy of the image to paste watermark on
    result = image.copy()
    result.paste(watermark_with_opacity, position, watermark_with_opacity)
    
    return result


def resize_image(image, max_size=2048):
    """
    Resize image so the longest side is max_size pixels.
    
    Args:
        image: PIL Image object
        max_size: Maximum size for longest side
    
    Returns:
        Resized PIL Image
    """
    width, height = image.size
    
    if width > height:
        if width > max_size:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            return image
    else:
        if height > max_size:
            new_height = max_size
            new_width = int(width * (max_size / height))
        else:
            return image
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def process_image(input_path, output_path, watermark_path, config, max_size, quality, preserve_exif):
    """
    Process a single image: resize, apply watermark, strip metadata, save.
    
    Args:
        input_path: Path to input image
        output_path: Path to save output image
        watermark_path: Path to watermark file (SVG or PNG)
        config: Configuration dictionary for this image
    """
    # Load original image
    Image.MAX_IMAGE_PIXELS = None  # Disable DecompressionBombError
    original = Image.open(input_path)
    
    # Resize image
    resized = resize_image(original, max_size=max_size)
    
    # Load and scale watermark with adaptive sizing
    watermark_scale = config.get('watermark_size', 1.0)
    target_percentage = config.get('watermark_target_percentage', 0.15)  # 15% of diagonal by default
    watermark = load_watermark(
        watermark_path, 
        scale=watermark_scale, 
        image_size=resized.size,
        target_percentage=target_percentage
    )
    
    # Get watermark position
    x_pos = config.get('x', 'right')
    y_pos = config.get('y', 'bottom')
    position = get_position_coords(resized.size, watermark.size, x_pos, y_pos)
    
    # Apply watermark
    opacity = config.get('opacity', 0.5)
    watermarked = apply_watermark(resized, watermark, position, opacity)
    
    # Convert back to RGB for JPEG
    if watermarked.mode == 'RGBA':
        # Create white background
        rgb_image = Image.new('RGB', watermarked.size, (255, 255, 255))
        rgb_image.paste(watermarked, mask=watermarked.split()[3])
        watermarked = rgb_image
    
    # Save with preserved EXIF (excluding GPS)
    try:
        if preserve_exif:
            # Get the original EXIF data directly
            exif_bytes = original.getexif()
            if exif_bytes:
                watermarked.save(output_path, 'JPEG', quality=quality, exif=exif_bytes)
            else:
                # No EXIF data to preserve
                watermarked.save(output_path, 'JPEG', quality=quality)
    except Exception as e:
        print(f"Warning: Could not save with EXIF, saving without: {e}")
        watermarked.save(output_path, 'JPEG', quality=quality)
    
    print(f"Processed: {Path(input_path).name} -> {Path(output_path).name}")


def process_batch(input_folder, output_folder, watermark_path, config_file, max_size, quality, preserve_exif):
    """
    Process all images in the input folder according to configuration.
    
    Args:
        input_folder: Path to folder containing input images
        output_folder: Path to folder for output images
        watermark_path: Path to watermark file (SVG or PNG)
        config_file: Path to YAML configuration file
    """
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Load configuration
    config = load_config(config_file)
    
    # Get default settings
    defaults = config.get('defaults', {})
    
    # Get file-specific settings
    file_configs = config.get('files', {})
    
    # Process each image
    input_path = Path(input_folder)
    
    for image_file in list(input_path.glob('*.jpg', case_sensitive=False)) + list(input_path.glob('*.jpeg', case_sensitive=False)):
        filename = image_file.name
        
        # Set output path (keep original filename)
        output_path = Path(output_folder) / filename
        
        # Skip if output file already exists
        if output_path.exists():
            print(f"Skipping {filename}: already exists in output folder")
            continue
        
        # Get config for this file (use defaults if not specified)
        file_config = file_configs.get(filename, {})
        
        # Merge with defaults
        merged_config = {**defaults, **file_config}
        
        try:
            process_image(str(image_file), str(output_path), watermark_path, merged_config, 
                          max_size=max_size, quality=quality, preserve_exif=preserve_exif)
        except Exception as e:
            print(f"Error processing {filename}: {e}")


def generate_yaml_template(output_yaml='config_template.yaml'):
    config = {
        'defaults': {
            'x': 'right',
            'y': 'bottom',
            'opacity': 0.5,
            'watermark_size': 1.0,
            'watermark_target_percentage': 0.15  # 15% of image diagonal
        },
        'files': {}
    }
    
    # Write YAML file
    with open(output_yaml, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    print(f"Generated YAML template: {output_yaml}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate watermarked image previews')
    parser.add_argument('--generate-template', action='store_true', help='Generate YAML template from input folder')
    parser.add_argument('--input', default='input', help='Input folder containing images')
    parser.add_argument('--output', default='output', help='Output folder for processed images')
    parser.add_argument('--config', default='config.yaml', help='YAML configuration file')
    parser.add_argument('--watermark', default='signature_script_kovacsadam.png', help='Watermark file (SVG or PNG)')
    parser.add_argument('--template-output', default='config_template.yaml', help='Output path for generated template (default: config_template.yaml)')
    
    args = parser.parse_args()
    
    if args.generate_template:
        # Generate YAML template
        generate_yaml_template(args.template_output)
    else:
        # Process images
        process_batch(args.input, args.output, args.watermark, args.config,
                      max_size=2048,  # 2560
                      quality=80,
                      preserve_exif=True)
