from flask import Flask, request, jsonify, send_file
import os
import tempfile
from main import parse_article_from_url, generate_title, generate_desc, render_article_html, split_markdown_blocks
import markdown
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtGui import QImage
from fpdf import FPDF
from PIL import Image

app = Flask(__name__)

@app.route('/api/parse', methods=['POST'])
def api_parse():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'Missing url'}), 400
    try:
        title, content = parse_article_from_url(url)
        xhs_title = generate_title(title, content)
        xhs_desc = generate_desc(content)
        return jsonify({'title': xhs_title, 'desc': xhs_desc, 'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/split', methods=['POST'])
def api_split():
    data = request.json
    content = data.get('content')
    n = int(data.get('split', 3))
    is_md = data.get('is_md', False)
    if not content:
        return jsonify({'error': 'Missing content'}), 400
    if is_md:
        groups = split_markdown_blocks(content, n)
        md_blocks = ['\n'.join([b['content'] for b in g]) for g in groups]
    else:
        paras = [line.strip() for line in content.split('\n') if line.strip()]
        chunk_size = (len(paras) + n - 1) // n
        md_blocks = ['\n'.join(paras[i*chunk_size:(i+1)*chunk_size]) for i in range(n)]
    return jsonify({'blocks': md_blocks})

@app.route('/api/render', methods=['POST'])
def api_render():
    data = request.json
    title = data.get('title', '')
    desc = data.get('desc', '')
    md = data.get('md', '')
    style = data.get('style', 'card')
    is_md = data.get('is_md', False)
    highlight = data.get('highlight', True)
    highlight_theme = data.get('highlight_theme', 'github')
    if is_md:
        html_content = markdown.markdown(md, extensions=['extra', 'codehilite'])
        html = render_article_html(title, html_content, desc, style, is_html=True, highlight=highlight, highlight_theme=highlight_theme)
    else:
        html = render_article_html(title, md, desc, style, highlight=highlight, highlight_theme=highlight_theme)
    return jsonify({'html': html})

@app.route('/api/export_image', methods=['POST'])
def api_export_image():
    data = request.json
    html = data.get('html')
    if not html:
        return jsonify({'error': 'Missing html'}), 400
    webview = QWebEngineView()
    webview.setHtml(html, QUrl('about:blank'))
    webview.setMinimumWidth(600)
    webview.setMaximumWidth(600)
    webview.setMinimumHeight(800)
    QTimer.singleShot(1000, lambda: None)
    img = webview.grab()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(tmp.name)
    return send_file(tmp.name, mimetype='image/png', as_attachment=True, download_name='xhs_img.png')

@app.route('/api/export_pdf', methods=['POST'])
def api_export_pdf():
    data = request.json
    html_list = data.get('html_list')
    if not html_list or not isinstance(html_list, list):
        return jsonify({'error': 'Missing html_list'}), 400
    img_paths = []
    for html in html_list:
        webview = QWebEngineView()
        webview.setHtml(html, QUrl('about:blank'))
        webview.setMinimumWidth(600)
        webview.setMaximumWidth(600)
        webview.setMinimumHeight(800)
        QTimer.singleShot(1000, lambda: None)
        img = webview.grab()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        img.save(tmp.name)
        img_paths.append(tmp.name)
    pdf = FPDF(unit='pt', format=[600, 800])
    for img_path in img_paths:
        pdf.add_page()
        pdf.image(img_path, 0, 0, 600, 800)
    pdf_path = tempfile.mktemp(suffix='.pdf')
    pdf.output(pdf_path, 'F')
    for img_path in img_paths:
        try:
            os.remove(img_path)
        except Exception:
            pass
    return send_file(pdf_path, mimetype='application/pdf', as_attachment=True, download_name='xhs_export.pdf')

@app.route('/api/export_long_image', methods=['POST'])
def api_export_long_image():
    data = request.json
    html_list = data.get('html_list')
    if not html_list or not isinstance(html_list, list):
        return jsonify({'error': 'Missing html_list'}), 400
    images = []
    for html in html_list:
        webview = QWebEngineView()
        webview.setHtml(html, QUrl('about:blank'))
        webview.setMinimumWidth(600)
        webview.setMaximumWidth(600)
        webview.setMinimumHeight(800)
        QTimer.singleShot(1000, lambda: None)
        img = webview.grab()
        images.append(img)
    if images:
        total_height = sum(img.height() for img in images)
        long_img = Image.new('RGB', (images[0].width(), total_height), (255,255,255))
        y = 0
        for img in images:
            buffer = img.toImage().bits().asstring(img.width()*img.height()*4)
            pil_img = Image.frombytes('RGBA', (img.width(), img.height()), buffer)
            pil_img = pil_img.convert('RGB')
            long_img.paste(pil_img, (0, y))
            y += img.height()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        long_img.save(tmp.name)
        return send_file(tmp.name, mimetype='image/png', as_attachment=True, download_name='xhs_long.png')
    return jsonify({'error': 'No images'}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True) 