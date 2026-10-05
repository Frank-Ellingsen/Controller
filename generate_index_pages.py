import os
import json

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | UiA Controlling</title>
    <style>
        :root {{
            --uia-navy: #002B49;
            --uia-blue: #005A9C;
            --uia-accent: #E35205;
            --uia-light: #F8FAFC;
            --uia-dark: #1E293B;
            --uia-border: #E2E8F0;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }}
        body {{ background-color: var(--uia-light); color: var(--uia-dark); line-height: 1.5; min-height: 100vh; display: flex; flex-direction: column; }}
        header {{ background-color: var(--uia-navy); color: white; padding: 1.2rem 2rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header-title {{ font-size: 1.25rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }}
        .btn-home {{ background-color: var(--uia-accent); color: white; text-decoration: none; padding: 0.45rem 1rem; border-radius: 6px; font-size: 0.85rem; font-weight: 600; transition: background 0.2s; }}
        .btn-home:hover {{ background-color: #c84400; }}
        .container {{ max-width: 1200px; width: 95%; margin: 2rem auto; flex: 1; }}
        .breadcrumb {{ margin-bottom: 1.5rem; font-size: 0.9rem; color: #64748B; }}
        .breadcrumb a {{ color: var(--uia-blue); text-decoration: none; font-weight: 500; }}
        .breadcrumb a:hover {{ text-decoration: underline; }}
        .summary-bar {{ display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }}
        .summary-card {{ background: white; border: 1px solid var(--uia-border); border-radius: 8px; padding: 1rem 1.5rem; flex: 1; min-width: 180px; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }}
        .summary-card .label {{ font-size: 0.8rem; text-transform: uppercase; color: #64748B; font-weight: 600; letter-spacing: 0.5px; }}
        .summary-card .value {{ font-size: 1.5rem; font-weight: 700; color: var(--uia-navy); margin-top: 0.25rem; }}
        .search-box {{ width: 100%; padding: 0.75rem 1rem; border-radius: 8px; border: 1px solid var(--uia-border); font-size: 0.95rem; margin-bottom: 1.5rem; outline: none; transition: border-color 0.2s; }}
        .search-box:focus {{ border-color: var(--uia-blue); }}
        .section-title {{ font-size: 1.1rem; font-weight: 600; color: var(--uia-navy); margin-bottom: 1rem; border-bottom: 2px solid var(--uia-navy); padding-bottom: 0.3rem; }}
        .grid-folders {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
        .folder-card {{ background: white; border: 1px solid var(--uia-border); border-left: 4px solid var(--uia-blue); border-radius: 8px; padding: 1rem; text-decoration: none; color: var(--uia-dark); transition: transform 0.15s, box-shadow 0.15s; display: flex; align-items: center; justify-content: space-between; }}
        .folder-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08); border-left-color: var(--uia-accent); }}
        .folder-info {{ display: flex; align-items: center; gap: 0.75rem; font-weight: 600; }}
        .file-table-container {{ background: white; border: 1px solid var(--uia-border); border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.02); margin-bottom: 2rem; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; }}
        th {{ background-color: #F1F5F9; color: var(--uia-navy); padding: 0.75rem 1rem; font-weight: 600; border-bottom: 1px solid var(--uia-border); }}
        td {{ padding: 0.75rem 1rem; border-bottom: 1px solid var(--uia-border); vertical-align: middle; }}
        tr:last-child td {{ border-bottom: none; }}
        tr:hover {{ background-color: #F8FAFC; }}
        .file-name {{ font-weight: 500; color: var(--uia-navy); text-decoration: none; word-break: break-word; }}
        .file-name:hover {{ color: var(--uia-blue); text-decoration: underline; }}
        .num-col {{ text-align: right; font-variant-numeric: tabular-nums; color: #64748B; }}
        .btn-download {{ background: var(--uia-blue); color: white; padding: 0.35rem 0.75rem; border-radius: 4px; text-decoration: none; font-size: 0.8rem; font-weight: 600; display: inline-block; }}
        .btn-download:hover {{ background: var(--uia-navy); }}
        footer {{ background: white; border-top: 1px solid var(--uia-border); text-align: center; padding: 1.5rem; font-size: 0.85rem; color: #64748B; margin-top: auto; }}
    </style>
</head>
<body>
    <header>
        <div class="header-title">🏛️ Universitetet i Agder | {title}</div>
        <a href="{home_rel_path}index.html" class="btn-home">🏠 Tilbake til Hovedportalen</a>
    </header>
    
    <div class="container">
        <div class="breadcrumb">{breadcrumb_html}</div>
        
        <div class="summary-bar">
            <div class="summary-card">
                <div class="label">Undermapper</div>
                <div class="value">{folder_count}</div>
            </div>
            <div class="summary-card">
                <div class="label">Dokumenter & Filer</div>
                <div class="value">{file_count}</div>
            </div>
            <div class="summary-card">
                <div class="label">Samlet Størrelse</div>
                <div class="value">{total_size_mb:.2f} MB</div>
            </div>
        </div>

        <input type="text" id="file-search" class="search-box" placeholder="🔍 Søk etter filnavn i denne mappen..." onkeyup="filterFiles()">

        {folders_html}

        {files_html}
    </div>

    <footer>
        Universitetet i Agder — Controlling & Financial Management Portal | Generert for GitHub Pages
    </footer>

    <script>
        function filterFiles() {{
            const query = document.getElementById('file-search').value.toLowerCase();
            const rows = document.querySelectorAll('#file-table-body tr');
            rows.forEach(row => {{
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            }});
        }}
    </script>
</body>
</html>"""

def get_icon(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.xlsx', '.xls', '.csv']:
        return '📊'
    elif ext in ['.docx', '.doc', '.txt', '.md']:
        return '📄'
    elif ext == '.pdf':
        return '📕'
    elif ext in ['.png', '.jpg', '.jpeg', '.svg']:
        return '🖼️'
    elif ext in ['.ps1', '.py', '.sh', '.json']:
        return '⚙️'
    return '📁'

def process_directory(target_dir):
    root_abs = os.path.abspath(target_dir)
    workspace_root = os.path.abspath('.')
    
    for current_root, dirs, files in os.walk(root_abs):
        # Filter out hidden or build folders if any
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        rel_to_workspace = os.path.relpath(current_root, workspace_root)
        parts = rel_to_workspace.split(os.sep)
        
        # Calculate depth to reach root index.html
        depth = len(parts)
        home_rel_path = '../' * depth
        
        # Breadcrumb
        breadcrumb_parts = [f'<a href="{home_rel_path}index.html">Hovedportal</a>']
        accum = []
        for i, p in enumerate(parts):
            accum.append(p)
            step_rel = '../' * (depth - 1 - i)
            breadcrumb_parts.append(f'<a href="{step_rel}index.html">{p}</a>')
        breadcrumb_html = ' / '.join(breadcrumb_parts)
        
        title = parts[-1]
        
        # Subdirectories HTML
        subdirs_list = sorted(dirs)
        folder_count = len(subdirs_list)
        if subdirs_list:
            folders_items = []
            for d in subdirs_list:
                folders_items.append(f'''
                <a href="{d}/index.html" class="folder-card">
                    <div class="folder-info">
                        <span>📁</span>
                        <span>{d}</span>
                    </div>
                    <span style="color: #94A3B8;">→</span>
                </a>''')
            folders_html = f'''
            <div class="section-title">📁 Undermapper ({folder_count})</div>
            <div class="grid-folders">
                {''.join(folders_items)}
            </div>'''
        else:
            folders_html = ''

        # Files HTML
        valid_files = [f for f in sorted(files) if f != 'index.html' and not f.startswith('.')]
        file_count = len(valid_files)
        total_size_bytes = 0
        
        if valid_files:
            table_rows = []
            for f in valid_files:
                f_path = os.path.join(current_root, f)
                size_b = os.path.getsize(f_path)
                total_size_bytes += size_b
                
                size_str = f"{size_b / 1024:.1f} KB" if size_b < 1024*1024 else f"{size_b / (1024*1024):.2f} MB"
                icon = get_icon(f)
                
                table_rows.append(f'''
                <tr>
                    <td style="width: 40px; text-align: center; font-size: 1.1rem;">{icon}</td>
                    <td><a href="{f}" class="file-name" target="_blank">{f}</a></td>
                    <td class="num-col">{size_str}</td>
                    <td style="width: 120px; text-align: right;">
                        <a href="{f}" download class="btn-download">📥 Last ned</a>
                    </td>
                </tr>''')
            
            files_html = f'''
            <div class="section-title">📄 Dokumenter og Datafiler ({file_count})</div>
            <div class="file-table-container">
                <table>
                    <thead>
                        <tr>
                            <th style="width: 40px;"></th>
                            <th>Filnavn</th>
                            <th style="text-align: right;">Størrelse</th>
                            <th style="text-align: right;">Handling</th>
                        </tr>
                    </thead>
                    <tbody id="file-table-body">
                        {''.join(table_rows)}
                    </tbody>
                </table>
            </div>'''
        else:
            files_html = '<div class="section-title">📄 Ingen direkte filer i denne mappen</div>'

        total_size_mb = total_size_bytes / (1024 * 1024)
        
        full_html = HTML_TEMPLATE.format(
            title=title,
            home_rel_path=home_rel_path,
            breadcrumb_html=breadcrumb_html,
            folder_count=folder_count,
            file_count=file_count,
            total_size_mb=total_size_mb,
            folders_html=folders_html,
            files_html=files_html
        )
        
        index_file_path = os.path.join(current_root, 'index.html')
        with open(index_file_path, 'w', encoding='utf-8') as out_f:
            out_f.write(full_html)
        print(f"Generated: {index_file_path}")

print("Processing Controller Mappe...")
process_directory("Controller Mappe")

print("Processing Kunnskapsbase...")
process_directory("Kunnskapsbase")

print("Processing Regelverk...")
process_directory("Regelverk")

print("All index pages generated successfully!")
