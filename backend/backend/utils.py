# utils.py
import pyotp
from django.utils import timezone
import logging
from .models import OTPSecret
import tempfile

logger = logging.getLogger(__name__)

class OTPHandler:
    @staticmethod
    def generate_and_store_otp(image_access, email):
        try:
            # Generate new secret and OTP
            secret = pyotp.random_base32()
            totp = pyotp.TOTP(secret, interval=300)  # 5 minutes
            otp = totp.now()

            # Store secret
            secret_obj = OTPSecret.objects.create(
                image_access=image_access,
                email=email,
                secret=secret
            )
            return otp

        except Exception as e:
            print(f"Error generating OTP: {str(e)}")
            raise

    @staticmethod
    def verify_otp(image_access, email, provided_otp):
        try:
            # Get the most recent unused secret
            secret_obj = OTPSecret.objects.filter(
                image_access=image_access,
                email=email,
                is_used=False
            ).order_by('-created_at').first()

            print(f"""
            Verifying OTP:
            Email: {email}
            Provided OTP: {provided_otp}
            Secret Found: {secret_obj is not None}
            """)

            if not secret_obj:
                print("No valid secret found")
                return False

            # Create TOTP verifier
            totp = pyotp.TOTP(secret_obj.secret, interval=300)

            # Try to verify with a window
            is_valid = totp.verify(str(provided_otp).zfill(6), valid_window=1)

            print(f"""
            Verification Details:
            Secret: {secret_obj.secret}
            Created at: {secret_obj.created_at}
            Current time: {timezone.now()}
            Is Valid: {is_valid}
            """)

            if is_valid:
                secret_obj.is_used = True
                secret_obj.save()
                print("OTP verified successfully")
            else:
                print("Invalid OTP")

            return is_valid

        except Exception as e:
            print(f"Error verifying OTP: {str(e)}")
            return False


from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
import numpy as np
from .models import WatermarkSettings, InvisibleWatermarkSettings
from .scripts.steg import TextSteganography
from .metadata_utils import MetadataExtractor
import subprocess
import json
import os
import cv2
from django.conf import settings
from datetime import datetime

