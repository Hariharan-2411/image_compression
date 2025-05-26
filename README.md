# image_compression


## Overview

This repository contains a Python script that performs **lossless image compression** using **horizontal**, **vertical**, and **diagonal** **Run-Length Encoding (RLE)** with **Huffman encoding**. The compression algorithm aims to reduce the file size of images while retaining all the original pixel data.

### Key Features:
- Horizontal Run-Length Encoding (RLE)
- Vertical Run-Length Encoding (RLE)
- Diagonal Run-Length Encoding (RLE)
- Huffman encoding for efficient storage
- Supports PNG, JPEG, and other image formats

## Requirements

- Python 3.x
- `numpy` library
- `Pillow` (PIL Fork)
- `dahuffman` library

## Installation

```bash
Step 1: Clone the repository
Clone this repository to your local machine:
git clone https://github.com/hariharan-2411/image_compression.git
cd image_compression

Step 2: Install dependencies
Install the required dependencies:
pip install numpy Pillow dahuffman

Usage
Run the script with an image file as the input:
python compress_image.py path_to_image.jpg
The script will output a compressed version of the image with _cmp appended to the original filename.

Example
Here’s an example of how the algorithm compresses an image:
python compress_image.py sample_image.png
The result will be a compressed image file sample_image_cmp.png.

How It Works
Run-Length Encoding:
Horizontal Run (n): Compresses consecutive repeating pixels horizontally.

Vertical Run (v): Compresses consecutive repeating pixels vertically.

Diagonal Run (d): Compresses consecutive repeating pixels diagonally from top-left to bottom-right.

Huffman Encoding:
The tags used in compression (like n, v, d, p, etc.) are encoded using Huffman coding to reduce their size in the final compressed image.

Tags and Their Meaning:
p: Pixel data (for new color pixels).

n: Run-length for horizontal repetition.

v: Run-length for vertical repetition.

d: Run-length for diagonal repetition.

i: Index of previously encountered pixel color.

R, C: Large color differences between rows and columns.

r, c: Small color differences between rows and columns.
