import fitz
import re
import unicodedata
from pathlib import Path

pages = []
#basic cleaning
def extract_pdf_text(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text+=page.get_text()
    return text

#medium level cleaning
def load_preprocess(file_path) :
    doc = fitz.open(file_path)
    
    for i,page in enumerate(doc) :
        text = page.get_text()
        text = re.sub(r'\s+'," ",text) #remove spaces
        text = re.sub(r'-\s+','',text) #hyphenation
        text = text.strip()
        if not text :
            continue
        pages.append(
            {
            "page_number" : i+1,
            "content" : text
            })
    return pages



#advanced cleaning
def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC",text)
    text = re.sub(r'-\s*\n\s*','',text)
    text = re.sub(r'[\t]+',' ',text)
    text = re.sub(r'\n{3,}','\n\n',text)
    text = re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', '', text)
    return text.strip()

def is_garbage_next(text: str,min_chars : int=50) -> bool :
    if(len(text)<min_chars) :
        return True
    alpha_ratio = sum(c.isalnum() for c in text)/max(len(text),1)
    if alpha_ratio < 0.2 :
        return True
    return False

def extract_clean_text (file_path: str) -> str:
    file_path = str(Path(file_path).resolve())
    try:
        pdf = fitz.open(file_path)
    except Exception as e :
        raise RuntimeError(f"Failed to open the PDF:{e}")
    
    all_text = []
    for page_num,page in enumerate(pdf,start = 1) :
        raw_text = page.get_text()
        cleaned = clean_text(raw_text)
        if is_garbage_next(cleaned) :
            continue
        all_text.append(cleaned)
    pdf.close()

    return '\n\n'.join(all_text)









                  



        

