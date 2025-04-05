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
            {"name": "OriginalRawFileName", "type": "text", "label": "File Name", "placeholder": "Enter file name", "readonly": False},
            {"name": "FileType", "type": "text", "label": "File Type", "readonly": True},
            {"name": "MIMEType", "type": "text", "label": "MIME Type", "readonly": True},
            {"name": "ImageWidth", "type": "number", "label": "Width", "readonly": True},
            {"name": "ImageHeight", "type": "number", "label": "Height", "readonly": True},
            {"name": "ImageSize", "type": "text", "label": "Image Size", "readonly": True},
            {"name": "Megapixels", "type": "number", "label": "Megapixels", "readonly": True},
            {"name": "Software", "type": "text", "label": "Software Used"}
        ],
        "Camera & Device Information": [
            {"name": "Make", "type": "text", "label": "Camera Brand"},
            {"name": "Model", "type": "text", "label": "Camera Model"},
            {"name": "FNumber", "type": "number", "label": "Aperture (f-stop)", "step": 0.1},
            {"name": "ExposureTime", "type": "text", "label": "Shutter Speed"},
            {"name": "ISO", "type": "number", "label": "ISO Sensitivity"},
            {"name": "FocalLength", "type": "text", "label": "Focal Length"},
            {"name": "LensInfo", "type": "text", "label": "Lens Information"},
            {"name": "LensMake", "type": "text", "label": "Lens Make"},
            {"name": "LensModel", "type": "text", "label": "Lens Model"},
            {"name": "Flash", "type": "text", "label": "Flash"},
            {"name": "WhiteBalance", "type": "text", "label": "White Balance"},
            {"name": "ExposureProgram", "type": "text", "label": "Exposure Program"},
            {"name": "MeteringMode", "type": "text", "label": "Metering Mode"},
            {"name": "ExposureCompensation", "type": "text", "label": "Exposure Compensation"}
        ],
        "Date & Time Information": [
            {"name": "DateTimeOriginal", "type": "datetime", "label": "Date/Time Taken"},
            {"name": "CreateDate", "type": "datetime", "label": "Date Created"},
            {"name": "ModifyDate", "type": "datetime", "label": "Date Modified"}
        ],
        "Location Data": [
            {"name": "GPSLatitude", "type": "geocoordinate", "label": "Latitude"},
            {"name": "GPSLongitude", "type": "geocoordinate", "label": "Longitude"},
            {"name": "GPSAltitude", "type": "text", "label": "Altitude"},
            {"name": "GPSPosition", "type": "text", "label": "GPS Position"},
            {"name": "GPSLatitudeRef", "type": "text", "label": "Latitude Reference"},
            {"name": "GPSLongitudeRef", "type": "text", "label": "Longitude Reference"}
        ],
        "Protection & Copyright": [
            {"name": "Copyright", "type": "text", "label": "Copyright Notice"},
            {"name": "Artist", "type": "text", "label": "Creator Name"},
            {"name": "Rights", "type": "text", "label": "Rights"}
        ]
    },
    "IPTC": {
        "Creator and Copyright Information": [
            {"name": "By-line", "type": "text", "label": "Photographer/Creator"},
            {"name": "By-lineTitle", "type": "text", "label": "Creator's Job Title"},
            {"name": "Credit", "type": "text", "label": "Credit"},
            {"name": "Source", "type": "text", "label": "Source"},
            {"name": "CopyrightNotice", "type": "text", "label": "Copyright Notice"},
            {"name": "Contact", "type": "text", "label": "Contact Info"}
        ],
        "Content Description": [
            {"name": "Caption-Abstract", "type": "textarea", "label": "Image Description"},
            {"name": "Headline", "type": "text", "label": "Headline"},
            {"name": "Keywords", "type": "text", "label": "Keywords"},
            {"name": "SpecialInstructions", "type": "textarea", "label": "Special Instructions"},
            {"name": "Category", "type": "text", "label": "Category"},
            {"name": "SubjectReference", "type": "text", "label": "Subject Reference"}
        ],
        "Location Data": [
            {"name": "City", "type": "text", "label": "City"},
            {"name": "Province-State", "type": "text", "label": "State/Province"},
            {"name": "Country-PrimaryLocationName", "type": "text", "label": "Country"},
            {"name": "Country-PrimaryLocationCode", "type": "text", "label": "Country Code"},
            {"name": "Sub-location", "type": "text", "label": "Sub-location"},
            {"name": "LocationName", "type": "text", "label": "Location Name"}
        ],
        "Status and Workflow": [
            {"name": "DateCreated", "type": "date", "label": "Date Created"},
            {"name": "ReleaseDate", "type": "date", "label": "Release Date"},
            {"name": "ExpirationDate", "type": "date", "label": "Expiration Date"},
            {"name": "Urgency", "type": "number", "label": "Urgency", "min": 1, "max": 9},
            {"name": "EditStatus", "type": "text", "label": "Edit Status"}
        ]
    },
    "XMP": {
            "Basic Information": [
                {"name": "Title", "type": "text", "label": "Image Title", "xmp_path": "dc:title"},
                {"name": "Description", "type": "textarea", "label": "Image Description", "xmp_path": "dc:description"},
                {"name": "Creator", "type": "text", "label": "Creator", "xmp_path": "dc:creator"},
                {"name": "Subject", "type": "text", "label": "Subject", "xmp_path": "dc:subject"},
                {"name": "Rights", "type": "text", "label": "Rights", "xmp_path": "dc:rights"}
            ],
            "Protection & Copyright": [
                {"name": "WebStatement", "type": "url", "label": "Copyright URL", "xmp_path": "xmpRights:WebStatement"},
                {"name": "Marked", "type": "boolean", "label": "Copyright Marked", "xmp_path": "xmpRights:Marked"},
                {"name": "UsageTerms", "type": "textarea", "label": "Usage Terms", "xmp_path": "xmpRights:UsageTerms"},
                {"name": "Owner", "type": "text", "label": "Owner", "xmp_path": "xmpRights:Owner"}
            ],
            "Creative Information": [
                {"name": "AuthorsPosition", "type": "text", "label": "Author's Position", "xmp_path": "photoshop:AuthorsPosition"},
                {"name": "CaptionWriter", "type": "text", "label": "Caption Writer", "xmp_path": "photoshop:CaptionWriter"},
                {"name": "Category", "type": "text", "label": "Category", "xmp_path": "photoshop:Category"},
                {"name": "DateCreated", "type": "date", "label": "Date Created", "xmp_path": "photoshop:DateCreated"},
                {"name": "Headline", "type": "text", "label": "Headline", "xmp_path": "photoshop:Headline"},
                {"name": "Instructions", "type": "textarea", "label": "Instructions", "xmp_path": "photoshop:Instructions"}
            ],
            "Rating & Workflow": [
                {"name": "Rating", "type": "number", "label": "Rating", "min": 0, "max": 5, "xmp_path": "xmp:Rating"},
                {"name": "CreatorTool", "type": "text", "label": "Creator Tool", "xmp_path": "xmp:CreatorTool"},
                {"name": "CreateDate", "type": "datetime", "label": "Create Date", "xmp_path": "xmp:CreateDate"},
                {"name": "ModifyDate", "type": "datetime", "label": "Modify Date", "xmp_path": "xmp:ModifyDate"},
                {"name": "MetadataDate", "type": "datetime", "label": "Metadata Date", "xmp_path": "xmp:MetadataDate"}
            ]
        }
}

