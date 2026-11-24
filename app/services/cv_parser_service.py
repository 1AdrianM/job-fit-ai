"""CV parsing service for extracting text from PDF and DOCX files."""

import io

import docx
from PyPDF2 import PdfReader


class CVParserService:
    """Service for parsing CV files (PDF and DOCX)."""

    # Max file size: 5MB
    MAX_FILE_SIZE = 5 * 1024 * 1024

    # Allowed MIME types
    ALLOWED_TYPES = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    }

    @staticmethod
    def parse_pdf(file_content: bytes) -> str:
        """
        Extract text from PDF file.

        Args:
            file_content: Raw PDF file bytes

        Returns:
            Extracted text content
        """
        pdf_file = io.BytesIO(file_content)
        reader = PdfReader(pdf_file)

        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

        return "\n\n".join(text_parts).strip()

    @staticmethod
    def parse_docx(file_content: bytes) -> str:
        """
        Extract text from DOCX file.

        Args:
            file_content: Raw DOCX file bytes

        Returns:
            Extracted text content
        """
        docx_file = io.BytesIO(file_content)
        doc = docx.Document(docx_file)

        text_parts = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)

        return "\n\n".join(text_parts).strip()

    @staticmethod
    def validate_file(content_type: str, file_size: int) -> tuple[bool, str | None]:
        """
        Validate uploaded file.

        Args:
            content_type: MIME type of the file
            file_size: Size of the file in bytes

        Returns:
            Tuple of (is_valid, error_message)
        """
        if file_size > CVParserService.MAX_FILE_SIZE:
            return False, "File too large. Max size: 5MB"

        if file_size == 0:
            return False, "Empty file"

        if content_type not in CVParserService.ALLOWED_TYPES:
            return False, "Invalid file type. Only PDF and DOCX are supported"

        return True, None

    @staticmethod
    def parse_cv(file_content: bytes, filename: str) -> str:
        """
        Parse CV file and extract text.

        Args:
            file_content: Raw file bytes
            filename: Name of the uploaded file

        Returns:
            Extracted text content

        Raises:
            ValueError: If file type is not supported or parsing fails
        """
        filename_lower = filename.lower()

        try:
            if filename_lower.endswith(".pdf"):
                return CVParserService.parse_pdf(file_content)
            elif filename_lower.endswith((".docx", ".doc")):
                return CVParserService.parse_docx(file_content)
            else:
                raise ValueError("Unsupported file type")
        except Exception as e:
            raise ValueError(f"Failed to parse CV: {str(e)}")
