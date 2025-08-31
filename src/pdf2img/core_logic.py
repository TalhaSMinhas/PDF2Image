import fitz  # PyMuPDF
from pathlib import Path
from rich.progress import Progress, BarColumn, TimeRemainingColumn, TimeElapsedColumn, TaskProgressColumn

DPI = 400
USE_PNG = True
JPEG_QUALITY = 95

def process(input_path: Path, output_path: Path):
    pdf_dir = Path(input_path)
    out_dir = Path(output_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    zoom = DPI / 72.0
    mat = fitz.Matrix(zoom, zoom)

    pdfs = [p for p in pdf_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"]
    if not pdfs:
        print("No PDFs found.")
        return

    file_pages = []
    total_pages = 0
    for pdf_path in pdfs:
        try:
            with fitz.open(pdf_path) as doc:
                pages = doc.page_count
            file_pages.append((pdf_path, pages))
            total_pages += pages
        except Exception as e:
            print(f"⚠️ Skipped counting {pdf_path.name}: {e}")

    if total_pages == 0:
        print("No pages to process.")
        return

    columns = (
        "[progress.description]{task.description}",
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    )

    with Progress(*columns, transient=False) as progress:
        task = progress.add_task("Processing all PDFs", total=total_pages)

        for pdf_path, pages in file_pages:
            try:
                with fitz.open(pdf_path) as doc:
                    for i, page in enumerate(doc, start=1):
                        pix = page.get_pixmap(matrix=mat, alpha=False)
                        if USE_PNG:
                            pix.save(out_dir / f"{pdf_path.stem}-page-{i}.png")
                        else:
                            pix.save(out_dir / f"{pdf_path.stem}-page-{i}.jpg", quality=JPEG_QUALITY)
                        progress.advance(task)
                progress.console.log(f"✔ Saved {pages} pages from {pdf_path.name}")
            except Exception as e:
                progress.console.log(f"⚠️ Skipped {pdf_path.name}: {e}")

    print("✅ All PDFs processed. Images are in:", out_dir.resolve())

def receive_paths(input_path: Path, output_path: Path):
    input_path = Path(input_path).expanduser().resolve()
    output_path = Path(output_path).expanduser().resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")
    if input_path.is_file():
        raise NotADirectoryError(f"Expected a folder, got a file: {input_path}")

    process(input_path, output_path)

    return 0

if __name__ == "__main__":
    i, o = receive_paths(Path.cwd(), Path.cwd())
    print(i, o)