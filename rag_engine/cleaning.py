import re
import unicodedata
import fitz
from pathlib import Path


# ─── Symbol & Noise Tables ────────────────────────────────────────────────────

# Academic footnote/affiliation symbols that pollute embeddings
ACADEMIC_NOISE_PATTERN = re.compile(
    r'[†‡⋆∗•◦‣⁎⁺⁻⁼⁽⁾ⁿ⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉]'
)

# Common PDF section headers to strip (extend as needed)
HEADER_FOOTER_PATTERN = re.compile(
    r'^\s*(abstract|introduction|references|acknowledgements?|'
    r'appendix|table of contents|contents|index)\s*$',
    re.IGNORECASE | re.MULTILINE
)

# Email addresses, URLs, DOIs → noise for semantic search
URL_EMAIL_PATTERN = re.compile(
    r'(https?://\S+|www\.\S+|doi:\S+|\S+@\S+\.\S+)'
)

# Author affiliation lines: "¹ MIT, ² Stanford" style
AFFILIATION_LINE_PATTERN = re.compile(
    r'^\s*[\d†‡⋆∗]+\s+[A-Z][^\n]{0,80}(university|institute|lab|department|dept|'
    r'school|college|research|inc\.|corp\.|ltd\.)[^\n]*$',
    re.IGNORECASE | re.MULTILINE
)


# ─── Core Cleaning Pipeline ───────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """
    RAG-optimized text cleaning pipeline.
    Goal: continuous semantic prose, no symbols, no structural noise.
    """

    # ── Step 1: Unicode normalization (ligatures, special spaces, etc.)
    # NFKC: ﬁ→fi, ﬀ→ff, non-breaking spaces→space, etc.
    text = unicodedata.normalize("NFKC", text)

    # ── Step 2: Remove academic noise symbols (†‡⋆ etc.)
    text = ACADEMIC_NOISE_PATTERN.sub('', text)

    # ── Step 3: Strip URLs, emails, DOIs (not semantically useful for RAG)
    text = URL_EMAIL_PATTERN.sub('', text)

    # ── Step 4: Remove affiliation lines ("¹ MIT CSAIL, Cambridge MA")
    text = AFFILIATION_LINE_PATTERN.sub('', text)

    # ── Step 5: Remove section header-only lines (they fragment chunks)
    text = HEADER_FOOTER_PATTERN.sub('', text)

    # ── Step 6: Fix hyphenation across line breaks
    # "knowl-\nedge" → "knowledge"
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)

    # ── Step 7: Collapse inline line breaks → single space
    # "Patrick Lewis\nEthan Perez" → "Patrick Lewis Ethan Perez"
    # But preserve intentional paragraph breaks (double newline)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

    # ── Step 8: Collapse multiple spaces/tabs → single space
    text = re.sub(r'[ \t]{2,}', ' ', text)

    # ── Step 9: Collapse 3+ newlines → paragraph break (double newline)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # ── Step 10: Remove stray punctuation left after symbol removal
    # e.g. ", ," or "( )" or lines that became just punctuation
    text = re.sub(r'\s*,\s*,', ',', text)
    text = re.sub(r'^\s*[,;:\-–—|]+\s*$', '', text, flags=re.MULTILINE)

    # ── Step 11: Remove control characters (keep \n)
    text = re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', '', text)

    # ── Step 12: Clean up blank lines left by removals above
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)

    return text.strip()


# ─── Garbage Detection ────────────────────────────────────────────────────────

def is_garbage_page(text: str, min_chars: int = 80) -> bool:
    """
    Filters out: blank pages, cover pages, image-only pages,
    pure reference lists, and pages with near-zero prose.
    """
    if len(text) < min_chars:
        return True

    # Alphanumeric ratio — image-only or symbol-heavy pages score very low
    alpha_ratio = sum(c.isalnum() for c in text) / max(len(text), 1)
    if alpha_ratio < 0.25:
        return True

    # Pages that are >60% digits → likely a table of numbers, not prose
    digit_ratio = sum(c.isdigit() for c in text) / max(len(text), 1)
    if digit_ratio > 0.6:
        return True

    # Fewer than 10 words → not enough content to chunk meaningfully
    if len(text.split()) < 10:
        return True

    return False


# ─── Extraction Entry Point ───────────────────────────────────────────────────

def extract_clean_text(file_path: str) -> str:
    """
    Extract and clean all pages from a PDF.
    Returns a single clean string of continuous semantic prose.
    """
    file_path = str(Path(file_path).resolve())

    try:
        pdf = fitz.open(file_path)
    except Exception as e:
        raise RuntimeError(f"Failed to open PDF: {e}")

    pages_text = []

    for page_num, page in enumerate(pdf, start=1):
        raw_text = page.get_text()
        cleaned = clean_text(raw_text)

        if is_garbage_page(cleaned):
            continue

        pages_text.append(cleaned)

    pdf.close()

    # Join pages with paragraph break so chunker sees a clean boundary
    return '\n\n'.join(pages_text)