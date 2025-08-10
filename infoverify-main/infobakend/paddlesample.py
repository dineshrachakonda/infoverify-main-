import os
import re
import logging
from pdf2image import convert_from_path
from paddleocr import PaddleOCR

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="en")

def extract_text_from_image(image_path):
    """Extracts text from an image using PaddleOCR."""
    try:
        result = ocr.ocr(image_path, cls=True)
        extracted_text = "\n".join(
            [" ".join([word_info[1][0] for word_info in line]) for line in result if line]
        )
        return extracted_text.strip()
    except Exception as e:
        logging.error(f"Error extracting text from image: {e}")
        return ""

def extract_text_from_pdf(pdf_path):
    """Converts each page of a PDF to an image and extracts text."""
    try:
        extracted_text = []
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            image_path = f"temp_page_{i+1}.jpg"
            image.save(image_path, "JPEG")
            page_text = extract_text_from_image(image_path)
            extracted_text.append(f"--- Page {i+1} ---\n{page_text}\n")
            os.remove(image_path)  # Clean up the temporary image file
        return "\n".join(extracted_text).strip()
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return ""

def extract_aadhar_details(text):
    """
    Extracts the Aadhar Number (12-digit) and the name from the text.
    The name is assumed to start with a capital letter and contain at least one space.
    """
    details = {}
    # Extract Aadhar Number (12-digit)
    aadhar_match = re.search(r'\b\d{12}\b', text)
    if aadhar_match:
        details["Aadhar Number"] = aadhar_match.group(0)
    else:
        details["Aadhar Number"] = "Not found"
    
    # Extract name using a regex: name starts with a capital letter and contains at least one space.
    name_match = re.search(r'\b([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)+)\b', text)
    if name_match:
        details["Name"] = name_match.group(1).strip()
    else:
        details["Name"] = "Not found"
    
    return details

def extract_candidate_details(text):
    """
    Extracts Candidate's Name, CGPA, and Aadhar Number from the 10th PDF using regex.
    The Aadhar number is extracted as a 12-digit number.
    """
    details = {}

    # Extract Candidate Name using two possible patterns
    name_pattern = r"[A-Z]+(?: [A-Z]+)*"
    name_match = re.search(
        rf"CANDIDATE'?S? NAME\s*[:\-]?\s*({name_pattern})\s*(?=FATHER'S NAME|MOTHER'S NAME|SCHOOL NAME|ROLL NUMBER)",
        text,
        re.IGNORECASE
    )
    if not name_match:
        name_match = re.search(
            rf"CERTIFIED THAT\s*[:\-]?\s*({name_pattern})\s*(?=HAS|PASSED|FATHER'S NAME|SCHOOL NAME)",
            text,
            re.IGNORECASE
        )
    if name_match:
        details["Candidate Name"] = name_match.group(1).strip()
    else:
        details["Candidate Name"] = "Not found"

    # Extract CGPA
    cgpa_match = re.search(
        r"CUMULATIVE GRADE POINT AVERAGE \(CGPA\):?\s*(\d+\.\d+)",
        text, 
        re.IGNORECASE
    )
    if cgpa_match:
        details["CGPA"] = cgpa_match.group(1).strip()
    else:
        details["CGPA"] = "Not found"

    # Extract Aadhar Number (12-digit)
    aadhar_match = re.search(r'\b\d{12}\b', text)
    if aadhar_match:
        details["Aadhar Number"] = aadhar_match.group(0)
    else:
        details["Aadhar Number"] = "Not found"

    return details

if __name__ == "__main__":
    # Process Aadhar Card PDF
    aadhar_path = input("Enter the Aadhar Card PDF file path: ").strip()
    print(f"\nProcessing file: {aadhar_path}")
    if aadhar_path.lower().endswith(".pdf"):
        full_text_aadhar = extract_text_from_pdf(aadhar_path)
    elif aadhar_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif")):
        full_text_aadhar = extract_text_from_image(aadhar_path)
    else:
        print("Unsupported file type. Please provide a PDF or an image file.")
        full_text_aadhar = ""
    
    if full_text_aadhar:
        print("\nFull Extracted Text from Aadhar Card:\n")
        print(full_text_aadhar)
        aadhar_details = extract_aadhar_details(full_text_aadhar)
        print("\nExtracted Aadhar Card Details:")
        for key, value in aadhar_details.items():
            print(f"{key}: {value}")
    
    # Process 10th PDF
    tenth_path = input("\nEnter the 10th PDF file path: ").strip()
    print(f"\nProcessing file: {tenth_path}")
    if tenth_path.lower().endswith(".pdf"):
        full_text_tenth = extract_text_from_pdf(tenth_path)
    elif tenth_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif")):
        full_text_tenth = extract_text_from_image(tenth_path)
    else:
        print("Unsupported file type. Please provide a PDF or an image file.")
        full_text_tenth = ""
    
    if full_text_tenth:
        print("\nFull Extracted Text from 10th PDF:\n")
        print(full_text_tenth)
        candidate_details = extract_candidate_details(full_text_tenth)
        
        # Update Candidate Name to exclude the last word for printing
        candidate_name = candidate_details.get("Candidate Name", "Not found")
        if candidate_name != "Not found":
            words = candidate_name.split()
            if len(words) > 1:
                candidate_name_clean = " ".join(words[:-1])
            else:
                candidate_name_clean = candidate_name
            candidate_details["Candidate Name"] = candidate_name_clean
        
        print("\nExtracted Candidate Details from 10th PDF (Name excluding last word):")
        for key, value in candidate_details.items():
            print(f"{key}: {value}")
    
    # Compare Aadhar Numbers
    aadhar_from_aadhar_pdf = aadhar_details.get("Aadhar Number", "Not found")
    aadhar_from_10th_pdf = candidate_details.get("Aadhar Number", "Not found")
    
    if aadhar_from_aadhar_pdf != "Not found" and aadhar_from_aadhar_pdf == aadhar_from_10th_pdf:
        print("\nAadhar is verified")
    else:
        print("\nAadhar verification failed: The Aadhar numbers do not match.")
    
    # Compare Names for verification using the cleaned candidate name
    name_from_aadhar_pdf = aadhar_details.get("Name", "Not found")
    name_from_candidate_pdf = candidate_details.get("Candidate Name", "Not found")
    
    if name_from_aadhar_pdf != "Not found" and name_from_candidate_pdf != "Not found" and \
       name_from_aadhar_pdf.lower() == name_from_candidate_pdf.lower():
        print("\nName is verified")
    else:
        print("\nName verification failed: The names do not match.")













