"""
PDF Processing utilities for extracting text and structured data from PDFs
"""

import pdfplumber
from pypdf import PdfReader
import io
from typing import Dict, List, Optional, Any


class PDFProcessor:
    """Handles PDF text extraction and processing"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text(self, pdf_file) -> str:
        """
        Extract text from a PDF file
        
        Args:
            pdf_file: File-like object or path to PDF
            
        Returns:
            Extracted text as string
        """
        try:
            # Handle both file paths and file-like objects
            if isinstance(pdf_file, str):
                with pdfplumber.open(pdf_file) as pdf:
                    return self._extract_from_pdfplumber(pdf)
            else:
                # For uploaded files (BytesIO)
                pdf_bytes = pdf_file.read()
                pdf_file.seek(0)  # Reset file pointer
                
                with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                    return self._extract_from_pdfplumber(pdf)
                    
        except Exception as e:
            # Fallback to pypdf if pdfplumber fails
            return self._fallback_extraction(pdf_file, str(e))
    
    def _extract_from_pdfplumber(self, pdf) -> str:
        """Extract text using pdfplumber"""
        text_parts = []
        
        for page_num, page in enumerate(pdf.pages, 1):
            page_text = page.extract_text()
            if page_text:
                text_parts.append(f"--- Page {page_num} ---\n{page_text}")
        
        return "\n\n".join(text_parts)
    
    def _fallback_extraction(self, pdf_file, error_msg: str) -> str:
        """Fallback extraction using pypdf"""
        try:
            if isinstance(pdf_file, str):
                reader = PdfReader(pdf_file)
            else:
                pdf_file.seek(0)
                reader = PdfReader(pdf_file)
            
            text_parts = []
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(f"--- Page {page_num} ---\n{page_text}")
            
            return "\n\n".join(text_parts)
            
        except Exception as e:
            return f"Error extracting PDF: {error_msg}. Fallback also failed: {str(e)}"
    
    def extract_tables(self, pdf_file) -> List[List[List[str]]]:
        """
        Extract tables from PDF
        
        Returns:
            List of tables, where each table is a list of rows
        """
        tables = []
        
        try:
            if isinstance(pdf_file, str):
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        page_tables = page.extract_tables()
                        if page_tables:
                            tables.extend(page_tables)
            else:
                pdf_bytes = pdf_file.read()
                pdf_file.seek(0)
                
                with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                    for page in pdf.pages:
                        page_tables = page.extract_tables()
                        if page_tables:
                            tables.extend(page_tables)
                            
        except Exception as e:
            print(f"Table extraction error: {e}")
        
        return tables
    
    def get_metadata(self, pdf_file) -> Dict[str, Any]:
        """Extract PDF metadata"""
        metadata = {
            "title": None,
            "author": None,
            "subject": None,
            "page_count": 0,
            "creation_date": None
        }
        
        try:
            if isinstance(pdf_file, str):
                reader = PdfReader(pdf_file)
            else:
                pdf_file.seek(0)
                reader = PdfReader(pdf_file)
            
            meta = reader.metadata
            if meta:
                metadata["title"] = meta.title
                metadata["author"] = meta.author
                metadata["subject"] = meta.subject
                metadata["creation_date"] = str(meta.creation_date) if meta.creation_date else None
            
            metadata["page_count"] = len(reader.pages)
            
        except Exception as e:
            print(f"Metadata extraction error: {e}")
        
        return metadata
    
    def extract_structured_content(self, pdf_file) -> Dict[str, Any]:
        """
        Extract structured content including text, tables, and metadata
        
        Returns:
            Dictionary with text, tables, and metadata
        """
        return {
            "text": self.extract_text(pdf_file),
            "tables": self.extract_tables(pdf_file),
            "metadata": self.get_metadata(pdf_file)
        }
