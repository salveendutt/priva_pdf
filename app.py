import streamlit as st
from pathlib import Path
import tempfile
import os

from src.pdf_tool import PdfTool
from src.pdf_compressor import CompressionLevel

st.set_page_config(
    page_title="Priva PDF",
    page_icon="📄",
    layout="centered",
)

st.title("📄 Priva PDF")
st.markdown("*Private, local PDF tools - your files never leave your machine*")

# Initialize the PDF tool
pdf_tool = PdfTool()

# Create tabs for different functionalities
tab_merge, tab_compress, tab_merge_compress = st.tabs([
    "🔗 Merge PDFs", 
    "🗜️ Compress PDF", 
    "🔗🗜️ Merge & Compress"
])

# Helper function for compression level selection
def compression_level_selector(key: str) -> CompressionLevel:
    level_descriptions = {
        "Low": "Minimal compression, best quality (85% quality, no scaling)",
        "Medium": "Balanced compression (65% quality, 85% scale)",
        "High": "Strong compression, smaller file (45% quality, 70% scale)",
        "Extreme": "Maximum compression, lowest quality (25% quality, 50% scale)",
    }
    
    level = st.selectbox(
        "Compression Level",
        options=["Low", "Medium", "High", "Extreme"],
        index=1,  # Default to Medium
        key=key,
        help="Select how aggressively to compress images in the PDF"
    )
    
    st.caption(level_descriptions[level])
    
    level_map = {
        "Low": CompressionLevel.LOW,
        "Medium": CompressionLevel.MEDIUM,
        "High": CompressionLevel.HIGH,
        "Extreme": CompressionLevel.EXTREME,
    }
    return level_map[level]


def get_file_size_mb(file_path: Path) -> float:
    return file_path.stat().st_size / (1024 * 1024)


# ===== MERGE TAB =====
with tab_merge:
    st.header("Merge Multiple PDFs")
    st.markdown("Combine multiple PDF files into a single document.")
    
    uploaded_files = st.file_uploader(
        "Upload PDF files to merge",
        type=["pdf"],
        accept_multiple_files=True,
        key="merge_upload",
        help="Select 2 or more PDF files to merge"
    )
    
    if uploaded_files:
        st.markdown(f"**{len(uploaded_files)} file(s) selected:**")
        for i, f in enumerate(uploaded_files, 1):
            st.text(f"{i}. {f.name} ({f.size / 1024:.1f} KB)")
        
        output_name = st.text_input(
            "Output filename",
            value="merged.pdf",
            key="merge_output_name"
        )
        
        if not output_name.endswith(".pdf"):
            output_name += ".pdf"
        
        if st.button("🔗 Merge PDFs", type="primary", key="merge_btn"):
            if len(uploaded_files) < 2:
                st.error("Please upload at least 2 PDF files to merge.")
            else:
                with st.spinner("Merging PDFs..."):
                    try:
                        with tempfile.TemporaryDirectory() as tmp_dir:
                            tmp_path = Path(tmp_dir)
                            
                            # Save uploaded files to temp directory
                            input_paths = []
                            for f in uploaded_files:
                                file_path = tmp_path / f.name
                                file_path.write_bytes(f.read())
                                input_paths.append(file_path)
                            
                            # Merge PDFs
                            output_path = tmp_path / output_name
                            result_path = pdf_tool.merge(input_paths, output_path)
                            
                            # Read result for download
                            result_bytes = result_path.read_bytes()
                            
                            st.success(f"✅ Successfully merged {len(uploaded_files)} PDFs!")
                            st.download_button(
                                label="⬇️ Download Merged PDF",
                                data=result_bytes,
                                file_name=output_name,
                                mime="application/pdf",
                            )
                    except Exception as e:
                        st.error(f"Error merging PDFs: {str(e)}")


