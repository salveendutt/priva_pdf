import base64
import tempfile
from pathlib import Path

from dash import Dash, dcc, html, callback, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from src.pdf_tool import PdfTool
from src.pdf_compressor import CompressionLevel

# Initialize the PDF tool
pdf_tool = PdfTool()

# Custom CSS for retro aesthetic
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

body {
    font-family: 'Space Grotesk', sans-serif;
    background: linear-gradient(135deg, #1c1917 0%, #292524 100%);
    min-height: 100vh;
    color: #fafaf9;
}

.main-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}

.main-header {
    text-align: center;
    padding: 1.5rem 0 0.75rem 0;
}

.main-header h1 {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #b45309 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.02em;
}

.main-header p {
    color: #78716c;
    font-size: 0.9rem;
    letter-spacing: 0.02em;
    margin-top: 0.25rem;
}

/* Tab styling */
.nav-tabs {
    gap: 4px;
    background-color: rgba(245, 158, 11, 0.08);
    padding: 0.5rem;
    border-radius: 12px;
    border: 1px solid rgba(245, 158, 11, 0.2);
    margin-bottom: 1.5rem;
}

.nav-tabs .nav-link {
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.7);
    background-color: transparent;
    border: none;
    transition: all 0.3s ease;
}

.nav-tabs .nav-link:hover {
    color: rgba(255, 255, 255, 0.9);
    background-color: rgba(245, 158, 11, 0.1);
    border: none;
}

.nav-tabs .nav-link.active {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
    color: #1c1917 !important;
    font-weight: 600 !important;
    border: none !important;
}

/* Upload area */
.upload-area {
    border: 2px dashed rgba(245, 158, 11, 0.3);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    transition: all 0.3s ease;
    background: rgba(245, 158, 11, 0.02);
    cursor: pointer;
}

.upload-area:hover {
    border-color: #f59e0b;
    background-color: rgba(245, 158, 11, 0.05);
}

.upload-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.upload-text {
    color: #a8a29e;
    font-size: 0.95rem;
}

/* File list */
.file-list-container {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.1) 100%);
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
    border-left: 4px solid #f59e0b;
}

.file-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(245, 158, 11, 0.1);
}

.file-item:last-child {
    border-bottom: none;
}

.file-name {
    color: #d6d3d1;
    font-weight: 500;
}

.file-size {
    color: #78716c;
    font-size: 0.85rem;
}

.reorder-btn {
    background: rgba(245, 158, 11, 0.2);
    border: none;
    border-radius: 4px;
    color: #f59e0b;
    padding: 0.25rem 0.5rem;
    cursor: pointer;
    margin: 0 2px;
    transition: all 0.2s ease;
}

.reorder-btn:hover {
    background: rgba(245, 158, 11, 0.4);
}

.reorder-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
}

/* Button styling */
.btn-primary-custom {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: #1c1917;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 14px 0 rgba(245, 158, 11, 0.35);
    cursor: pointer;
    font-size: 1rem;
}

.btn-primary-custom:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(245, 158, 11, 0.45);
}

.btn-download {
    background: linear-gradient(135deg, #78716c 0%, #57534e 100%);
    color: #fafaf9;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 14px 0 rgba(120, 113, 108, 0.35);
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    font-size: 1rem;
}

.btn-download:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(120, 113, 108, 0.45);
    color: #fafaf9;
}

/* Input styling */
.form-control, .form-select {
    background-color: rgba(28, 25, 23, 0.8);
    border: 2px solid rgba(245, 158, 11, 0.2);
    border-radius: 8px;
    padding: 0.75rem;
    color: #fafaf9;
    transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
    border-color: #f59e0b;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15);
    background-color: rgba(28, 25, 23, 0.9);
    color: #fafaf9;
}

.form-select option {
    background-color: #1c1917;
    color: #fafaf9;
}

.form-label {
    color: #a8a29e;
    font-weight: 500;
    margin-bottom: 0.5rem;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.08) 100%);
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid rgba(245, 158, 11, 0.2);
    text-align: center;
}

.metric-label {
    color: #a8a29e;
    font-weight: 500;
    font-size: 0.85rem;
    margin-bottom: 0.25rem;
}

.metric-value {
    color: #fafaf9;
    font-weight: 700;
    font-size: 1.25rem;
}

/* Alert styling */
.alert-success-custom {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(22, 163, 74, 0.1) 100%);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 12px;
    color: #86efac;
    padding: 1rem;
}

.alert-error-custom {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.1) 100%);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 12px;
    color: #fca5a5;
    padding: 1rem;
}

