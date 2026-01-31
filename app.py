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
    initial_sidebar_state="collapsed",
)

# Custom CSS for a more polished look
st.markdown("""
<style>
    /* Import font - using a more retro-friendly font */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    
    .main-header .logo-icon {
        font-size: 3.5rem;
        filter: grayscale(100%) brightness(2);
        opacity: 0.9;
    }
    
    .main-header h1 {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #b45309 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        color: #a8a29e;
        font-size: 1.1rem;
        letter-spacing: 0.02em;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: rgba(245, 158, 11, 0.08);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.7);
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: rgba(255, 255, 255, 0.9);
        background-color: rgba(245, 158, 11, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: #1c1917 !important;
        font-weight: 600 !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        border: 2px dashed rgba(245, 158, 11, 0.3);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #f59e0b;
        background-color: rgba(245, 158, 11, 0.05);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: #1c1917;
        box-shadow: 0 4px 14px 0 rgba(245, 158, 11, 0.35);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.45);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #78716c 0%, #57534e 100%);
        border-radius: 8px;
        border: none;
        font-weight: 600;
        box-shadow: 0 4px 14px 0 rgba(120, 113, 108, 0.35);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(120, 113, 108, 0.45);
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.08) 100%);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
    
    [data-testid="stMetric"] label {
        color: #a8a29e;
        font-weight: 500;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #fafaf9;
        font-weight: 700;
    }
    
    /* Info/Success/Error boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid rgba(245, 158, 11, 0.2);
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #f59e0b;
        box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #78716c;
        font-size: 0.875rem;
    }
    
    .footer .privacy-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.1) 100%);
        color: #f59e0b;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    /* File list styling */
    .file-list {
        background: rgba(245, 158, 11, 0.05);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(245, 158, 11, 0.3), transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="logo-icon">▢</div>
    <h1>Priva PDF</h1>
    <p>Private, local PDF tools — your files never leave your machine</p>
</div>
""", unsafe_allow_html=True)

# Initialize the PDF tool
pdf_tool = PdfTool()

