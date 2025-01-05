import json
import re
import requests
from PIL import Image #, ImageEnhance
import pytesseract
#import cv2
#import numpy as np


class ReceiptOCR:
    """
    A class for processing and extracting text from receipt images using Optical Character Recognition (OCR).

    This class provides methods to preprocess receipt images to enhance OCR accuracy and extract text using
    the Tesseract OCR engine.

    Attributes:
        tesseract_cmd (str): Path to the Tesseract OCR executable, if not set in the system's PATH.
    """
    def __init__(self, tesseract_cmd=None):
        """
        Initializes the ReceiptOCR class.

        :param tesseract_cmd: Path to the Tesseract executable (optional).
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def preprocess_image(self, image_path):
        """
        Preprocess the image to improve OCR results.

        :param image_path: Path to the receipt image.
        :return: Preprocessed image as a PIL Image object.
        """
        #TODOs Preprocessing

    def extract_text(self, image_path):
        """
        Extract text from the receipt image.

        :param image_path: Path to the receipt image.
        :return: Extracted text as a string.
        """
        # Preprocess the image
        #preprocessed_image = self.preprocess_image(image_path)

        # Open the image
        image = Image.open(image_path)

        # Perform OCR using Tesseract
        text = pytesseract.image_to_string(image)
        return text
    
    def filter_receipt_json(self, json_data, keys_to_extract):   
        """
        Filters receipt JSON data to include only the specified keys.

        Parameters:
            json_data (dict): The input JSON data.
            keys_to_extract (list): List of keys to extract from the JSON data.

        Returns:
            dict: Filtered JSON data containing only the specified keys.
        """
        try:
            # Check if the input JSON contains receipts
            receipts = json_data.get("receipts", [])
            if not receipts:
                raise ValueError("No receipts found in the JSON data.")

            # Extract the first receipt
            receipt = receipts[0]

            # Filtered data structure based on keys_to_extract
            filtered_data = {key: receipt.get(key) for key in keys_to_extract if key != "items"}

            # Handle "items" separately if included in keys_to_extract
            if "items" in keys_to_extract:
                filtered_data["items"] = [
                    {key: item.get(key) for key in ["description", "amount", "qty"] if key in item}
                    for item in receipt.get("items", [])
                ]

            return filtered_data

        except Exception as e:
            print(f"Error while filtering JSON data: {e}")
            return None

    def ocr_api(self, image_path,json_path):
        """
        Sends an image to the receipt OCR API and returns the JSON response.

        Parameters:
            image_path (str): Path to the image file.
            json_path (str): Path for the json file.

        Returns:
            dict: JSON response from the OCR API.
        """
        receipt_ocr_endpoint ="https://ocr2.asprise.com/api/v1/receipt" #Primary "https://ocr.asprise.com/api/v1/receipt"  # backup : https://ocr2.asprise.com/api/v1/receipt

        try:
            # Make the POST request
            with open(image_path, "rb") as image_file:
                response = requests.post(
                    receipt_ocr_endpoint,
                    data={
                        'api_key': "TEST",
                        'recognizer': "US",
                        'ref_no': "ocr_python_123",
                    },
                    files={"file": image_file},
                    timeout=10
                )

            # Check if the request was successful
            response.raise_for_status()

            # Parse the JSON response
            api_response_json = response.json()

            # Write the api_response_json data to the file
            file_name = json_path[:-4]+".json"
            with open( file_name , 'w', encoding='utf-8') as json_file:
                json.dump( api_response_json , json_file, indent=4, ensure_ascii=False)

            filtered_receipt_json = self.filter_receipt_json(api_response_json, ["merchant_name", "merchant_address", "date", "time", "total", "currency", "ocr_confidence", "items"])

            return filtered_receipt_json
        
        except requests.exceptions.Timeout:
            print("Error: The request timed out after 10 seconds.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except json.JSONDecodeError:
            print("Error: Unable to parse JSON response.")
            return None
        