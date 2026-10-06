"""
File Replacer Script

This script discovers all JPG files in a target folder (including subfolders) 
and replaces them with corresponding files from a source folder.
"""

import os
import shutil
from pathlib import Path
import argparse


def discover_jpg_files(folder_path):
    """
    Discover all JPG files in a folder and its subfolders.
    
    Args:
        folder_path: Path to the folder to search
        
    Returns:
        List of Path objects for all JPG files found
    """
    folder = Path(folder_path)
    jpg_files = []
    
    # Search for all JPG extensions
    extensions = ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']
    
    for ext in extensions:
        jpg_files.extend(folder.rglob(ext))
    
    return sorted(jpg_files)


def find_source_file(target_file, source_folder):
    """
    Find the corresponding source file for a target file.
    
    Args:
        target_file: Path object of the target file
        source_folder: Path to the source folder
        
    Returns:
        Path object of the source file if found, None otherwise
    """
    source_path = Path(source_folder)
    filename = target_file.name
    
    # Look for exact filename match
    potential_source = source_path / filename
    if potential_source.exists():
        return potential_source
    
    # Look for filename with different extension
    stem = target_file.stem
    extensions = ['.jpg', '.jpeg', '.JPG', '.JPEG']
    
    for ext in extensions:
        potential_source = source_path / f"{stem}{ext}"
        if potential_source.exists():
            return potential_source
    
    return None


def replace_files(target_folder, source_folder, dry_run=False, backup=False):
    """
    Replace all JPG files in target folder with files from source folder.
    
    Args:
        target_folder: Path to folder containing files to replace
        source_folder: Path to folder containing replacement files
        dry_run: If True, only show what would be done without actually doing it
        backup: If True, create backup of original files before replacing
        
    Returns:
        Dictionary with statistics
    """
    target_path = Path(target_folder)
    source_path = Path(source_folder)
    
    if not target_path.exists():
        raise FileNotFoundError(f"Target folder not found: {target_folder}")
    
    if not source_path.exists():
        raise FileNotFoundError(f"Source folder not found: {source_folder}")
    
    # Discover all JPG files in target folder
    target_files = discover_jpg_files(target_folder)
    
    stats = {
        'total_found': len(target_files),
        'replaced': 0,
        'not_found_in_source': 0,
        'errors': 0,
        'backed_up': 0
    }
    
    print(f"Found {len(target_files)} JPG files in target folder")
    print(f"{'DRY RUN - ' if dry_run else ''}Processing files...")
    print("-" * 60)
    
    for target_file in target_files:
        try:
            # Find corresponding source file
            source_file = find_source_file(target_file, source_folder)
            
            if source_file is None:
                print(f"❌ No source file found for: {target_file.relative_to(target_path)}")
                stats['not_found_in_source'] += 1
                continue
            
            # Show what will be done
            relative_target = target_file.relative_to(target_path)
            print(f"{'🔄' if not dry_run else '👁️ '} {relative_target} <- {source_file.name}")
            
            if not dry_run:
                # Create backup if requested
                if backup:
                    backup_path = target_file.with_suffix(target_file.suffix + '.backup')
                    shutil.copy2(target_file, backup_path)
                    stats['backed_up'] += 1
                
                # Replace the file
                shutil.copy2(source_file, target_file)
                stats['replaced'] += 1
            
        except Exception as e:
            print(f"❌ Error processing {target_file.name}: {e}")
            stats['errors'] += 1
    
    return stats


def main():
    parser = argparse.ArgumentParser(description='Replace JPG files in target folder with files from source folder')
    parser.add_argument('source_folder', help='Folder containing replacement files')
    parser.add_argument('target_folder', help='Folder containing files to replace (searched recursively)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without actually doing it')
    parser.add_argument('--backup', action='store_true', help='Create backup of original files before replacing')
    parser.add_argument('--list-only', action='store_true', help='Only list files that would be processed')
    
    args = parser.parse_args()
    
    try:
        if args.list_only:
            # Just discover and list files
            target_files = discover_jpg_files(args.target_folder)
            source_files = discover_jpg_files(args.source_folder)
            
            print(f"📁 Target folder: {args.target_folder}")
            print(f"Found {len(target_files)} JPG files:")
            for f in target_files:
                print(f"  📄 {f.relative_to(Path(args.target_folder))}")
            
            print(f"\n📁 Source folder: {args.source_folder}")
            print(f"Found {len(source_files)} JPG files:")
            for f in source_files:
                print(f"  📄 {f.name}")
            
        else:
            # Process files
            stats = replace_files(
                args.target_folder, 
                args.source_folder, 
                dry_run=args.dry_run,
                backup=args.backup
            )
            
            # Print summary
            print("\n" + "=" * 60)
            print("SUMMARY")
            print("=" * 60)
            print(f"Total files found: {stats['total_found']}")
            print(f"Files replaced: {stats['replaced']}")
            print(f"Files backed up: {stats['backed_up']}")
            print(f"Source files not found: {stats['not_found_in_source']}")
            print(f"Errors: {stats['errors']}")
            
            if args.dry_run:
                print("\n🔍 This was a dry run. Use without --dry-run to actually replace files.")
            elif stats['replaced'] > 0:
                print(f"\n✅ Successfully replaced {stats['replaced']} files!")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())

# python file_replacer.py C:\Users\adamk\Pictures\TOOLS\website_generator\adamk-gallery\preview_utils\output C:\Users\adamk\Pictures\TOOLS\website_generator\adamk-gallery\content