#!/usr/bin/env python3
import os
from jsmin import jsmin

def optimize_js_file(input_file, output_file):
    with open(input_file, 'r') as file:
        js_content = file.read()

    optimized_js = jsmin(js_content)

    with open(output_file, 'w') as file:
        file.write(optimized_js)

    print(f"Optimized JS saved to {output_file}")

def optimize_js_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.js'):
                input_file = os.path.join(root, file)
                output_file = os.path.join(root, f"optimized_{file}")
                optimize_js_file(input_file, output_file)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Optimize JS files.")
    parser.add_argument("path", help="Path to the JS file or directory containing JS files.")
    args = parser.parse_args()

    if os.path.isfile(args.path):
        optimize_js_file(args.path, f"optimized_{os.path.basename(args.path)}")
    elif os.path.isdir(args.path):
        optimize_js_directory(args.path)
    else:
        print("Invalid path. Please provide a valid JS file or directory.")