import numpy as np
import cv2

# --- Multichaos Map Function ---
def multichaos_map(x, mu=3.99):
    if x < 0.5:
        return mu * x * (1 - x)          # Logistic map
    elif x < 0.75:
        return np.sin(np.pi * x)         # Sine map
    else:
        return mu * min(x, 1 - x)        # Tent map

# --- Generate Chaotic Sequence ---
def generate_chaotic_sequence(length, seed, mu=3.99):
    x = seed
    seq = []
    for _ in range(length):
        x = multichaos_map(x, mu)
        seq.append(x)
    return np.array(seq)

# --- Key Stream and Permutation for a single channel ---
def generate_key_stream(shape, key):
    total = shape[0] * shape[1]
    # Create a seed from the key; ensure it is in [0,1)
    seed = (sum(ord(c) for c in key) % 1000) / 1000.0
    chaos = generate_chaotic_sequence(total, seed)

    # Permutation order (store this to reverse later)
    perm = np.argsort(chaos)
    # Generate XOR key stream
    xor_stream = np.floor(chaos * 256).astype(np.uint8)

    return perm, xor_stream

# --- Encrypt a single channel ---
def encrypt_channel(channel, key):
    flat = channel.flatten()
    perm, xor_stream = generate_key_stream(channel.shape, key)

    # Permutation: rearrange pixels
    permuted = flat[perm]
    # Substitution: XOR with the key stream
    substituted = np.bitwise_xor(permuted, xor_stream)

    # Return encrypted channel and the values needed to decrypt
    return substituted.reshape(channel.shape), perm, xor_stream

# --- Decrypt a single channel using stored permutation and key stream ---
def decrypt_channel(encrypted_channel, key, perm, xor_stream):
    flat = encrypted_channel.flatten()
    # Reverse the XOR operation
    unxored = np.bitwise_xor(flat, xor_stream)
    # Compute the inverse permutation from the stored permutation
    inv_perm = np.argsort(perm)
    # Reverse the permutation by placing each element in its original index
    unpermuted = unxored[inv_perm]

    return unpermuted.reshape(encrypted_channel.shape)

# --- Encrypt Color Image ---
def encrypt_color_image(image, key):
    # Split the image into its B, G, R channels (OpenCV uses BGR)
    channels = cv2.split(image)
    encrypted_channels = []
    perms = []       # To store permutation for each channel
    xor_streams = [] # To store XOR key stream for each channel
    for idx, channel in enumerate(channels):
        # Modify key for each channel to further differentiate (optional)
        channel_key = key + str(idx)
        enc_channel, perm, xor_stream = encrypt_channel(channel, channel_key)
        encrypted_channels.append(enc_channel)
        perms.append(perm)
        xor_streams.append(xor_stream)
    # Merge the channels back
    encrypted_img = cv2.merge(encrypted_channels)
    return encrypted_img, perms, xor_streams

# --- Decrypt Color Image ---
def decrypt_color_image(encrypted_image, key, perms, xor_streams):
    channels = cv2.split(encrypted_image)
    decrypted_channels = []
    for idx, channel in enumerate(channels):
        channel_key = key + str(idx)
        dec_channel = decrypt_channel(channel, channel_key, perms[idx], xor_streams[idx])
        decrypted_channels.append(dec_channel)
    decrypted_img = cv2.merge(decrypted_channels)
    return decrypted_img

# --- Demo Run ---
if __name__ == "__main__":
    key = "mysecurekey"
    input_image_path = "/content/watermarked-image (10).png"  # Provide a color image file

    # Load the color image (BGR format)
    img = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
    if img is None:
        print("Failed to load image. Ensure '{}' exists.".format(input_image_path))
        exit()

    # Encrypt the image
    encrypted_img, perms, xor_streams = encrypt_color_image(img, key)
    cv2.imwrite("encrypted_color.png", encrypted_img)

    # Decrypt the image using the stored permutation and XOR key streams
    decrypted_img = decrypt_color_image(encrypted_img, key, perms, xor_streams)
    cv2.imwrite("decrypted_color.png", decrypted_img)

    print("✔️ Color image encryption and decryption completed successfully.")
