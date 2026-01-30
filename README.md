# 🔒 Priva PDF

A local-first PDF tool for merging and compressing documents. Built for privacy—your sensitive files never leave your machine.

No cloud uploads. No tracking. No bloat.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Merge PDFs

```bash
python main.py merge file1.pdf file2.pdf file3.pdf -o combined.pdf
```

### Compress a PDF

```bash
# Default medium compression
python main.py compress large_scan.pdf -o smaller.pdf

# High compression for iPhone scans
python main.py compress iphone_scan.pdf -l high

# Extreme compression (lower quality)
python main.py compress document.pdf -l extreme
```

### Merge and Compress

```bash
python main.py merge-compress scan1.pdf scan2.pdf -o final.pdf -l high
```

## Compression Levels

| Level    | Quality | Best For                        |
|----------|---------|----------------------------------|
| low      | 85%     | Documents needing minimal reduction |
| medium   | 65%     | General purpose (default)        |
| high     | 45%     | iPhone scans, image-heavy PDFs   |
| extreme  | 25%     | Maximum compression, lower quality |

## Programmatic Usage

```python
from pathlib import Path
from src.pdf_tool import PdfTool
from src.pdf_compressor import CompressionLevel

tool = PdfTool()

# Merge PDFs
tool.merge(
    [Path("doc1.pdf"), Path("doc2.pdf")],
    Path("merged.pdf")
)

# Compress a PDF
tool.compress(
    Path("large.pdf"),
    Path("small.pdf"),
    CompressionLevel.HIGH
)

# Merge and compress in one step
tool.merge_and_compress(
    [Path("scan1.pdf"), Path("scan2.pdf")],
    Path("output.pdf"),
    CompressionLevel.HIGH
)
```

## Why Use This?

- **Privacy First**: No cloud, no uploads, no tracking
- **Simple & Transparent**: See exactly how your data is handled
- **No Bloat**: No heavy PDF suites or browser extensions needed
