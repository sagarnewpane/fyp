# utils.py
import pyotp
from django.utils import timezone
import logging
from .models import OTPSecret

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