# Create tabs for different functionalities
tab_merge, tab_compress, tab_merge_compress = st.tabs([
    "Merge PDFs", 
    "Compress PDF", 
    "Merge & Compress"
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
    st.markdown("### Merge Multiple PDFs")
    st.markdown("<p style='color: #a8a29e; margin-bottom: 1.5rem;'>Combine multiple PDF files into a single document.</p>", unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Drop PDF files here or click to browse",
        type=["pdf"],
        accept_multiple_files=True,
        key="merge_upload",
        help="Select 2 or more PDF files to merge"
    )
    
    if uploaded_files:
        st.markdown(f"""<div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.1) 100%); 
            border-radius: 12px; padding: 1rem; margin: 1rem 0; border-left: 4px solid #f59e0b;'>
            <strong>{len(uploaded_files)} file(s) ready to merge</strong></div>""", unsafe_allow_html=True)
        for i, f in enumerate(uploaded_files, 1):
            st.markdown(f"<span style='color: #d6d3d1;'>{i}. **{f.name}** <span style='color: #78716c;'>({f.size / 1024:.1f} KB)</span></span>", unsafe_allow_html=True)
        
        output_name = st.text_input(
            "Output filename",
            value="merged.pdf",
            key="merge_output_name"
        )
        
        if not output_name.endswith(".pdf"):
            output_name += ".pdf"
        
        if st.button("Merge PDFs", type="primary", key="merge_btn"):
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
                            
                            st.success(f"Successfully merged {len(uploaded_files)} PDFs!")
                            st.download_button(
                                label="Download Merged PDF",
                                data=result_bytes,
                                file_name=output_name,
                                mime="application/pdf",
                            )
                    except Exception as e:
                        st.error(f"Error merging PDFs: {str(e)}")


# ===== COMPRESS TAB =====
with tab_compress:
    st.markdown("### Compress a PDF")
    st.markdown("<p style='color: #a8a29e; margin-bottom: 1.5rem;'>Reduce PDF file size by compressing embedded images.</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Drop a PDF file here or click to browse",
        type=["pdf"],
        key="compress_upload",
    )
    
    if uploaded_file:
        original_size_kb = uploaded_file.size / 1024
        st.markdown(f"""<div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.1) 100%); 
            border-radius: 12px; padding: 1rem; margin: 1rem 0; border-left: 4px solid #d97706;'>
            <strong>{uploaded_file.name}</strong> — Original size: <strong>{original_size_kb:.1f} KB</strong></div>""", unsafe_allow_html=True)
        
        compression_level = compression_level_selector("compress_level")
        
        output_name = st.text_input(
            "Output filename",
            value=f"{Path(uploaded_file.name).stem}_compressed.pdf",
            key="compress_output_name"
        )
        
        if not output_name.endswith(".pdf"):
            output_name += ".pdf"
        
        if st.button("Compress PDF", type="primary", key="compress_btn"):
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
                        
                        st.success(f"Compression complete!")
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Original Size", f"{original_size_kb:.1f} KB")
                        col2.metric("Compressed Size", f"{new_size_kb:.1f} KB")
                        col3.metric("Reduction", f"{reduction:.1f}%")
                        
                        st.download_button(
                            label="Download Compressed PDF",
                            data=result_bytes,
                            file_name=output_name,
                            mime="application/pdf",
                        )
                except Exception as e:
                    st.error(f"Error compressing PDF: {str(e)}")


# ===== MERGE & COMPRESS TAB =====
with tab_merge_compress:
    st.markdown("### Merge & Compress PDFs")
    st.markdown("<p style='color: #a8a29e; margin-bottom: 1.5rem;'>Combine multiple PDFs into one and compress the result.</p>", unsafe_allow_html=True)
    
    uploaded_files_mc = st.file_uploader(
        "Drop PDF files here or click to browse",
        type=["pdf"],
        accept_multiple_files=True,
        key="merge_compress_upload",
        help="Select 2 or more PDF files"
    )
    
    if uploaded_files_mc:
        st.markdown(f"""<div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(180, 83, 9, 0.1) 100%); 
            border-radius: 12px; padding: 1rem; margin: 1rem 0; border-left: 4px solid #b45309;'>
            <strong>{len(uploaded_files_mc)} file(s) ready</strong></div>""", unsafe_allow_html=True)
        total_size = 0
        for i, f in enumerate(uploaded_files_mc, 1):
            st.markdown(f"<span style='color: #d6d3d1;'>{i}. **{f.name}** <span style='color: #78716c;'>({f.size / 1024:.1f} KB)</span></span>", unsafe_allow_html=True)
            total_size += f.size
        
        st.markdown(f"""<div style='background: rgba(245, 158, 11, 0.08); border-radius: 8px; padding: 0.75rem; margin-top: 0.5rem; text-align: center; border: 1px solid rgba(245, 158, 11, 0.2);'>
            Total input size: <strong>{total_size / 1024:.1f} KB</strong></div>""", unsafe_allow_html=True)
        
        compression_level_mc = compression_level_selector("merge_compress_level")
        
        output_name_mc = st.text_input(
            "Output filename",
            value="merged_compressed.pdf",
            key="merge_compress_output_name"
        )
        
        if not output_name_mc.endswith(".pdf"):
            output_name_mc += ".pdf"
        
        if st.button("Merge & Compress", type="primary", key="merge_compress_btn"):
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
                            
                            st.success(f"Successfully merged and compressed {len(uploaded_files_mc)} PDFs!")
                            
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Original Total", f"{total_size_kb:.1f} KB")
                            col2.metric("Final Size", f"{new_size_kb:.1f} KB")
                            col3.metric("Reduction", f"{reduction:.1f}%")
                            
                            st.download_button(
                                label="Download Result",
                                data=result_bytes,
                                file_name=output_name_mc,
                                mime="application/pdf",
                            )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")


# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="footer">
        <div class="privacy-badge">
            100% Private — All processing happens locally
        </div>
        <p style="margin-top: 1rem; font-size: 0.8rem;">Your files never leave your machine</p>
    </div>
    """,
    unsafe_allow_html=True
)
