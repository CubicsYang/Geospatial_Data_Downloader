import rasterio as rio
import numpy as np
import os

def mosaic_dems(input_files, output_path):
    """Mosaic DEMs

    Args:
        input_files (list): list of DEM files
        output_path (str): output path
    """
    try:
        # Read metadata of first file
        with rio.open(input_files[0]) as src0:
            meta = src0.meta
        # Update metadata
        meta.update(count = len(input_files))
        # Read each layer and write it to stack
        with rio.open(output_path, 'w', **meta) as dst:
            for id, layer in enumerate(input_files, start=1):
                with rio.open(layer) as src1:
                    dst.write_band(id, src1.read(1))
        print(f"Mosaiced DEMs to {output_path}")
    except Exception as e:
        print(f"Failed to mosaic DEMs: {e}")
        