#!/usr/bin/env python3
import os
from PIL import Image
import pillow_avif

def optimize_image_file(input_file, output_file):
    with Image.open(input_file) as img:
        img.save(output_file, format="AVIF", quality=85)
    print(f"Optimized image saved to {output_file}")

def optimize_image_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                input_file = os.path.join(root, file)
                output_file = os.path.join(root, f"optimized_{os.path.splitext(file)[0]}.avif")
                optimize_image_file(input_file, output_file)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Optimize images and convert them to AVIF format.")
    parser.add_argument("path", help="Path to the image file or directory containing image files.")
    args = parser.parse_args()

    if os.path.isfile(args.path):
        output_file = f"optimized_{os.path.splitext(os.path.basename(args.path))[0]}.avif"
        optimize_image_file(args.path, output_file)
    elif os.path.isdir(args.path):
        optimize_image_directory(args.path)
    else:
        print("Invalid path. Please provide a valid image file or directory.")