class ProtectionChain:
    @staticmethod
    def create_protected_image(user_image, protection_features, access_rule):
            """Create a protected version of the image with selected features"""
            logger.info(f"Starting protection chain for image {user_image.id}")
            logger.info(f"Protection features requested: {protection_features}")

            try:
                # Start with the original image
                logger.info(f"Opening original image from path: {user_image.image.path}")
                current_image = Image.open(user_image.image.path)
                protected_image = current_image

                # Log initial image details
                logger.info(f"Initial image size: {current_image.size}")
                logger.info(f"Initial image mode: {current_image.mode}")

                # Apply protections in order of computational intensity
                if protection_features.get('ai_protection') and user_image.ai_protection_enabled:
                    logger.info("Applying AI protection...")
                    protected_image = ProtectionChain._apply_ai_protection(protected_image)

                if protection_features.get('hidden_watermark') and user_image.hidden_watermark_enabled:
                    try:
                        invisible_settings = InvisibleWatermarkSettings.objects.get(user_image=user_image)
                        if invisible_settings.enabled and invisible_settings.text:
                            logger.info("Applying steganography...")
                            protected_image = ProtectionChain._apply_steganography(
                                protected_image,
                                invisible_settings.text
                            )
                    except InvisibleWatermarkSettings.DoesNotExist:
                        logger.warning("No invisible watermark settings found")

                if protection_features.get('watermark') and user_image.watermark_enabled:
                    try:
                        watermark_settings = WatermarkSettings.objects.get(user_image=user_image)
                        if watermark_settings.enabled:
                            logger.info(f"Applying watermark with settings: {watermark_settings.settings}")
                            protected_image = ProtectionChain._apply_watermark(
                                protected_image,
                                watermark_settings.settings
                            )
                    except WatermarkSettings.DoesNotExist:
                        logger.warning("No watermark settings found")

                # If metadata is enabled, use the processed file
                if protection_features.get('metadata') and user_image.metadata_enabled:
                    logger.info("Applying metadata protection...")
                    result = ProtectionChain._apply_metadata(protected_image, user_image.metadata)

                    if result:
                        file_path = os.path.join(result['temp_dir'], result['filename'])
                        logger.info(f"Attempting to open file at: {file_path}")

                        # Save the processed file to the model
                        with open(file_path, 'rb') as f:
                            access_rule.protected_image.save(
                                f'protected_{user_image.image_name}',
                                ContentFile(f.read()),
                                save=True
                            )

                        # Clean up the processing file
                        try:
                            os.remove(file_path)
                            logger.info(f"Cleaned up processing file: {file_path}")
                        except Exception as e:
                            logger.warning(f"Could not remove processing file: {str(e)}")

                        return True
                    else:
                        logger.error("Metadata protection failed")
                        return False

                # Save the final protected image
                output = BytesIO()
                protected_image.save(output, format='PNG')
                access_rule.protected_image.save(
                    f'protected_{user_image.image_name}',
                    ContentFile(output.getvalue()),
                    save=True
                )

            except Exception as e:
                logger.error(f"Error in protection chain: {str(e)}", exc_info=True)
                return None

    @staticmethod
    def _apply_watermark(image, settings):
            """Apply watermark using Node.js script"""
            logger.info("Starting watermark application")
            temp_input_path = None
            temp_output_path = None

            try:
                # Create temporary files with .png extension
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_input, \
                     tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_output:

                    temp_input_path = temp_input.name
                    temp_output_path = temp_output.name

                    logger.info(f"Saving input image to: {temp_input_path}")
                    logger.info(f"Output will be saved to: {temp_output_path}")

                    # Save input image
                    image.save(temp_input_path, 'PNG')

                    # Prepare watermark settings
                    watermark_settings = {
                        'text': settings.get('text', 'Protected'),
                        'font': settings.get('font', 'Arial'),
                        'fontSize': int(settings.get('fontSize', 24)),
                        'color': settings.get('color', '#000000'),
                        'opacity': float(settings.get('opacity', 50)),
                        'rotation': float(settings.get('rotation', 45)),
                        'pattern': settings.get('pattern', 'tiled'),
                        'spacing': float(settings.get('spacing', 50)),
                        'horizontalOffset': float(settings.get('horizontalOffset', 0)),
                        'verticalOffset': float(settings.get('verticalOffset', 0))
                    }

                    settings_json = json.dumps(watermark_settings)
                    logger.info(f"Watermark settings: {settings_json}")

                    # Get script path from Django settings
                    script_path = '../frontend/watermark.cjs'
                    logger.info(f"Using watermark script at: {script_path}")

                    # Execute Node.js script
                    cmd = ["node", script_path, temp_input_path, temp_output_path, settings_json]
                    logger.info(f"Executing command: {' '.join(cmd)}")

                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        check=True
                    )

                    # Log the script output
                    if result.stdout:
                        logger.info(f"Script stdout: {result.stdout}")
                    if result.stderr:
                        logger.warning(f"Script stderr: {result.stderr}")

                    # Check if output file exists and has content
                    if not os.path.exists(temp_output_path):
                        raise FileNotFoundError(f"Output file was not created: {temp_output_path}")

                    if os.path.getsize(temp_output_path) == 0:
                        raise ValueError("Output file is empty")

                    # Read the watermarked image
                    logger.info("Reading watermarked image")
                    watermarked_image = Image.open(temp_output_path)

                    # Create a copy of the image in memory
                    output_image = watermarked_image.copy()
                    watermarked_image.close()

                    return output_image

            except subprocess.CalledProcessError as e:
                logger.error(f"Watermark script failed with return code {e.returncode}")
                logger.error(f"stdout: {e.stdout}")
                logger.error(f"stderr: {e.stderr}")
                return image

            except Exception as e:
                logger.error(f"Error in watermarking: {str(e)}", exc_info=True)
                return image

            finally:
                # Clean up temporary files
                for path in [temp_input_path, temp_output_path]:
                    if path and os.path.exists(path):
                        try:
                            os.unlink(path)
                            logger.info(f"Cleaned up temporary file: {path}")
                        except Exception as e:
                            logger.error(f"Error cleaning up file {path}: {str(e)}")

    @staticmethod
    def _apply_steganography(image, message):
            """Apply steganography to the image"""
            logger.info("Starting steganography application")
            try:
                # Create temporary files for input and output
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_input:
                    temp_input_path = temp_input.name

                    # Save PIL Image to temporary file
                    logger.info(f"Saving input image to temporary file: {temp_input_path}")
                    image.save(temp_input_path, 'PNG')

                    try:
                        # Initialize steganography
                        stego = TextSteganography()

                        # Apply steganography using the file path
                        stego_image = stego.embed_message(temp_input_path, message)

                        if stego_image is not None:
                            # Convert back to PIL Image
                            rgb_image = cv2.cvtColor(stego_image, cv2.COLOR_BGR2RGB)
                            return Image.fromarray(rgb_image)
                        else:
                            logger.error("Steganography failed to produce output image")
                            return image

                    except Exception as e:
                        logger.error(f"Error during steganography: {str(e)}", exc_info=True)
                        return image

            except Exception as e:
                logger.error(f"Steganography error: {str(e)}", exc_info=True)
                return image
            finally:
                # Clean up temporary file
                try:
                    if os.path.exists(temp_input_path):
                        os.unlink(temp_input_path)
                        logger.info(f"Cleaned up temporary file: {temp_input_path}")
                except Exception as e:
                    logger.error(f"Error cleaning up file {temp_input_path}: {str(e)}")

    @staticmethod
    def _apply_ai_protection(image):
        """Apply AI protection to the image"""
        # Implement your AI protection logic here
        return image

    @staticmethod
    def _apply_metadata(image, metadata):
        """Apply metadata to the image"""
        logger.info("Starting metadata application")

        try:
            # Convert BASE_DIR to string and create temp directory path
            base_dir = str(settings.BASE_DIR)
            temp_dir = os.path.join(base_dir, 'backend', 'temp')

            # Ensure the temp directory exists
            os.makedirs(temp_dir, exist_ok=True)
            logger.info(f"Temp directory created/verified at: {temp_dir}")

            # Generate a unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f'processing_{timestamp}.png'
            processing_path = os.path.join(temp_dir, unique_filename)

            logger.info(f"Attempting to save image to: {processing_path}")

            # Save the PIL Image
            image.save(processing_path, 'PNG')
            logger.info("Image saved successfully")

            # Apply metadata
            result = MetadataExtractor.embed_metadata(processing_path, metadata)

            if result and result.get('success'):
                logger.info("Metadata embedding successful")
                # Return both the filename and the full path
                return {
                    'filename': unique_filename,
                    'full_path': processing_path,
                    'temp_dir': temp_dir
                }
            else:
                logger.error(f"Metadata embedding failed: {result.get('error', 'Unknown error')}")
                return None

        except Exception as e:
            logger.error(f"Error in metadata embedding: {str(e)}", exc_info=True)
            return None


    @staticmethod
    def verify_metadata(image_path):
        """Verify metadata in the image"""
        try:
            result = subprocess.run(
                ['exiftool', '-json', image_path],
                capture_output=True, text=True, check=True
            )
            metadata = json.loads(result.stdout)
            logger.info(f"Verified metadata: {metadata}")
            return metadata
        except Exception as e:
            logger.error(f"Error verifying metadata: {str(e)}")
            return None



