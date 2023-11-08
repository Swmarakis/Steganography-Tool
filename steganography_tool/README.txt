# Author

George Somarakis
georgesom7@gmail.com


# Steganography Tool

This is a simple command-line tool that uses the Least Significant Bit (LSB) steganography technique to hide and extract messages in PNG images. It also checks if the message can fit within the image.

## Features

1. **Information Hiding**: Given a secret message and an image, the tool will hide (embed) the message within the image.
2. **Information Extraction**: Given an image, it will extract a secret message.
3. **Information Detection**: Given an image, it will detect whether the image carries a hidden message.

## Requirements

- Python 3
- Pillow library
  sudo pip3 install Pillow

## Usage
## This is only for Terminal use 

To use this tool, run the following commands in your terminal:

- To hide a message: `python3 steganography.py hide path_to_your_image.png "Your secret message"`
- To extract a message: `python3 steganography.py extract path_to_your_encoded_image.png`
- To detect a message: `python3 steganography.py detect path_to_your_image.png`

Replace `path_to_your_image.png` with the path to your image and `"Your secret message"` with the message you want to hide. `path_to_your_encoded_image.png` is the path to the image with the hidden message.

## Note

This is a basic implementation and might not work as expected with large images or large messages. For a more robust solution, you might want to look into more advanced steganography techniques or libraries.

