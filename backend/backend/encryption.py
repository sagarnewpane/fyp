import os
import time
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# === AES Config ===
KEY_SIZE = 32  # 256-bit
BLOCK_SIZE = 16  # AES block size

# === Helper Functions ===
def pad(data):
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_aes_cbc(data, key):
    iv = os.urandom(BLOCK_SIZE)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded = pad(data)
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return iv + ciphertext  # Store IV at beginning

def decrypt_aes_cbc(encrypted_data, key):
    iv = encrypted_data[:BLOCK_SIZE]
    ciphertext = encrypted_data[BLOCK_SIZE:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return unpad(padded_plaintext)

# === Main Test Function ===
def run_test(image_path: str):
    key = os.urandom(KEY_SIZE)
    input_path = Path(image_path)
    if not input_path.exists():
        print("❌ Image file not found.")
        return

    with open(input_path, "rb") as f:
        image_data = f.read()

    print(f"\n📸 Loaded image: {input_path.name} ({len(image_data) / 1024 / 1024:.2f} MB)")

    # === Encrypt ===
    print("🔐 Encrypting...")
    t1 = time.time()
    encrypted = encrypt_aes_cbc(image_data, key)
    t2 = time.time()
    enc_time_ms = (t2 - t1)

    encrypted_path = input_path.with_name("encrypted_image.bin")
    with open(encrypted_path, "wb") as f:
        f.write(encrypted)

    print(f"💾 Encrypted image saved as: {encrypted_path}")

    # === Decrypt ===
    print("🔓 Decrypting...")
    t3 = time.time()
    decrypted = decrypt_aes_cbc(encrypted, key)
    t4 = time.time()
    dec_time_ms = (t4 - t3)

    decrypted_path = input_path.with_name(f"decrypted_{input_path.name}")
    with open(decrypted_path, "wb") as f:
        f.write(decrypted)

    # === Compare and Output ===
    match = image_data == decrypted
    print(f"\n✔️ Decryption match: {match}")
    print(f"⏱️ Encryption time: {enc_time_ms:.4f} ms")
    print(f"⏱️ Decryption time: {dec_time_ms:.4f} ms")
    print(f"📝 Decrypted image saved as: {decrypted_path}")

# === Run ===
if __name__ == "__main__":
    # Replace with your image path here
    test_image_path = "/content/watermarked-image (11).png"  # ← Change this to your test image
    run_test(test_image_path)
