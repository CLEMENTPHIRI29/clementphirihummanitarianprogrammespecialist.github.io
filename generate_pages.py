from pathlib import Path

root = Path(r"c:\Users\cleme\OneDrive\Documentos\Jobs\Humanitarian Programme Officer")
src_file = root / "Clement_Phiri_Portfolio_v2 (1).html"
if not src_file.exists():
    raise SystemExit(f"Source file not found: {src_file}")

text = src_file.read_text(encoding='utf-8')

# Extract <head> ... </head>
head_end = text.find('</head>')
if head_end == -1:
    raise SystemExit('Could not locate </head> in source file')
head_html = text[:head_end+7]

# Extract body content
body_start = text.find('<body>')
body_end = text.rfind('</body>')
if body_start == -1 or body_end == -1:
    raise SystemExit('Could not locate <body> or </body>')
body_html = text[body_start+6:body_end]

# Extract nav
nav_start = body_html.find('<!-- ═══ NAV')
nav_end = body_html.find('<!-- ═══ HERO', nav_start)
if nav_start == -1 or nav_end == -1:
    raise SystemExit('Could not locate nav section in body')
nav_html = body_html[nav_start:nav_end]

# Update nav links for local pages
nav_html = nav_html.replace('https://sites.google.com/view/clementphiri-hummanitarian/home', 'home.html')
nav_html = nav_html.replace('https://sites.google.com/view/clementphiri-hummanitarian/about', 'about.html')
nav_html = nav_html.replace('https://sites.google.com/view/clementphiri-hummanitarian/experiences', 'experiences.html')
nav_html = nav_html.replace('https://sites.google.com/view/clementphiri-hummanitarian/competencies', 'competencies.html')
nav_html = nav_html.replace('https://sites.google.com/view/clementphiri-hummanitarian/projects', 'projects.html')
nav_html = nav_html.replace('https://sites.google.com/view/clementphiri-hummanitarian/education', 'education.html')
nav_html = nav_html.replace('https://sites.google.com/view/clementphiri-hummanitarian/contact', 'contact.html')

# Define page sections (start marker, end marker)
sections = {
    'home.html': ('<!-- ═══ HERO', '<!-- ═══ ABOUT'),
    'about.html': ('<!-- ═══ ABOUT', '<!-- ═══ EXPERIENCE'),
    'experiences.html': ('<!-- ═══ EXPERIENCE', '<!-- ═══ PARTNERS'),
    'competencies.html': ('<!-- ═══ COMPETENCIES', '<!-- ═══ PROJECTS'),
    'projects.html': ('<!-- ═══ PROJECTS', '<!-- ═══ EDUCATION'),
    'education.html': ('<!-- ═══ EDUCATION', '<!-- ═══ CONTACT'),
    'contact.html': ('<!-- ═══ CONTACT', '<!-- ═══ FOOTER'),
}

# Extract footer+JS (from footer marker to end of body)
footer_start = body_html.find('<!-- ═══ FOOTER')
if footer_start == -1:
    raise SystemExit('Could not locate footer section')
footer_html = body_html[footer_start:]

for filename, (start_marker, end_marker) in sections.items():
    start_idx = body_html.find(start_marker)
    if start_idx == -1:
        print(f"Skipping {filename}: marker {start_marker} not found")
        continue
    end_idx = body_html.find(end_marker, start_idx)
    if end_idx == -1:
        section_html = body_html[start_idx:]
    else:
        section_html = body_html[start_idx:end_idx]

    page_html = head_html + "\n<body>\n" + nav_html + "\n" + section_html + "\n" + footer_html + "\n</body>\n</html>"
    out_path = root / filename
    out_path.write_text(page_html, encoding='utf-8')
    print('Created', out_path)
