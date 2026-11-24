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

Dependencies are listed in [pyproject.toml](pyproject.toml) and managed with [uv](https://docs.astral.sh/uv/). From the `preview_utils` folder, `uv run` creates the `.venv` and installs the packages automatically on first use:

```bash
uv run python preview_generator.py --help
```

To set up the environment explicitly without running anything:

```bash
uv sync
```

## Usage

### 1. Generate YAML Template

First, generate a configuration template from your input folder:

```bash
uv run python preview_generator.py --generate-template --input input --template-output config.yaml
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

Run the script to process all images (all options have defaults, so `uv run python preview_generator.py` alone also works):

```bash
uv run python preview_generator.py --input input --output output --config config.yaml --watermark watermark.svg
```

Or use a PNG watermark:

```bash
uv run python preview_generator.py --input input --output output --config config.yaml --watermark watermark.png
```

## Command Line Arguments

### Generate Template Mode
```bash
uv run python preview_generator.py --generate-template --input <folder> [--template-output <file>]
```

- `--generate-template`: Generate YAML template from input folder
- `--input`: Input folder containing JPG images (default: `input`)
- `--template-output`: Output path for template (default: config_template.yaml)

### Process Mode
```bash
uv run python preview_generator.py --input <folder> --output <folder> --config <file> --watermark <file>
```

- `--input`: Input folder containing JPG images (default: `input`)
- `--output`: Output folder for processed images (default: `output`)
- `--config`: YAML configuration file (default: `config.yaml`)
- `--watermark`: Watermark file, SVG or PNG (default: `signature_script_kovacsadam.png`)

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
3. Generate template: `uv run python preview_generator.py --generate-template --input input --template-output config.yaml`
4. Edit the generated `config.yaml` to customize positions
5. Process images: `uv run python preview_generator.py --input input --output output --config config.yaml --watermark watermark.png`

## Output

- Images are resized to 2048px on the longest side
- Original filenames are preserved
- JPEG quality is set to 95
- Only exposure EXIF data is retained
- Watermark is applied with specified position, opacity, and size