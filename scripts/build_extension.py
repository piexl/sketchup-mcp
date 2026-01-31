#!/usr/bin/env python3
"""Create SketchUp extension .rbz file from source."""

import zipfile
import shutil
import os
from pathlib import Path

# Configuration
EXTENSION_NAME = "su_mcp"
VERSION = "1.6.0"
OUTPUT_NAME = f"{EXTENSION_NAME}_v{VERSION}.rbz"

# Get directories
script_dir = Path(__file__).parent
project_root = script_dir.parent
ext_dir = project_root / EXTENSION_NAME
temp_dir = project_root / f"{EXTENSION_NAME}_temp"
output_file = project_root / OUTPUT_NAME

# Clean up temp directory
if temp_dir.exists():
    shutil.rmtree(temp_dir)

# Create temp directory and copy files
temp_dir.mkdir()

# Copy su_mcp directory
if ext_dir.exists():
    shutil.copytree(ext_dir, temp_dir / "su_mcp")
    print(f"Copied {ext_dir}")

# Copy su_mcp.rb
su_mcp_rb = project_root / "su_mcp.rb"
if su_mcp_rb.exists():
    shutil.copy(su_mcp_rb, temp_dir / "su_mcp.rb")
    print(f"Copied su_mcp.rb")

# Copy extension.json
extension_json = ext_dir / "extension.json"
if extension_json.exists():
    shutil.copy(extension_json, temp_dir / "extension.json")
    print(f"Copied extension.json")

# Create rbz file
if output_file.exists():
    output_file.unlink()

with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
    for file_path in temp_dir.rglob("*"):
        if file_path.is_file():
            arcname = file_path.relative_to(temp_dir)
            zipf.write(file_path, arcname)
            print(f"Adding: {arcname}")

# Clean up
shutil.rmtree(temp_dir)

print(f"\n✓ Created {OUTPUT_NAME}")
print(f"  Location: {output_file}")
print(f"  Install in SketchUp: Window > Extension Manager > Install Extension")