import requests
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class SimpleLocationCollector:
    @staticmethod
    def get_client_ip(request):
        """Get client IP address from request object."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        # For development/testing, if IP is localhost/127.0.0.1, use a default public IP
        if ip in ['127.0.0.1', 'localhost', '::1']:
            ip = '8.8.8.8'  # Using Google's DNS IP as default for testing

        return ip

    @staticmethod
    def get_location_data(request):
        """Get approximate location data based on IP address."""
        try:
            client_ip = SimpleLocationCollector.get_client_ip(request)
            logger.info(f"Getting location data for IP: {client_ip}")

            # Try to get cached data
            cache_key = f'location_{client_ip}'
            cached_data = cache.get(cache_key)
            if cached_data:
                logger.info(f"Retrieved cached location data for IP: {client_ip}")
                return cached_data

            # Try different free IP geolocation services
            # Method 1: ipapi.co
            try:
                response = requests.get(f'https://ipapi.co/{client_ip}/json/')
                if response.status_code == 200:
                    data = response.json()
                    if 'error' not in data:
                        location_data = {
                            'country': data.get('country_name'),
                            'region': data.get('region'),
                            'city': data.get('city'),
                            'ip_address': client_ip
                        }
                        cache.set(cache_key, location_data, 60 * 60 * 24)  # Cache for 24 hours
                        logger.info(f"Successfully got location data from ipapi.co: {location_data}")
                        return location_data
            except Exception as e:
                logger.warning(f"ipapi.co request failed: {str(e)}")

            # Method 2: ip-api.com (fallback)
            try:
                response = requests.get(f'http://ip-api.com/json/{client_ip}')
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 'success':
                        location_data = {
                            'country': data.get('country'),
                            'region': data.get('regionName'),
                            'city': data.get('city'),
                            'ip_address': client_ip
                        }
                        cache.set(cache_key, location_data, 60 * 60 * 24)
                        logger.info(f"Successfully got location data from ip-api.com: {location_data}")
                        return location_data
            except Exception as e:
                logger.warning(f"ip-api.com request failed: {str(e)}")

            # Method 3: extreme-ip-lookup.com (second fallback)
            try:
                response = requests.get(f'https://extreme-ip-lookup.com/json/{client_ip}')
                if response.status_code == 200:
                    data = response.json()
                    location_data = {
                        'country': data.get('country'),
                        'region': data.get('region'),
                        'city': data.get('city'),
                        'ip_address': client_ip
                    }
                    cache.set(cache_key, location_data, 60 * 60 * 24)
                    logger.info(f"Successfully got location data from extreme-ip-lookup.com: {location_data}")
                    return location_data
            except Exception as e:
                logger.warning(f"extreme-ip-lookup.com request failed: {str(e)}")

        except Exception as e:
            logger.error(f"Error in get_location_data: {str(e)}")

        # Default response if all methods fail
        default_data = {
            'country': 'Unknown',
            'region': 'Unknown',
            'city': 'Unknown',
            'ip_address': client_ip
        }
        logger.warning(f"Using default location data: {default_data}")
        return default_data
