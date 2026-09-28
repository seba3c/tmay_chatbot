from pathlib import Path

import pymupdf
import pymupdf4llm


def pdf_to_markdown(pdf_path: str | Path, output_path: str | Path | None = None) -> str:
    """Extract a PDF's content as Markdown text and save it to a file.

    Args:
        pdf_path: Path to a local PDF file.
        output_path: Where to save the Markdown output. Defaults to
            pdf_path with its extension replaced by ".md".

    Returns:
        The PDF's content converted to a Markdown-formatted string.

    Raises:
        FileNotFoundError: If pdf_path does not exist.
        ValueError: If the file cannot be opened as a PDF, or is password-protected.
    """
    path = Path(pdf_path)
    if not path.is_file():
        raise FileNotFoundError(f"PDF file not found: {path}")

    try:
        doc = pymupdf.open(path)
    except Exception as exc:
        raise ValueError(f"Could not open '{path}' as a PDF") from exc

    try:
        if doc.needs_pass:
            raise ValueError(f"PDF '{path}' is password-protected")
        markdown = pymupdf4llm.to_markdown(doc)
    finally:
        doc.close()

    out_path = Path(output_path) if output_path is not None else path.with_suffix(".md")
    out_path.write_text(markdown)

    return markdown


if __name__ == "__main__":
    import sys

    pdf_to_markdown(sys.argv[1])
