import os
import io
import pdfplumber

try:
    from PIL import Image
    import pytesseract
except ImportError:
    pass # Expected if not installed, but we did pip install

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text from a PDF file using pdfplumber."""
    text_content = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
    return "\n".join(text_content)

def extract_text_from_image(file_bytes: bytes) -> str:
    """Extracts text from an image using Tesseract OCR."""
    try:
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"[OCR Error: {str(e)}]"

def extract_text_from_audio(file_path: str) -> str:
    """Extracts text from audio using OpenAI Whisper (local)."""
    # Note: For production with large files, we'd want this as an async background task.
    try:
        import whisper
        # Load base model (requires download on first run)
        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        return f"[Audio Transcription Error: {str(e)}]"

def process_upload(filename: str, file_bytes: bytes, file_path: str = None) -> str:
    """Routes the file to the appropriate extraction method based on extension."""
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == ".pdf":
        return extract_text_from_pdf(file_bytes)
    elif ext in [".png", ".jpg", ".jpeg", ".heic"]:
        return extract_text_from_image(file_bytes)
    elif ext in [".mp3", ".wav", ".m4a"] and file_path:
        return extract_text_from_audio(file_path)
    elif ext in [".txt", ".md", ".csv"]:
        return file_bytes.decode('utf-8')
    else:
        return "[Unsupported file format]"