# ===== COMPRESS TAB =====
with tab_compress:
    st.header("Compress a PDF")
    st.markdown("Reduce PDF file size by compressing embedded images.")
    
    uploaded_file = st.file_uploader(
        "Upload a PDF file to compress",
        type=["pdf"],
        key="compress_upload",
    )
    
    if uploaded_file:
        original_size_kb = uploaded_file.size / 1024
        st.info(f"📁 **{uploaded_file.name}** - Original size: {original_size_kb:.1f} KB")
        
        compression_level = compression_level_selector("compress_level")
        
        output_name = st.text_input(
            "Output filename",
            value=f"{Path(uploaded_file.name).stem}_compressed.pdf",
            key="compress_output_name"
        )
        
        if not output_name.endswith(".pdf"):
            output_name += ".pdf"
        
        if st.button("🗜️ Compress PDF", type="primary", key="compress_btn"):
            with st.spinner("Compressing PDF..."):
                try:
                    with tempfile.TemporaryDirectory() as tmp_dir:
                        tmp_path = Path(tmp_dir)
                        
                        # Save uploaded file
                        input_path = tmp_path / uploaded_file.name
                        input_path.write_bytes(uploaded_file.read())
                        
                        # Compress PDF
                        output_path = tmp_path / output_name
                        result_path = pdf_tool.compress(
                            input_path, 
                            output_path, 
                            compression_level
                        )
                        
                        # Calculate size reduction
                        result_bytes = result_path.read_bytes()
                        new_size_kb = len(result_bytes) / 1024
                        reduction = ((original_size_kb - new_size_kb) / original_size_kb) * 100
                        
                        st.success(f"✅ Compression complete!")
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Original Size", f"{original_size_kb:.1f} KB")
                        col2.metric("Compressed Size", f"{new_size_kb:.1f} KB")
                        col3.metric("Reduction", f"{reduction:.1f}%")
                        
                        st.download_button(
                            label="⬇️ Download Compressed PDF",
                            data=result_bytes,
                            file_name=output_name,
                            mime="application/pdf",
                        )
                except Exception as e:
                    st.error(f"Error compressing PDF: {str(e)}")


# ===== MERGE & COMPRESS TAB =====
with tab_merge_compress:
    st.header("Merge & Compress PDFs")
    st.markdown("Combine multiple PDFs into one and compress the result.")
    
    uploaded_files_mc = st.file_uploader(
        "Upload PDF files to merge and compress",
        type=["pdf"],
        accept_multiple_files=True,
        key="merge_compress_upload",
        help="Select 2 or more PDF files"
    )
    
    if uploaded_files_mc:
        st.markdown(f"**{len(uploaded_files_mc)} file(s) selected:**")
        total_size = 0
        for i, f in enumerate(uploaded_files_mc, 1):
            st.text(f"{i}. {f.name} ({f.size / 1024:.1f} KB)")
            total_size += f.size
        
        st.info(f"📊 Total input size: {total_size / 1024:.1f} KB")
        
        compression_level_mc = compression_level_selector("merge_compress_level")
        
        output_name_mc = st.text_input(
            "Output filename",
            value="merged_compressed.pdf",
            key="merge_compress_output_name"
        )
        
        if not output_name_mc.endswith(".pdf"):
            output_name_mc += ".pdf"
        
        if st.button("🔗🗜️ Merge & Compress", type="primary", key="merge_compress_btn"):
            if len(uploaded_files_mc) < 2:
                st.error("Please upload at least 2 PDF files to merge.")
            else:
                with st.spinner("Merging and compressing PDFs..."):
                    try:
                        with tempfile.TemporaryDirectory() as tmp_dir:
                            tmp_path = Path(tmp_dir)
                            
                            # Save uploaded files
                            input_paths = []
                            for f in uploaded_files_mc:
                                file_path = tmp_path / f.name
                                file_path.write_bytes(f.read())
                                input_paths.append(file_path)
                            
                            # Merge and compress
                            merged_path = tmp_path / "merged_temp.pdf"
                            output_path = tmp_path / output_name_mc
                            
                            # First merge
                            pdf_tool.merge(input_paths, merged_path)
                            
                            # Then compress
                            result_path = pdf_tool.compress(
                                merged_path,
                                output_path,
                                compression_level_mc
                            )
                            
                            # Read result
                            result_bytes = result_path.read_bytes()
                            new_size_kb = len(result_bytes) / 1024
                            total_size_kb = total_size / 1024
                            reduction = ((total_size_kb - new_size_kb) / total_size_kb) * 100
                            
                            st.success(f"✅ Successfully merged and compressed {len(uploaded_files_mc)} PDFs!")
                            
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Original Total", f"{total_size_kb:.1f} KB")
                            col2.metric("Final Size", f"{new_size_kb:.1f} KB")
                            col3.metric("Reduction", f"{reduction:.1f}%")
                            
                            st.download_button(
                                label="⬇️ Download Merged & Compressed PDF",
                                data=result_bytes,
                                file_name=output_name_mc,
                                mime="application/pdf",
                            )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")


# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <small>🔒 All processing happens locally on your machine. Your files are never uploaded to any server.</small>
    </div>
    """,
    unsafe_allow_html=True
)
