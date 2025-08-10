import os
import re
import logging
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

def extract_manual_entry_details(text):
    details = {}
    name_match = re.search(r"1\.\s*Name\s*([A-Z\s]+)", text)
    details['Name'] = name_match.group(1).strip() if name_match else "Not found"


    # Extract Email
    email_match = re.search(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", text)
    details["Email"] = email_match.group(0) if email_match else "Not found"

    # Extract Phone Number (handles both continuous and spaced formats)
    phone_match = re.search(r"\b\d{10}\b|\b\d{5}\s\d{5}\b", text)
    details["Phone"] = phone_match.group(0).replace(" ", "") if phone_match else "Not found"

    # Extract CGPA
    cgpa_match = re.search(r"(\d+\.\d+)\s*CGPA", text)
    details['CGPA'] = cgpa_match.group(1).strip() if cgpa_match else "Not found"

    # Extract GATE Score and GATE Rank
    gate_score_match = re.search(r"GATE\s+\d{4}\s+-\s+Score:\s*(\d+)", text)
    details['GATE Score'] = gate_score_match.group(1).strip() if gate_score_match else "Not found"

    gate_rank_match = re.search(r"Rank:\s*(\d+)", text)
    details['GATE Rank'] = gate_rank_match.group(1).strip() if gate_rank_match else "Not found"

    # Extract Aadhar Number (12-digit)
    aadhar_match = re.search(r"\b\d{12}\b", text)
    details["Aadhar Number"] = aadhar_match.group(0) if aadhar_match else "Not found"

    return details


def extract_aadhar_details(text):
    """Extracts the Aadhar Number (12-digit) and the name from the text."""
    details = {}
    aadhar_match = re.search(r'\b\d{12}\b', text)
    details["Aadhar Number"] = aadhar_match.group(0) if aadhar_match else "Not found"
    name_match = re.search(r'\b([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)+)\b', text)
    details["Name"] = name_match.group(1).strip() if name_match else "Not found"
    return details

def extract_candidate_details(text):
    """Extracts Candidate's Name and CGPA from the 10th PDF."""
    details = {}
    name_match = re.search(r"CERTIFIED THAT\s*[:\-]?\s*([A-Z]+(?: [A-Z]+)*)\s*(?=FATHER'S NAME)", text, re.IGNORECASE)
    if name_match:
        words = name_match.group(1).strip().split()
        details["Candidate Name"] = " ".join(words[:-1]) if len(words) > 1 else name_match.group(1).strip()
    else:
        details["Candidate Name"] = "Not found"
    
    cgpa_match = re.search(r"CUMULATIVE GRADE POINT AVERAGE \(CGPA\):?\s*(\d+\.\d+)", text, re.IGNORECASE)
    details["CGPA"] = cgpa_match.group(1).strip() if cgpa_match else "Not found"
    
    aadhar_match = re.search(r'\b\d{12}\b', text)
    details["Aadhar Number"] = aadhar_match.group(0) if aadhar_match else "Not found"
    
    return details

def extract_inter_details(text):
    """Extracts Candidate's Name and Marks from the Inter Memo."""
    details = {}
    name_match = re.search(r"THIS IS TO CERTIFY THAT\s*[:\-]?\s*([A-Z]+(?: [A-Z]+)*)\s*(?=FATHER'S NAME)", text, re.IGNORECASE)
    details["Candidate Name"] = name_match.group(1).strip() if name_match else "Not found"
    marks_match = re.search(r"TOTAL MARKS\s*[:\-]?\s*(\d+)", text, re.IGNORECASE)
    details["Marks"] = marks_match.group(1).strip() if marks_match else "Not found"
    return details

def extract_gate_details(text):
    """Extracts GATE Score, Marks out of 100, and All India Rank in this paper from the GATE PDF."""
    details = {}
    score_match = re.search(r"GATE SCORE\s*[:\-]?\s*(\d+)", text, re.IGNORECASE)
    details["GATE Score"] = score_match.group(1).strip() if score_match else "Not found"
    marks_match = re.search(r"MARKS OUT OF 100\s*[:\-]?\s*(\d+\.\d+|\d+)", text, re.IGNORECASE)
    details["Marks out of 100"] = marks_match.group(1).strip() if marks_match else "Not found"
    rank_match = re.search(r"ALL INDIA RANK IN THIS PAPER\s*[:\-]?\s*(\d+)", text, re.IGNORECASE)
    details["All India Rank in this paper"] = rank_match.group(1).strip() if rank_match else "Not found"
    return details

def send_acknowledgment_email(user_email, user_name):
    sender_email = "neelaadarsh1@gmail.com"  # Replace with your email
    sender_password = "kbasycamtdoosjaj"  # Use an app password for security
    subject = "Application Received - Confirmation"
    body = f"""
                      Dear {user_name},

                    We have successfully received your application.
                    You have successfully selected for recruitment and eligible for further processing

                   Best Regards,
                   [INFO VERIFY]
                  """
    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = user_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)  # Login
        server.sendmail(sender_email, user_email, msg.as_string())  # Send Email
        server.quit()

        print(f"✅ Acknowledgment email sent to {user_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    # Process PDFs
    pdf_paths = {
        "Aadhar": input("Enter the Aadhar Card PDF file path: ").strip(),
        "10th": input("Enter the 10th PDF file path: ").strip(),
        "Inter": input("Enter the Inter Memo PDF file path: ").strip(),
        "GATE": input("Enter the GATE PDF file path: ").strip(),
        "Manual Entry": input("Enter the Manual Entry PDF file path: ").strip()
    }
    
    extracted_data = {
        "Aadhar": extract_aadhar_details(extract_text_from_pdf(pdf_paths["Aadhar"])) if pdf_paths["Aadhar"] else {},
        "10th": extract_candidate_details(extract_text_from_pdf(pdf_paths["10th"])) if pdf_paths["10th"] else {},
        "Inter": extract_inter_details(extract_text_from_pdf(pdf_paths["Inter"])) if pdf_paths["Inter"] else {},
        "GATE": extract_gate_details(extract_text_from_pdf(pdf_paths["GATE"])) if pdf_paths["GATE"] else {},
        "Manual Entry": extract_manual_entry_details(extract_text_from_pdf(pdf_paths["Manual Entry"])) if pdf_paths["Manual Entry"] else {}
    }
    
    # Print extracted details
    for category, details in extracted_data.items():
        print(f"\nExtracted {category} Details:", details)
    
    # Compare Names and Aadhar Numbers
    def normalize_name(name):
        return " ".join(name.lower().split()) if name != "Not found" else ""
    
    names = {normalize_name(extracted_data["Aadhar"].get("Name", "")), normalize_name(extracted_data["10th"].get("Candidate Name", "")), normalize_name(extracted_data["Inter"].get("Candidate Name", "")),normalize_name(extracted_data["Manual Entry"].get("Name", ""))}
    names.discard("")
    print("\nName is Verified among all Documents", "" if len(names) == 1 else "Mismatch Found")
    
    aadhar_verified = extracted_data["Aadhar"].get("Aadhar Number") == extracted_data["10th"].get("Aadhar Number")
    print("\nAadhar Number is verified", "" if aadhar_verified else "Mismatch Found")

    cgpa = float(extracted_data["10th"].get("CGPA",0))
    marks = int(extracted_data["Inter"].get("Marks", 0))
    gate_marks = float(extracted_data["GATE"].get("Marks out of 100", 0))
    aggregate = float(extracted_data["Manual Entry"].get("CGPA", 0))

    # Check conditions
    if cgpa > 8.0 and marks > 700 and gate_marks > 50 and aggregate > 7.5:
        print("Application is eligible for further processing ✅")
        send_acknowledgment_email(extracted_data["Manual Entry"].get("Email"), extracted_data["Manual Entry"].get("Name"))
    else:
        print("Application is not eligible ❌")   
   





















