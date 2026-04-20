from rag_engine.ingestion import extract_clean_text,extract_pdf_text
from rag_engine.cleaning import extract_clean_text

pdf_path = "rag_engine/documents/Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.pdf"
#text = extract_clean_text(pdf_path)
raw_text = extract_pdf_text(pdf_path)
cleaned_text = extract_clean_text(pdf_path)
print(f"RAW TEXT : {raw_text[:1000]}")
print(f"Cleaned text : {cleaned_text[:1000]}")


