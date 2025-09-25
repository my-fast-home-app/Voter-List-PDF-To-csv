import pdfplumber
import re
from typing import List, Dict

def extract_voter_data(pdf_path: str) -> List[Dict]:
    """
    Extract voter data from PDF and return as list of dictionaries
    """
    voter_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            
            if text:
                # Split text into lines and process
                lines = text.split('\n')
                current_entry = {}
                
                for line in lines:
                    line = line.strip()
                    
                    # Extract serial number
                    serial_match = re.search(r'(\d+)\.\s*নাম:', line)
                    if serial_match:
                        if current_entry:  # Save previous entry
                            voter_data.append(current_entry)
                        current_entry = {'ক্রমিক_নং': serial_match.group(1)}
                        
                    # Extract name
                    name_match = re.search(r'নাম:\s*(.+)', line)
                    if name_match and 'ক্রমিক_নং' in current_entry:
                        current_entry['নাম'] = name_match.group(1).strip()
                    
                    # Extract voter number
                    voter_match = re.search(r'ভোটার\s*নং:\s*(\d+)', line)
                    if voter_match:
                        current_entry['ভোটার_নম্বর'] = voter_match.group(1)
                    
                    # Extract father's name
                    father_match = re.search(r'পিতা:\s*(.+)', line)
                    if father_match:
                        current_entry['পিতার_নাম'] = father_match.group(1).strip()
                    
                    # Extract mother's name
                    mother_match = re.search(r'মাতা:\s*(.+)', line)
                    if mother_match:
                        current_entry['মাতার_নাম'] = mother_match.group(1).strip()
                    
                    # Extract profession
                    profession_match = re.search(r'পেশা:\s*(.+)', line)
                    if profession_match:
                        current_entry['পেশা'] = profession_match.group(1).strip()
                    
                    # Extract birth date
                    dob_match = re.search(r'জন্ম\s*তারিখ:\s*([\d/]+)', line)
                    if dob_match:
                        current_entry['জন্ম_তারিখ'] = dob_match.group(1)
                    
                    # Extract address
                    address_match = re.search(r'ঠিকানা:\s*(.+)', line)
                    if address_match:
                        current_entry['ঠিকানা'] = address_match.group(1).strip()
                
                # Add the last entry
                if current_entry:
                    voter_data.append(current_entry)
    
    return voter_data

# Sample data for testing
def get_sample_data():
    return [
        {
            'ক্রমিক_নং': '১',
            'নাম': 'মোসাম্মৎ জোবেদা খাতুন',
            'ভোটার_নম্বর': '902090805611',
            'পিতার_নাম': 'আব্দুল সামাদ',
            'মাতার_নাম': 'ফুলবান',
            'পেশা': 'গৃহিণী',
            'জন্ম_তারিখ': '১২/০২/১৯৬২',
            'ঠিকানা': 'মৌয়াড়া, মতয়াখলা, বিরপুর, নানিয়াজ'
        }
    ]
