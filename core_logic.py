import fitz  # PyMuPDF
from pathlib import Path

DPI = 400
USE_PNG = True
JPEG_QUALITY = 95

def receive_paths(input_path: Path, output_path: Path):
    input_path = Path(input_path).expanduser().resolve()
    output_path = Path(output_path).expanduser().resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")
    if input_path.is_file():
        raise NotADirectoryError(f"Expected a folder, got a file: {input_path}")

    output_path.mkdir(parents=True, exist_ok=True)

    return [input_path, output_path]


'''
pdf_dir = Path()   # change this
out_dir = Path("exported_pages_multi")
out_dir.mkdir(exist_ok=True)

zoom = DPI / 72.0
mat = fitz.Matrix(zoom, zoom)

for pdf_path in list(pdf_dir.glob("*.pdf")) + list(pdf_dir.glob("*.PDF")):
    print(f"Processing {pdf_path.name} ...")
    try:
        with fitz.open(pdf_path) as doc:
            pages_done = 0
            for i, page in enumerate(doc, start=1):
                pix = page.get_pixmap(matrix=mat, alpha=False)
                if USE_PNG:
                    pix.save(out_dir / f"{pdf_path.stem}-page-{i}.png")
                else:
                    pix.save(out_dir / f"{pdf_path.stem}-page-{i}.jpg", quality=JPEG_QUALITY)
                pages_done += 1

        print(f"✔ Saved {pages_done} pages from {pdf_path.name}")
    except Exception as e:
        print(f"⚠️ Skipped {pdf_path.name}: {e}")

print("✅ All PDFs processed. Images are in:", out_dir.resolve())

'''

if __name__ == "__main__":
    i, o = receive_paths(Path.cwd(), Path.cwd())
    print(i, o)