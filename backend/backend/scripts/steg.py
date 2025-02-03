import numpy as np
import cv2
from pywt import dwt2, idwt2
class TextSteganography:
    def __init__(self):
        self.bits_per_char = 8
        self.length_bits = 32
        self.embedding_strength = 0.2  # Adjust as needed for stability

    def text_to_bits(self, text):
        """
        Convert text to a binary string with a 32-bit length header.
        """
        length = len(text)
        # Format length into a 32-bit binary string
        length_bits = format(length, '032b')
        # Convert each character to its 8-bit binary representation
        text_bits = ''.join(format(ord(c), '08b') for c in text)
        return length_bits + text_bits

    def bits_to_text(self, bits):
        """
        Convert a binary string back to text.
        Assumes the first 32 bits encode the message length.
        """
        # Get message length from the first 32 bits
        length_bits = bits[:32]
        length = int(length_bits, 2)
        # Extract the bits corresponding to the actual message
        text_bits = bits[32:32 + length * self.bits_per_char]
        text = ''
        for i in range(0, len(text_bits), 8):
            byte = text_bits[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text

    def modify_coefficient(self, coeff, bit):
        """
        Embed a bit into a coefficient by quantizing the coefficient and then adding an offset.
        """
        # Quantize the coefficient in steps of 0.5 for stability
        base = round(coeff * 2) / 2
        offset = self.embedding_strength if bit == '1' else -self.embedding_strength
        return base + offset

    def extract_bit(self, coeff):
        """
        Extract an embedded bit from a coefficient by quantizing the coefficient and checking the offset.
        """
        base = round(coeff * 2) / 2
        diff = coeff - base
        # If diff is positive, interpret it as a '1'; otherwise, a '0'
        return '1' if diff > 0 else '0'

    def embed_message(self, image_path, message):
        """
        Embed a secret message into the blue channel of the image using DWT.
        Returns the modified (stego) image.
        """
        # Read the image from file
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image. Check the image path.")

        # Convert the message into a binary string (including a 32-bit length header)
        binary_data = self.text_to_bits(message)
        total_bits = len(binary_data)

        # Work with the blue channel (index 0)
        blue_channel = image[:, :, 0].astype(float)

        # Apply the Discrete Wavelet Transform (DWT) to the blue channel
        coeffs = dwt2(blue_channel, 'haar')
        cA, (cH, cV, cD) = coeffs

        # Ensure there are enough coefficients in the cD sub-band to embed the message
        if cD.size < total_bits:
            max_chars = (cD.size - self.length_bits) // self.bits_per_char
            raise ValueError(
                f"Image too small. Need {total_bits} coefficients, but have {cD.size}. "
                f"Maximum message length for this image is {max_chars} characters."
            )

        # Flatten the cD coefficients for sequential embedding
        cD_flat = cD.flatten()
        modified_coeffs = cD_flat.copy()

        # Embed each bit into the corresponding coefficient
        for i, bit in enumerate(binary_data):
            modified_coeffs[i] = self.modify_coefficient(cD_flat[i], bit)

        # Reshape the modified coefficients back to the original shape
        cD_modified = modified_coeffs.reshape(cD.shape)
        # Reconstruct the modified blue channel using the inverse DWT
        blue_channel_stego = idwt2((cA, (cH, cV, cD_modified)), 'haar')

        # Replace the blue channel in the original image with the modified channel
        stego_image = image.copy()
        stego_image[:, :, 0] = np.clip(blue_channel_stego, 0, 255).astype(np.uint8)

        return stego_image

    def extract_message(self, stego_image):
        """
        Extract the hidden message from the stego image.
        First, extract the 32-bit length header, then extract the appropriate number of bits.
        """
        # Convert blue channel to float and perform DWT
        blue_channel = stego_image[:, :, 0].astype(float)
        coeffs = dwt2(blue_channel, 'haar')
        cA, (cH, cV, cD) = coeffs
        cD_flat = cD.flatten()

        # Extract the first 32 bits to determine the message length
        length_bits = ''.join(self.extract_bit(coeff) for coeff in cD_flat[:32])
        message_length = int(length_bits, 2)

        # Calculate the total number of bits required (header + message)
        total_bits_needed = self.length_bits + message_length * self.bits_per_char

        # Extract exactly the required number of bits from the coefficients
        bits = ''.join(self.extract_bit(coeff) for coeff in cD_flat[:total_bits_needed])
        return self.bits_to_text(bits)

def test_steganography(image_path, message):
    """
    Test the text steganography process:
    - Embed the message into the image.
    - Save the stego image.
    - Extract the message from the stego image.
    - Display the original and stego images.
    """
    stego = TextSteganography()

    # Embed the message into the image
    print(f"Original message: {message}")
    stego_image = stego.embed_message(image_path, message)

    # Save the stego image (using PNG for lossless compression)
    cv2.imwrite('stego_output.png', stego_image)
    print("Stego image saved as 'stego_output.png'")

    # Extract the message from the stego image
    extracted_message = stego.extract_message(stego_image)
    print(f"Extracted message: {extracted_message}")


if __name__ == "__main__":
    # Update with your image path and message
    image_path = "/home/sagar/Documents/FYP/igaurdian/backend/media/uploads/bg.png"
    message = "Hello, this is a secret message!"
    test_steganography(image_path, message)
