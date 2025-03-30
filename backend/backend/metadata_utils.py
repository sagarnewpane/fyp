import subprocess
import json
import os
from pathlib import Path
from io import BytesIO
from PIL import Image
from fnmatch import fnmatch

# Define your target schema for categorizing metadata
TARGET_SCHEMA = {
    "EXIF": {
        "Basic Image Information": [
            {"name": "FileName", "type": "text", "label": "File Name", "placeholder": "Enter file name", "readonly": True},
            {"name": "FileSize", "type": "text", "label": "File Size (bytes)", "readonly": True},
            {"name": "ImageWidth", "type": "number", "label": "Image Width (px)", "readonly": True},
            {"name": "ImageHeight", "type": "number", "label": "Image Height (px)", "readonly": True},
            {"name": "Software", "type": "text", "label": "Software Used"}
        ],
        "Camera & Device Information": [
            {"name": "Make", "type": "text", "label": "Camera Brand"},
            {"name": "Model", "type": "text", "label": "Camera Model"},
            {"name": "FNumber", "type": "number", "label": "Aperture (f-stop)", "step": 0.1},
            {"name": "ExposureTime", "type": "text", "label": "Shutter Speed"},
            {"name": "ISO", "type": "number", "label": "ISO Sensitivity"}
        ],
        "Location Data": [
            {"name": "GPSLatitude", "type": "geocoordinate", "label": "Latitude"},
            {"name": "GPSLongitude", "type": "geocoordinate", "label": "Longitude"}
        ],
        "Protection & Copyright": [
            {"name": "Copyright", "type": "text", "label": "Copyright Notice"},
            {"name": "Artist", "type": "text", "label": "Creator Name"}
        ]
    },
    "IPTC": {
        "Creator and Copyright Information": [
            {"name": "By-line", "type": "text", "label": "Photographer/Creator"},
            {"name": "Caption-Abstract", "type": "textarea", "label": "Image Description"}
        ],
        "Location Data": [
            {"name": "City", "type": "text", "label": "City"},
            {"name": "Country", "type": "text", "label": "Country"}
        ]
    },
    "XMP": {
        "Basic Information": [
            {"name": "dc:title", "type": "text", "label": "Image Title"},
            {"name": "dc:description", "type": "textarea", "label": "Image Description"}
        ],
        "Protection & Copyright": [
            {"name": "xmpRights:WebStatement", "type": "url", "label": "Copyright URL"}
        ]
    }
}

class MetadataExtractor:
    @staticmethod
    def run_exiftool(image_path):
        """
        Run exiftool on the image and return the metadata as a dictionary.
        """
        try:
            result = subprocess.run(
                ['exiftool', '-j', image_path],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            return data[0] if data else {}
        except Exception as e:
            print(f"Error running exiftool: {e}")
            return {}

    @staticmethod
    def extract_metadata(image_path):
        """
        Extract metadata from an image and organize it based on TARGET_SCHEMA.
        Includes file name and full path information.
        """
        # Ensure we have the full path and filename
        full_path = os.path.abspath(image_path)
        filename = os.path.basename(image_path)

        raw_metadata = MetadataExtractor.run_exiftool(image_path)
        organized = {
        }

        # Loop through each category and its sections defined in TARGET_SCHEMA
        for category, sections in TARGET_SCHEMA.items():
            organized[category] = {}
            for section, fields in sections.items():
                organized[category][section] = {}
                for field in fields:
                    field_name = field["name"]
                    value = None
                    # Check possible key variations in the raw metadata
                    possible_keys = [
                        field_name,
                        f"{category}:{field_name}",
                        f"{category.lower()}:{field_name}"
                    ]
                    for key in possible_keys:
                        if key in raw_metadata:
                            value = raw_metadata[key]
                            break

                    # Special handling for filename
                    if field_name == "FileName":
                        value = filename

                    # Create a metadata object that includes schema properties
                    metadata_obj = {
                        "value": value,
                        "type": field.get("type"),
                        "label": field.get("label")
                    }

                    # Add optional properties if they exist in the schema
                    if "readonly" in field:
                        metadata_obj["readonly"] = field["readonly"]
                    if "placeholder" in field:
                        metadata_obj["placeholder"] = field["placeholder"]
                    if "step" in field:
                        metadata_obj["step"] = field["step"]

                    organized[category][section][field_name] = metadata_obj

        return organized

    @staticmethod
    def embed_metadata(image_path, metadata):
        """
        Embed modified metadata back into the image.
        Uses the filename from the image path.
        """

        print(image_path)

        try:
            command = ['exiftool', '-overwrite_original']

            # Get filename from the image path
            current_filename = os.path.basename(image_path)
            print(current_filename)

            # Flatten organized metadata into exiftool arguments
            for main_cat, subcats in metadata.items():
                if main_cat in ['EXIF', 'IPTC', 'XMP']:
                    for subcat, tags in subcats.items():
                        for tag, value_obj in tags.items():
                            # Extract the actual value from the value object
                            value = value_obj.get("value") if isinstance(value_obj, dict) else value_obj
                            if value is None:
                                continue

                            # Skip filename handling as we're using the path filename
                            if tag == "FileName":
                                continue

                            # Handle special XMP namespaces if needed
                            if main_cat == 'XMP' and ':' in tag:
                                parts = tag.split(':')
                                command.append(f'-{main_cat}:{parts[0]}:{parts[1]}="{value}"')
                            else:
                                command.append(f'-{main_cat}:{tag}="{value}"')

            # Add the image path to the command
            command.append(image_path)

            # Execute the exiftool command
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"Metadata embedding failed: {result.stderr}")
                return {
                    "success": False,
                    "error": result.stderr,
                    "full_path": image_path
                }

            return {
                "success": True,
                "filename": current_filename,
                "full_path": image_path
            }

        except Exception as e:
            print(f"Metadata embedding error: {e}")
            return {
                "success": False,
                "error": str(e),
                "full_path": image_path
            }

    @staticmethod
    def organize_metadata(raw_metadata):
        """
        Fallback method using pattern matching to organize raw metadata.
        """
        return raw_metadata

# Example usage
def main():
    # Example of how to use the MetadataExtractor
    image_path = 'new_filename.png'

    # Extract metadata
    extracted_metadata = MetadataExtractor.extract_metadata(image_path)
    print("Extracted Metadata:")
    print(json.dumps(extracted_metadata, indent=2))

    # Optionally modify metadata
    # For example, changing the filename
    extracted_metadata['EXIF']['Basic Image Information']['FileName']['value'] = 'new_filename.png'

    # Embed modified metadata
    result = MetadataExtractor.embed_metadata(image_path, extracted_metadata)
    print("\nEmbedding Result:")
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
