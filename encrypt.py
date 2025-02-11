import cv2
import json
import os

# Load the original image
img = cv2.imread("TestImage.jpg")

if img is None:
    print("Error: Could not load image. Check the file path.")
    exit()

msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Save password in a separate JSON file
with open("secret.json", "w") as f:
    json.dump({"password": password}, f)

# Get image dimensions
height, width, _ = img.shape
max_chars = (height * width * 3) - 2  # Reserve first 2 pixels for length storage

if len(msg) > max_chars:
    print(f"Error: Message too long! Max {max_chars} characters allowed.")
    exit()

# Store message length in the first 2 pixels
msg_length = len(msg)
img[0, 0, 0] = msg_length // 256  # High byte (0-255)
img[0, 0, 1] = msg_length % 256   # Low byte (0-255)

n, m, z = 0, 0, 2  # Start storing after length

# Encoding message into image
for char in msg:
    img[n, m, z] = ord(char)  # Convert char to ASCII
    z += 1
    if z == 3:  # Move to the next pixel
        z = 0
        m += 1
        if m == width:  # Move to the next row
            m = 0
            n += 1

# Save encrypted image
cv2.imwrite("encryptedImage.png", img)  # Use PNG to avoid compression artifacts
print("Message encrypted successfully in 'encryptedImage.png'.")

cv2.imwrite("encryptedImage.jpg", img)
os.system("start encryptedImage.jpg")
