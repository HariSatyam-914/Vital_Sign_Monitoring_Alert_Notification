import pdfplumber
import re

def extract_patient_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    # Extracting Patient Info using Regular Expressions
    data = {
        "patient_name": re.search(r"Patient Name:\s*([\w\s]+)", text).group(1) if re.search(r"Patient Name:\s*([\w\s]+)", text) else "Unknown",
        "age": int(re.search(r"Age:\s*(\d+)", text).group(1)) if re.search(r"Age:\s*(\d+)", text) else 0,
        "gender": re.search(r"Gender:\s*(\w+)", text).group(1) if re.search(r"Gender:\s*(\w+)", text) else "Unknown",
        "phone_number": re.search(r"Phone:\s*([\d-]+)", text).group(1) if re.search(r"Phone:\s*([\d-]+)", text) else "Unknown",
        "body_temperature": float(re.search(r"Temperature:\s*([\d.]+)", text).group(1)) if re.search(r"Temperature:\s*([\d.]+)", text) else 0.0,
        "spo2": float(re.search(r"SpO2:\s*([\d.]+)", text).group(1)) if re.search(r"SpO2:\s*([\d.]+)", text) else 0.0,
        "heart_rate": int(re.search(r"Heart Rate:\s*(\d+)", text).group(1)) if re.search(r"Heart Rate:\s*(\d+)", text) else 0,
        "respiration_rate": int(re.search(r"Respiration Rate:\s*(\d+)", text).group(1)) if re.search(r"Respiration Rate:\s*(\d+)", text) else 0,
        "blood_pressure_systolic": int(re.search(r"BP Systolic:\s*(\d+)", text).group(1)) if re.search(r"BP Systolic:\s*(\d+)", text) else 0,
        "blood_pressure_diastolic": int(re.search(r"BP Diastolic:\s*(\d+)", text).group(1)) if re.search(r"BP Diastolic:\s*(\d+)", text) else 0,
    }

    return data
