import sys
from PIL import Image
import binascii
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

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

def select_image():
    filename = filedialog.askopenfilename()
    return filename

def gui():
    window = tk.Tk()
    window.title("Steganography App")

    def hide():
        image_path = select_image()
        message = simpledialog.askstring("Input", "Enter the message to hide:")
        result = hide_message(image_path, message)
        messagebox.showinfo("Result", result)

    def extract():
        image_path = select_image()
        message = extract_message(image_path)
        messagebox.showinfo("Extracted Message", message)

    def detect():
        image_path = select_image()
        result = detect_message(image_path)
        messagebox.showinfo("Result", result)

    hide_button = tk.Button(window, text="Hide", command=hide)
    extract_button = tk.Button(window, text="Extract", command=extract)
    detect_button = tk.Button(window, text="Detect", command=detect)

    hide_button.pack(side=tk.LEFT)
    extract_button.pack(side=tk.LEFT)
    detect_button.pack(side=tk.LEFT)

    window.mainloop()

if __name__ == "__main__":
    gui()

