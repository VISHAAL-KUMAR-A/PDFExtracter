import pdfplumber
from pathlib import Path


class PDFExtractor:
    """Service for extracting text from PDF files"""

    def extract_text(self, pdf_path: Path) -> str:
        """
        Extract text content from a PDF file

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text as string
        """
        text_content = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text from page
                    page_text = page.extract_text()

                    if page_text:
                        text_content.append(
                            f"--- Page {page_num} ---\n{page_text}")

                    # Try to extract tables
                    tables = page.extract_tables()
                    if tables:
                        for table_idx, table in enumerate(tables, 1):
                            text_content.append(
                                f"\n--- Table {table_idx} on Page {page_num} ---")
                            for row in table:
                                if row:
                                    text_content.append(" | ".join(
                                        [str(cell) if cell else "" for cell in row]))

            return "\n".join(text_content)

        except Exception as e:
            raise Exception(
                f"Error extracting text from {pdf_path.name}: {str(e)}")
