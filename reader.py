import fitz  # pymupdf
from typing import List, Dict, Optional
from pathlib import Path
import io
from llama_index.core.schema import Document
from llama_index.core.readers.file.base import get_default_fs, is_default_fs
from llama_index.core.readers.base import BaseReader


class PDFReader(BaseReader):
    """PDF parser using pymupdf."""

    def __init__(self, return_full_document: Optional[bool] = False) -> None:
        """
        Initialize PDFReader.
        """
        self.return_full_document = return_full_document

    def load_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
    ) -> List[Document]:
        """Parse file."""
        if not isinstance(file, Path):
            file = Path(file)

        try:
            import fitz  # pymupdf
        except ImportError:
            raise ImportError(
                "pymupdf is required to read PDF files: `pip install pymupdf`"
            )
        fs = get_default_fs()
        with fs.open(str(file), "rb") as fp:
            # Load the file in memory if the filesystem is not the default one to avoid
            # issues with pymupdf
            # stream = fp if is_default_fs(fs) else io.BytesIO(fp.read())

            # Create a PDF object
            pdf = fitz.open(fp)

            # Get the number of pages in the PDF document
            num_pages = len(pdf)

            docs = []

            # This block returns a whole PDF as a single Document
            if self.return_full_document:
                metadata = {"file_name": file.name}
                if extra_info is not None:
                    metadata.update(extra_info)

                # Join text extracted from each page
                text = "\n".join(
                    pdf.load_page(page).get_text() for page in range(num_pages)
                )

                docs.append(Document(text=text, metadata=metadata))

            # This block returns each page of a PDF as its own Document
            else:
                # Iterate over every page
                for page in range(num_pages):
                    # Extract the text from the page
                    page_text = pdf.load_page(page).get_text()
                    page_label = int(page + 1)  # pymupdf does not provide page labels directly

                    metadata = {"page_label": page_label, "file_name": file.name}
                    if extra_info is not None:
                        metadata.update(extra_info)

                    docs.append(Document(text=page_text, metadata=metadata))

            return docs