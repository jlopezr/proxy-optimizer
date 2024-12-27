#!/usr/bin/env python3
import csscompressor
import os

def optimize_css_file(input_file, output_file):
    with open(input_file, 'r') as file:
        css_content = file.read()

    optimized_css = csscompressor.compress(css_content)

    with open(output_file, 'w') as file:
        file.write(optimized_css)

    print(f"Optimized CSS saved to {output_file}")

def optimize_css_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.css'):
                input_file = os.path.join(root, file)
                output_file = os.path.join(root, f"optimized_{file}")
                optimize_css_file(input_file, output_file)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Optimize CSS files.")
    parser.add_argument("path", help="Path to the CSS file or directory containing CSS files.")
    args = parser.parse_args()

    if os.path.isfile(args.path):
        optimize_css_file(args.path, f"optimized_{os.path.basename(args.path)}")
    elif os.path.isdir(args.path):
        optimize_css_directory(args.path)
    else:
        print("Invalid path. Please provide a valid CSS file or directory.")