/* Total size box */
.total-size-box {
    background: rgba(245, 158, 11, 0.08);
    border-radius: 8px;
    padding: 0.75rem;
    margin-top: 0.5rem;
    text-align: center;
    border: 1px solid rgba(245, 158, 11, 0.2);
    color: #d6d3d1;
}

/* Compression level description */
.compression-desc {
    color: #78716c;
    font-size: 0.85rem;
    margin-top: 0.25rem;
}

/* Footer */
.footer {
    text-align: center;
    padding: 2rem 0;
    color: #78716c;
    font-size: 0.875rem;
}

.privacy-badge {
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

/* Section header */
.section-header {
    color: #fafaf9;
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.section-desc {
    color: #a8a29e;
    margin-bottom: 1.5rem;
}

/* Loading spinner */
.loading-overlay {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.spinner {
    border: 3px solid rgba(245, 158, 11, 0.1);
    border-top: 3px solid #f59e0b;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Tab pane content */
.tab-content {
    padding: 1rem 0;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(245, 158, 11, 0.3), transparent);
    margin: 2rem 0;
}

/* Dropdown styling for dark theme */
.Select-control {
    background-color: rgba(28, 25, 23, 0.8) !important;
    border: 2px solid rgba(245, 158, 11, 0.2) !important;
}

.Select-menu-outer {
    background-color: #1c1917 !important;
    border: 1px solid rgba(245, 158, 11, 0.3) !important;
}

.Select-option {
    background-color: #1c1917 !important;
    color: #fafaf9 !important;
}

.Select-option:hover {
    background-color: rgba(245, 158, 11, 0.2) !important;
}

.Select-value-label {
    color: #fafaf9 !important;
}
"""

# Compression level options
COMPRESSION_OPTIONS = [
    {"label": "Low", "value": "LOW"},
    {"label": "Medium", "value": "MEDIUM"},
    {"label": "High", "value": "HIGH"},
    {"label": "Extreme", "value": "EXTREME"},
]

COMPRESSION_DESCRIPTIONS = {
    "LOW": "Minimal compression, best quality (85% quality, no scaling)",
    "MEDIUM": "Balanced compression (65% quality, 85% scale)",
    "HIGH": "Strong compression, smaller file (45% quality, 70% scale)",
    "EXTREME": "Maximum compression, lowest quality (25% quality, 50% scale)",
}

# Initialize Dash app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
    title="Priva PDF",
)

# Inject custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
''' + CUSTOM_CSS + '''
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App layout
app.layout = html.Div([
    html.Div([
        # Header
        html.Div([
            html.H1("Priva PDF"),
            html.P("Private, local PDF tools — your files never leave your machine"),
        ], className="main-header"),
        
        # Tabs
        dbc.Tabs([
            dbc.Tab(label="Merge PDFs", tab_id="tab-merge"),
            dbc.Tab(label="Compress PDF", tab_id="tab-compress"),
            dbc.Tab(label="Merge & Compress", tab_id="tab-merge-compress"),
        ], id="tabs", active_tab="tab-merge"),
        
        # Tab content
        html.Div(id="tab-content"),
        
        # Footer
        html.Div([
            html.Div("🔒 100% Private — All processing happens locally", className="privacy-badge"),
            html.P("Your files never leave your machine", style={"marginTop": "1rem", "fontSize": "0.8rem"}),
        ], className="footer"),
        
    ], className="main-container"),
    
    # Storage for file data
    dcc.Store(id="merge-files-store", data=[]),
    dcc.Store(id="compress-file-store", data=None),
    dcc.Store(id="merge-compress-files-store", data=[]),
], style={"minHeight": "100vh"})


def create_upload_component(component_id: str, multiple: bool = False) -> html.Div:
    """Create a styled upload component."""
    return dcc.Upload(
        id=component_id,
        children=html.Div([
            html.Div("📄", className="upload-icon"),
            html.Div([
                "Drop PDF file(s) here or ",
                html.Span("click to browse", style={"color": "#f59e0b", "fontWeight": "500"}),
            ], className="upload-text"),
        ]),
        className="upload-area",
        multiple=multiple,
        accept=".pdf",
    )


def create_file_list(files: list) -> html.Div:
    """Create a styled file list."""
    if not files:
        return html.Div()
    
    items = []
    for idx, f in enumerate(files):
        items.append(html.Div([
            html.Span(f"{idx + 1}. ", style={"color": "#78716c", "marginRight": "0.5rem"}),
            html.Span(f["name"], className="file-name"),
            html.Span(f" ({f['size'] / 1024:.1f} KB)", className="file-size"),
        ], className="file-item"))
    
    return html.Div([
        html.Div([
            html.Strong(f"{len(files)} file(s) ready"),
        ]),
        html.Div(items, style={"marginTop": "0.75rem"}),
    ], className="file-list-container")


def create_compression_selector(component_id: str) -> html.Div:
    """Create compression level selector."""
    return html.Div([
        html.Label("Compression Level", className="form-label"),
        dcc.Dropdown(
            id=component_id,
            options=COMPRESSION_OPTIONS,
            value="MEDIUM",
            clearable=False,
            style={"backgroundColor": "rgba(28, 25, 23, 0.8)"},
        ),
        html.Div(id=f"{component_id}-desc", className="compression-desc"),
    ], style={"marginBottom": "1rem"})


def create_output_input(component_id: str, default_value: str) -> html.Div:
    """Create output filename input."""
    return html.Div([
        html.Label("Output filename", className="form-label"),
        dbc.Input(
            id=component_id,
            value=default_value,
            type="text",
            className="form-control",
        ),
    ], style={"marginBottom": "1rem"})


def create_metrics(original: float, compressed: float, reduction: float) -> html.Div:
    """Create metrics display."""
    return dbc.Row([
        dbc.Col(html.Div([
            html.Div("Original Size", className="metric-label"),
            html.Div(f"{original:.1f} KB", className="metric-value"),
        ], className="metric-card")),
        dbc.Col(html.Div([
            html.Div("Compressed Size", className="metric-label"),
            html.Div(f"{compressed:.1f} KB", className="metric-value"),
        ], className="metric-card")),
        dbc.Col(html.Div([
            html.Div("Reduction", className="metric-label"),
            html.Div(f"{reduction:.1f}%", className="metric-value"),
        ], className="metric-card")),
    ], className="g-3", style={"marginBottom": "1rem"})


# Callback to render tab content
@callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):
    if active_tab == "tab-merge":
        return html.Div([
            html.H3("Merge Multiple PDFs", className="section-header"),
            html.P("Combine multiple PDF files into a single document.", className="section-desc"),
            create_upload_component("merge-upload", multiple=True),
            html.Div(id="merge-file-list"),
            html.Div(id="merge-options", style={"display": "none"}, children=[
                create_output_input("merge-output-name", "merged.pdf"),
                html.Button("Merge PDFs", id="merge-btn", className="btn-primary-custom"),
            ]),
            dcc.Loading(
                html.Div(id="merge-result"),
                type="circle",
                color="#f59e0b",
            ),
        ])
    
    elif active_tab == "tab-compress":
        return html.Div([
            html.H3("Compress a PDF", className="section-header"),
            html.P("Reduce PDF file size by compressing embedded images.", className="section-desc"),
            create_upload_component("compress-upload", multiple=False),
            html.Div(id="compress-file-info"),
            html.Div(id="compress-options", style={"display": "none"}, children=[
                create_compression_selector("compress-level"),
                create_output_input("compress-output-name", "compressed.pdf"),
                html.Button("Compress PDF", id="compress-btn", className="btn-primary-custom"),
            ]),
            dcc.Loading(
                html.Div(id="compress-result"),
                type="circle",
                color="#f59e0b",
            ),
        ])
    
    elif active_tab == "tab-merge-compress":
        return html.Div([
            html.H3("Merge & Compress PDFs", className="section-header"),
            html.P("Combine multiple PDFs into one and compress the result.", className="section-desc"),
            create_upload_component("merge-compress-upload", multiple=True),
            html.Div(id="merge-compress-file-list"),
            html.Div(id="merge-compress-options", style={"display": "none"}, children=[
                create_compression_selector("merge-compress-level"),
                create_output_input("merge-compress-output-name", "merged_compressed.pdf"),
                html.Button("Merge & Compress", id="merge-compress-btn", className="btn-primary-custom"),
            ]),
            dcc.Loading(
                html.Div(id="merge-compress-result"),
                type="circle",
                color="#f59e0b",
            ),
        ])
    
    return html.Div()


# Callback for merge file upload
@callback(
    Output("merge-files-store", "data"),
    Input("merge-upload", "contents"),
    State("merge-upload", "filename"),
    State("merge-files-store", "data"),
    prevent_initial_call=True,
)
def handle_merge_upload(contents, filenames, existing_files):
    if contents is None:
        raise PreventUpdate
    
    if not isinstance(contents, list):
        contents = [contents]
        filenames = [filenames]
    
    new_files = []
    for content, filename in zip(contents, filenames):
        content_type, content_string = content.split(",")
        decoded = base64.b64decode(content_string)
        new_files.append({
            "name": filename,
            "content": content_string,
            "size": len(decoded),
        })
    
    return (existing_files or []) + new_files


# Callback for merge file list display
@callback(
    Output("merge-file-list", "children"),
    Output("merge-options", "style"),
    Input("merge-files-store", "data"),
)
def update_merge_file_list(files):
    if not files:
        return html.Div(), {"display": "none"}
    
    return create_file_list(files), {"display": "block", "marginTop": "1rem"}


# Callback for compress file upload
@callback(
    Output("compress-file-store", "data"),
    Input("compress-upload", "contents"),
    State("compress-upload", "filename"),
    prevent_initial_call=True,
)
def handle_compress_upload(content, filename):
    if content is None:
        raise PreventUpdate
    
    content_type, content_string = content.split(",")
    decoded = base64.b64decode(content_string)
    
    return {
        "name": filename,
        "content": content_string,
        "size": len(decoded),
    }


# Callback for compress file info display
@callback(
    Output("compress-file-info", "children"),
    Output("compress-options", "style"),
    Output("compress-output-name", "value"),
    Input("compress-file-store", "data"),
)
def update_compress_file_info(file_data):
    if not file_data:
        return html.Div(), {"display": "none"}, "compressed.pdf"
    
    default_name = f"{Path(file_data['name']).stem}_compressed.pdf"
    
    info = html.Div([
        html.Strong(file_data["name"]),
        html.Span(f" — Original size: ", style={"color": "#a8a29e"}),
        html.Strong(f"{file_data['size'] / 1024:.1f} KB"),
    ], className="file-list-container", style={"borderLeftColor": "#d97706"})
    
    return info, {"display": "block", "marginTop": "1rem"}, default_name


# Callback for merge-compress file upload
@callback(
    Output("merge-compress-files-store", "data"),
    Input("merge-compress-upload", "contents"),
    State("merge-compress-upload", "filename"),
    State("merge-compress-files-store", "data"),
    prevent_initial_call=True,
)
def handle_merge_compress_upload(contents, filenames, existing_files):
    if contents is None:
        raise PreventUpdate
    
    if not isinstance(contents, list):
        contents = [contents]
        filenames = [filenames]
    
    new_files = []
    for content, filename in zip(contents, filenames):
        content_type, content_string = content.split(",")
        decoded = base64.b64decode(content_string)
        new_files.append({
            "name": filename,
            "content": content_string,
            "size": len(decoded),
        })
    
    return (existing_files or []) + new_files


# Callback for merge-compress file list display
@callback(
    Output("merge-compress-file-list", "children"),
    Output("merge-compress-options", "style"),
    Input("merge-compress-files-store", "data"),
)
def update_merge_compress_file_list(files):
    if not files:
        return html.Div(), {"display": "none"}
    
    total_size = sum(f["size"] for f in files)
    file_list = create_file_list(files)
    
    total_box = html.Div([
        f"Total input size: ",
        html.Strong(f"{total_size / 1024:.1f} KB"),
    ], className="total-size-box")
    
    return html.Div([file_list, total_box]), {"display": "block", "marginTop": "1rem"}


# Callbacks for compression level descriptions
@callback(
    Output("compress-level-desc", "children"),
    Input("compress-level", "value"),
)
def update_compress_level_desc(level):
    if level:
        return COMPRESSION_DESCRIPTIONS.get(level, "")
    return ""


@callback(
    Output("merge-compress-level-desc", "children"),
    Input("merge-compress-level", "value"),
)
def update_merge_compress_level_desc(level):
    if level:
        return COMPRESSION_DESCRIPTIONS.get(level, "")
    return ""


# Callback for merge action
@callback(
    Output("merge-result", "children"),
    Input("merge-btn", "n_clicks"),
    State("merge-files-store", "data"),
    State("merge-output-name", "value"),
    prevent_initial_call=True,
)
def merge_pdfs(n_clicks, files, output_name):
    if not n_clicks or not files:
        raise PreventUpdate
    
    if len(files) < 2:
        return html.Div("Please upload at least 2 PDF files to merge.", className="alert-error-custom")
    
    if not output_name.endswith(".pdf"):
        output_name += ".pdf"
    
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            # Save files
            input_paths = []
            for f in files:
                file_path = tmp_path / f["name"]
                file_path.write_bytes(base64.b64decode(f["content"]))
                input_paths.append(file_path)
            
            # Merge
            output_path = tmp_path / output_name
            result_path = pdf_tool.merge(input_paths, output_path)
            
            # Read result
            result_bytes = result_path.read_bytes()
            result_b64 = base64.b64encode(result_bytes).decode()
            
            return html.Div([
                html.Div(f"✓ Successfully merged {len(files)} PDFs!", className="alert-success-custom"),
                html.A(
                    "Download Merged PDF",
                    href=f"data:application/pdf;base64,{result_b64}",
                    download=output_name,
                    className="btn-download",
                    style={"marginTop": "1rem", "display": "inline-block"},
                ),
            ])
    except Exception as e:
        return html.Div(f"Error merging PDFs: {str(e)}", className="alert-error-custom")


# Callback for compress action
@callback(
    Output("compress-result", "children"),
    Input("compress-btn", "n_clicks"),
    State("compress-file-store", "data"),
    State("compress-level", "value"),
    State("compress-output-name", "value"),
    prevent_initial_call=True,
)
def compress_pdf(n_clicks, file_data, level, output_name):
    if not n_clicks or not file_data:
        raise PreventUpdate
    
    if not output_name.endswith(".pdf"):
        output_name += ".pdf"
    
    level_map = {
        "LOW": CompressionLevel.LOW,
        "MEDIUM": CompressionLevel.MEDIUM,
        "HIGH": CompressionLevel.HIGH,
        "EXTREME": CompressionLevel.EXTREME,
    }
    compression_level = level_map.get(level, CompressionLevel.MEDIUM)
    
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            # Save file
            input_path = tmp_path / file_data["name"]
            input_path.write_bytes(base64.b64decode(file_data["content"]))
            
            # Compress
            output_path = tmp_path / output_name
            result_path = pdf_tool.compress(input_path, output_path, compression_level)
            
            # Read result
            result_bytes = result_path.read_bytes()
            result_b64 = base64.b64encode(result_bytes).decode()
            
            original_size_kb = file_data["size"] / 1024
            new_size_kb = len(result_bytes) / 1024
            reduction = ((original_size_kb - new_size_kb) / original_size_kb) * 100
            
            return html.Div([
                html.Div("✓ Compression complete!", className="alert-success-custom"),
                create_metrics(original_size_kb, new_size_kb, reduction),
                html.A(
                    "Download Compressed PDF",
                    href=f"data:application/pdf;base64,{result_b64}",
                    download=output_name,
                    className="btn-download",
                    style={"display": "inline-block"},
                ),
            ])
    except Exception as e:
        return html.Div(f"Error compressing PDF: {str(e)}", className="alert-error-custom")


# Callback for merge & compress action
@callback(
    Output("merge-compress-result", "children"),
    Input("merge-compress-btn", "n_clicks"),
    State("merge-compress-files-store", "data"),
    State("merge-compress-level", "value"),
    State("merge-compress-output-name", "value"),
    prevent_initial_call=True,
)
def merge_and_compress_pdfs(n_clicks, files, level, output_name):
    if not n_clicks or not files:
        raise PreventUpdate
    
    if len(files) < 2:
        return html.Div("Please upload at least 2 PDF files to merge.", className="alert-error-custom")
    
    if not output_name.endswith(".pdf"):
        output_name += ".pdf"
    
    level_map = {
        "LOW": CompressionLevel.LOW,
        "MEDIUM": CompressionLevel.MEDIUM,
        "HIGH": CompressionLevel.HIGH,
        "EXTREME": CompressionLevel.EXTREME,
    }
    compression_level = level_map.get(level, CompressionLevel.MEDIUM)
    
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            # Save files
            input_paths = []
            total_size = 0
            for f in files:
                file_path = tmp_path / f["name"]
                content = base64.b64decode(f["content"])
                file_path.write_bytes(content)
                input_paths.append(file_path)
                total_size += len(content)
            
            # Merge
            merged_path = tmp_path / "merged_temp.pdf"
            pdf_tool.merge(input_paths, merged_path)
            
            # Compress
            output_path = tmp_path / output_name
            result_path = pdf_tool.compress(merged_path, output_path, compression_level)
            
            # Read result
            result_bytes = result_path.read_bytes()
            result_b64 = base64.b64encode(result_bytes).decode()
            
            total_size_kb = total_size / 1024
            new_size_kb = len(result_bytes) / 1024
            reduction = ((total_size_kb - new_size_kb) / total_size_kb) * 100
            
            return html.Div([
                html.Div(f"✓ Successfully merged and compressed {len(files)} PDFs!", className="alert-success-custom"),
                create_metrics(total_size_kb, new_size_kb, reduction),
                html.A(
                    "Download Result",
                    href=f"data:application/pdf;base64,{result_b64}",
                    download=output_name,
                    className="btn-download",
                    style={"display": "inline-block"},
                ),
            ])
    except Exception as e:
        return html.Div(f"Error: {str(e)}", className="alert-error-custom")


# Server for deployment
server = app.server

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
