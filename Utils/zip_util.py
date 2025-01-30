import os
import sys

def unzip_file(zip_file, output_dir, create_dir=True):
    try:
        if create_dir:
            output_dir = zip_file.split('.')[0]
            os.makedirs(output_dir, exist_ok=True)
        os.system(f"unzip -o {zip_file} -d {output_dir}")
    except Exception as e:
        print(f"Failed to unzip file: {e}")
        sys.exit(1)
        