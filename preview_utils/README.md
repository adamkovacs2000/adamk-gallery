# Watermarked Image Preview Generator


A Python script for creating watermarked image previews with configurable watermark positions, opacity, and size. The script resizes images to 2048px (longest side) and preserves only exposure-related EXIF metadata.

## Features

- **Batch processing** of JPG images
- **SVG and PNG watermark support** with configurable size and opacity
- **Flexible positioning**: left/center/right and top/middle/bottom alignment
- **Smart resizing**: Longest side to 2048px while maintaining aspect ratio
- **Metadata preservation**: Keeps exposure parameters (ISO, aperture, shutter speed, etc.) while stripping other data
- **YAML configuration**: Easy per-file or batch configuration
- **Template generation**: Automatically create YAML config from input folder

## Requirements

Install required dependencies:

```powershell
pip install Pillow PyYAML svglib reportlab
```

Or use the requirements file:

```powershell
pip install -r requirements.txt
```

## Usage

### 1. Generate YAML Template

First, generate a configuration template from your input folder:

```powershell
python watermark_previews.py --generate-template --input "C:\path\to\input" --template-output config.yaml
```

This will scan the input folder for JPG images and create a YAML file with default settings for each image.

### 2. Edit Configuration

Edit the generated `config.yaml` file to customize watermark placement:

```yaml
defaults:
  x: right          # left, center, right, or pixel value
  y: bottom         # top, middle, bottom, or pixel value
  opacity: 0.5      # 0.0 (transparent) to 1.0 (opaque)
  watermark_size: 1.0  # Scale factor (1.0 = original size)

files:
  photo1.jpg:
    x: right
    y: bottom
    opacity: 0.7
    watermark_size: 1.2
  
  photo2.jpg:
    x: center
    y: top
    opacity: 0.5
    watermark_size: 0.8
```

### 3. Process Images

Run the script to process all images:

```powershell
python watermark_previews.py --input "C:\path\to\input" --output "C:\path\to\output" --config config.yaml --watermark watermark.svg
```

Or use a PNG watermark:

```powershell
python watermark_previews.py --input "C:\path\to\input" --output "C:\path\to\output" --config config.yaml --watermark watermark.png
```

## Command Line Arguments

### Generate Template Mode
```powershell
python watermark_previews.py --generate-template --input <folder> [--template-output <file>]
```

- `--generate-template`: Generate YAML template from input folder
- `--input, -i`: Input folder containing JPG images (required)
- `--template-output`: Output path for template (default: config_template.yaml)

### Process Mode
```powershell
python watermark_previews.py --input <folder> --output <folder> --config <file> --watermark <file>
```

- `--input, -i`: Input folder containing JPG images (required)
- `--output, -o`: Output folder for processed images (required)
- `--config, -c`: YAML configuration file (required)
- `--watermark, -w`: Watermark file - supports SVG or PNG (required)

## Configuration Options

### Position Options

**X Position:**
- `left`: Align to left edge
- `center` or `middle`: Center horizontally
- `right`: Align to right edge
- Numeric value: Exact pixel position from left

**Y Position:**
- `top`: Align to top edge
- `middle` or `center`: Center vertically
- `bottom`: Align to bottom edge
- Numeric value: Exact pixel position from top

### Appearance Options

- **opacity**: Float from 0.0 (fully transparent) to 1.0 (fully opaque)
- **watermark_size**: Scale factor for watermark size (e.g., 1.5 = 150% of original size)

## Preserved EXIF Tags

The script preserves the following exposure-related EXIF metadata:

- ExposureTime
- FNumber (Aperture)
- ISO / ISOSpeedRatings
- DateTimeOriginal
- DateTimeDigitized
- ShutterSpeedValue
- ApertureValue
- ExposureBiasValue
- FocalLength
- FocalLengthIn35mmFilm
- WhiteBalance
- LensModel
- LensMake

All other metadata (including GPS, camera serial numbers, etc.) is stripped.

## Example Workflow

1. Place your JPG images in an input folder
2. Create an SVG watermark file
3. Generate template: `python watermark_previews.py --generate-template -i input_folder`
4. Edit the generated `config_template.yaml` to customize positions
5. Process images: `python watermark_previews.py -i input_folder -o output_folder -c config_template.yaml -w watermark.svg`

## Output

- Images are resized to 2048px on the longest side
- Original filenames are preserved
- JPEG quality is set to 95
- Only exposure EXIF data is retained
- Watermark is applied with specified position, opacity, and size