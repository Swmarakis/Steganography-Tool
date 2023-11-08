import sys
from PIL import Image
import binascii

def text_to_bin(text):
    return ''.join(format(ord(i), '08b') for i in text)

def bin_to_text(binary):
    message = [binary[i:i+8] for i in range(0, len(binary), 8)]
    ascii_message = [chr(int(i, 2)) for i in message]
    return ''.join(ascii_message)

def hide_message(image_path, message):
    image = Image.open(image_path)
    binary_message = text_to_bin(message) + text_to_bin(chr(0))  # Add null terminator
    if len(binary_message) > image.width * image.height:
        return "The message is too long to fit in the image."
    encoded = image.copy()
    d = encoded.getdata()

    new_data = []
    for i in range(len(d)):
        if i < len(binary_message):
            new_pixel = ((d[i][0] & ~1) | int(binary_message[i]),) + d[i][1:]
            new_data.append(new_pixel)
        else:
            new_data.append(d[i])
    encoded.putdata(new_data)
    encoded.save("encoded_image.png", "PNG")
    return "Message hidden. The new image is saved as 'encoded_image.png'."

def extract_message(image_path):
    image = Image.open(image_path)
    binary_message = ""
    d = image.getdata()

    for i in range(image.width * image.height):
        binary_message += str(d[i][0] & 1)
        if (i+1) % 8 == 0 and int(binary_message[-8:], 2) == 0:
            break
    message = bin_to_text(binary_message[:-8])
    
    with open('hidden_message.txt', 'w') as f:
        f.write(message)
    
    return message

def detect_message(image_path):
    image = Image.open(image_path)
    d = image.getdata()

    binary_message = ""
    for i in range(image.width * image.height):
        binary_message += str(d[i][0] & 1)
        if (i+1) % 8 == 0 and int(binary_message[-8:], 2) == 0:
            break
    message = bin_to_text(binary_message[:-8])
    if message.isascii():
        return "This image contains a hidden message."
    else:
        return "This image does not contain a hidden message."

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python steganography.py <command> <image_path> [<message>]")
        sys.exit(1)

    command = sys.argv[1]
    image_path = sys.argv[2]

    if command.lower() == "hide":
        if len(sys.argv) < 4:
            print("Usage: python steganography.py hide <image_path> <message>")
            sys.exit(1)
        message = sys.argv[3]
        print(hide_message(image_path, message))
    elif command.lower() == "extract":
        extract_message(image_path)
        print("Hidden Message Extracted")
    elif command.lower() == "detect":
        print(detect_message(image_path))
    else:
        print(f"Unknown command: {command}")

