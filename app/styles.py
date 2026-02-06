"""Custom CSS styles for the Priva PDF application."""

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


def get_index_string() -> str:
    """Generate the custom HTML template with injected CSS."""
    return '''
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
