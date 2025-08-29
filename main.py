import fitz  # PyMuPDF
from pathlib import Path

pdf_path = "filepath" #adjust later on
out_dir = Path("exported_pages")
out_dir.mkdir(exist_ok=True)

DPI = 400                    # 300 is good, 400–600 for extra crispness
USE_PNG = True               # True = PNG (lossless, larger). False = JPEG
JPEG_QUALITY = 95            # Only used if USE_PNG=False

doc = fitz.open(pdf_path)
zoom = DPI / 72.0            # PDF units are 72 DPI
mat = fitz.Matrix(zoom, zoom)

for i in range(len(doc)):
    page = doc[i]
    pix = page.get_pixmap(matrix=mat, alpha=False)  # alpha=False avoids transparent bgs
    if USE_PNG:
        pix.save(out_dir / f"page-{i+1}.png")
    else:
        pix.save(out_dir / f"page-{i+1}.jpg", quality=JPEG_QUALITY)

doc.close()
print(f"Done. Saved {len(doc)} pages at ~{DPI} DPI to {out_dir.resolve()}")
