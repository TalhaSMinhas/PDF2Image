import fitz  # PyMuPDF
from pathlib import Path

pdf_dir = Path("/Users/talhaminhas/Downloads/pdf_test")   # change this
out_dir = Path("exported_pages_multi")
out_dir.mkdir(exist_ok=True)

DPI = 400
USE_PNG = True
JPEG_QUALITY = 95

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