class MetadataExtractor:
    @staticmethod
    def run_exiftool(image_path):
        """
        Run exiftool on the image and return the metadata as a dictionary.
        Added -a and -G flags to get all possible metadata including XMP.
        """
        try:
            result = subprocess.run(
                ['exiftool', '-j', '-a', '-G', '-XMP:all', image_path],
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
        organized = {}

        # Debug: Print full metadata to identify XMP fields
        print("DEBUG: Raw metadata keys:")
        print(json.dumps(list(raw_metadata.keys()), indent=2))

        # Loop through each category and its sections defined in TARGET_SCHEMA
        for category, sections in TARGET_SCHEMA.items():
            organized[category] = {}
            for section, fields in sections.items():
                organized[category][section] = {}
                for field in fields:
                    field_name = field["name"]
                    value = None

                    # For XMP data, look for the right keys with more detailed matching
                    if category == "XMP":
                        # Look for XMP data with various possible keys
                        xmp_path = field.get("xmp_path", field_name)

                        # Try these variations of XMP keys
                        possible_keys = [
                            xmp_path,
                            f"XMP:{xmp_path}",
                            f"XMP-{xmp_path.split(':')[0]}:{xmp_path.split(':')[1] if ':' in xmp_path else xmp_path}",
                            f"XMP-dc:{field_name}" if "dc:" in xmp_path else None,
                            f"XMP-xmp:{field_name}" if "xmp:" in xmp_path else None,
                            f"XMP-xmpRights:{field_name}" if "xmpRights:" in xmp_path else None,
                            f"XMP-photoshop:{field_name}" if "photoshop:" in xmp_path else None
                        ]

                        # Filter out None values
                        possible_keys = [k for k in possible_keys if k]

                        # Try each possible key
                        for key in possible_keys:
                            if key in raw_metadata:
                                value = raw_metadata[key]
                                break

                        # Try with group name format ExifTool might use
                        for key in raw_metadata:
                            if "[XMP]" in key and field_name in key:
                                value = raw_metadata[key]
                                break
                    else:
                        # Handle EXIF and IPTC similar to before
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
                    if "min" in field:
                        metadata_obj["min"] = field["min"]
                    if "max" in field:
                        metadata_obj["max"] = field["max"]

                    organized[category][section][field_name] = metadata_obj

        return organized

    @staticmethod
    def embed_metadata(image_path, metadata):
        """
        Embed modified metadata back into the image.
        Updated to better handle XMP data.
        """
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

                            # Handle XMP data with special consideration for namespaces
                            if main_cat == 'XMP':
                                # Find the original XMP path from schema
                                xmp_path = None
                                for section in TARGET_SCHEMA['XMP'].values():
                                    for field in section:
                                        if field['name'] == tag:
                                            xmp_path = field.get('xmp_path', tag)
                                            break
                                    if xmp_path:
                                        break

                                if xmp_path and ':' in xmp_path:
                                    namespace, prop = xmp_path.split(':', 1)
                                    command.append(f'-XMP-{namespace}:{prop}={value}')
                                else:
                                    command.append(f'-XMP:{tag}={value}')
                            else:
                                command.append(f'-{main_cat}:{tag}={value}')

            # Add the image path to the command
            command.append(image_path)

            # Debug: Print the command
            print(f"DEBUG: ExifTool command: {' '.join(command)}")

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
    # For example, setting XMP data
    if 'XMP' in extracted_metadata and 'Basic Information' in extracted_metadata['XMP']:
        if 'Title' in extracted_metadata['XMP']['Basic Information']:
            extracted_metadata['XMP']['Basic Information']['Title']['value'] = 'somethinf something'
        if 'Rights' in extracted_metadata['XMP']['Basic Information']:
            extracted_metadata['XMP']['Basic Information']['Rights']['value'] = 'cannot use XPM'
        if 'Creator' in extracted_metadata['XMP']['Basic Information']:
            extracted_metadata['XMP']['Basic Information']['Creator']['value'] = 'sagar XMP'
        if 'Subject' in extracted_metadata['XMP']['Basic Information']:
            extracted_metadata['XMP']['Basic Information']['Subject']['value'] = 'something XMP'
        if 'Description' in extracted_metadata['XMP']['Basic Information']:
            extracted_metadata['XMP']['Basic Information']['Description']['value'] = 'civjci'

    # Embed modified metadata
    result = MetadataExtractor.embed_metadata(image_path, extracted_metadata)
    print("\nEmbedding Result:")
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
