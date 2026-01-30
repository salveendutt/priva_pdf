from pathlib import Path

from .pdf_merger import PdfMerger
from .pdf_compressor import PdfCompressor, CompressionLevel


class PdfTool:
    def __init__(self):
        self._merger = PdfMerger()

    def merge(self, input_files: list[Path], output_file: Path) -> Path:
        return self._merger.merge(input_files, output_file)

    def compress(
        self,
        input_file: Path,
        output_file: Path | None = None,
        level: CompressionLevel = CompressionLevel.MEDIUM,
    ) -> Path:
        compressor = PdfCompressor(level)
        return compressor.compress(input_file, output_file)

    def merge_and_compress(
        self,
        input_files: list[Path],
        output_file: Path,
        compression_level: CompressionLevel = CompressionLevel.MEDIUM,
    ) -> Path:
        merged_file = self.merge(input_files, output_file)
        
        compressed_file = output_file.with_stem(f"{output_file.stem}_compressed")
        self.compress(merged_file, compressed_file, compression_level)
        
        return compressed_file
