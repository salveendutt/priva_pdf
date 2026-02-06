"""Reusable UI components for the Priva PDF application."""

from dash import dcc, html
import dash_bootstrap_components as dbc

from .config import COMPRESSION_OPTIONS


def create_upload_component(component_id: str, multiple: bool = False) -> dcc.Upload:
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


def create_file_list(files: list, show_reorder: bool = False, id_prefix: str = "") -> html.Div:
    """Create a styled file list with optional reorder buttons."""
    if not files:
        return html.Div()
    
    items = []
    for idx, f in enumerate(files):
        file_row = [
            html.Span(f"{idx + 1}. ", style={"color": "#78716c", "marginRight": "0.5rem"}),
            html.Span(f["name"], className="file-name"),
            html.Span(f" ({f['size'] / 1024:.1f} KB)", className="file-size"),
        ]
        
        if show_reorder:
            reorder_buttons = html.Span([
                html.Button("↑", id={"type": f"{id_prefix}-move-up", "index": idx}, 
                           className="reorder-btn", disabled=(idx == 0)),
                html.Button("↓", id={"type": f"{id_prefix}-move-down", "index": idx}, 
                           className="reorder-btn", disabled=(idx == len(files) - 1)),
                html.Button("✕", id={"type": f"{id_prefix}-remove", "index": idx}, 
                           className="reorder-btn", style={"color": "#ef4444"}),
            ], style={"marginLeft": "auto"})
            file_row.append(reorder_buttons)
        
        items.append(html.Div(file_row, className="file-item"))
    
    return html.Div([
        html.Div([
            html.Strong(f"{len(files)} file(s) ready"),
            html.Span(" — drag to reorder or use arrows" if show_reorder else "", 
                     style={"color": "#78716c", "fontSize": "0.85rem"}),
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


def create_metrics(original: float, compressed: float, reduction: float) -> dbc.Row:
    """Create metrics display for compression results."""
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


def create_success_alert(message: str) -> html.Div:
    """Create a success alert."""
    return html.Div(message, className="alert-success-custom")


def create_error_alert(message: str) -> html.Div:
    """Create an error alert."""
    return html.Div(message, className="alert-error-custom")


def create_download_button(href: str, filename: str, text: str = "Download") -> html.A:
    """Create a download button."""
    return html.A(
        text,
        href=href,
        download=filename,
        className="btn-download",
        style={"marginTop": "1rem", "display": "inline-block"},
    )
