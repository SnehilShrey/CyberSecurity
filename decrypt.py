import cv2
import json

# Load the encrypted image
img = cv2.imread("encryptedImage.png")

if img is None:
    print("Error: Could not load encrypted image. Check the file path.")
    exit()

# Retrieve stored password
try:
    with open("secret.json", "r") as f:
        stored_data = json.load(f)
    stored_password = stored_data["password"]
except FileNotFoundError:
    print("Error: Password file missing. Cannot decrypt.")
    exit()

password = input("Enter passcode: ")

if password != stored_password:
    print("Incorrect password!")
    exit()

# **Retrieve message length correctly**
msg_length = (int(img[0, 0, 0]) * 256) + int(img[0, 0, 1])  # FIXED

n, m, z = 0, 0, 2  # Start reading after length
message = ""

# **Read only the required number of characters**
for _ in range(msg_length):
    message += chr(int(img[n, m, z]))  # FIXED TYPE CONVERSION
    z += 1
    if z == 3:  # Move to the next pixel
        z = 0
        m += 1
        if m == img.shape[1]:  # Move to next row
            m = 0
            n += 1

print("Decrypted Message:", message)
