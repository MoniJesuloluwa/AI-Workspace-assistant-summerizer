import os
import PyPDF2
import docx


class FileAnalyzer:
    """
    Extracts readable text from multiple file types
    so it can be indexed or summarized.
    """

    TEXT_EXT = [".txt", ".md", ".py", ".js", ".json", ".csv"]
    DOC_EXT = [".docx"]
    PDF_EXT = [".pdf"]

    def extract_text(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()

        if ext in self.TEXT_EXT:
            return self._read_plain_text(file_path)

        elif ext in self.DOC_EXT:
            return self._read_docx(file_path)

        elif ext in self.PDF_EXT:
            return self._read_pdf(file_path)

        # Unsupported file types are skipped safely
        return ""

    def _read_plain_text(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception:
            return ""

    def _read_docx(self, file_path: str) -> str:
        try:
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception:
            return ""

    def _read_pdf(self, file_path: str) -> str:
        text = ""
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception:
            return text
        return text
