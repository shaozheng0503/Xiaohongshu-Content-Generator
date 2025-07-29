import sys
import os
import tempfile
import markdown
import re
import json
import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QFileDialog, QMessageBox, QProgressBar, QComboBox, QSpinBox, QScrollArea, QFrame, QCheckBox, QDialog, QDialogButtonBox,
    QMenu, QAction, QToolTip, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPainter, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QTimer, QUrl, QMimeData, QPoint
from PyQt5.QtGui import QDrag
from parser import parse_article_from_url
from nlp_gen import generate_title, generate_desc
from html_render import render_article_html
from screenshot import save_webview_as_image
from PIL import Image
from fpdf import FPDF

STYLE_MAP = {
    '极简黑白': 'minimal',
    '杂志卡片': 'card',
    '梦幻渐变': 'gradient',
    '清新自然': 'fresh',
    '暗黑科技': 'darktech',
    '卡哇伊风格': 'kawaii',
    '简约清新风': 'simple',
    'emoji风': 'emoji',
    '马卡龙风': 'macaron',
    '贴纸风': 'sticker',
    '复古学习感': 'retro',
    '苹果备忘录': 'apple',
    '奶油胶风': 'cream',
    '纯白极简': 'clean',
}
HIGHLIGHT_THEMES = {
    'GitHub': 'github',
    'Monokai': 'monokai',
    'Dracula': 'dracula',
}

i18n = {
    'zh': {
        'title': '小红书内容生成工具',
        'desc': '一键将博客文章转为小红书风格图片和文案，支持多模板、多主题、智能分割、内容编辑与批量导出。',
        'parse_btn': '解析链接',
        'upload_btn': '上传本地文件',
        'split_label': '分割张数',
        'smart_split': '智能推荐张数',
        'style_label': '排版样式',
        'theme_label': '主题',
        'highlight': '代码高亮',
        'hl_theme': '高亮主题',
        'card_style': '卡片模板',
        'beautify': '一键美化',
        'preview_mode': '预览模式',
        'title_label': '自动生成标题',
        'desc_label': '自动生成描述',
        'screenshot_btn': '批量导出图片',
        'save_desc_btn': '保存文案',
        'history_btn': '历史记录',
        'batch_btn': '批量处理',
        'progress': '进度',
        'delete': '删除',
        'export': '批量导出文案',
        'export_img': '批量导出图片',
        'export_pdf': '批量导出PDF',
        'export_long': '批量导出长图',
        'beautify_batch': '批量一键美化',
        'lang': '语言',
    },
    'en': {
        'title': 'Xiaohongshu Content Generator',
        'desc': 'One-click to convert blog articles into Xiaohongshu-style images and copywriting. Supports multi-template, multi-theme, smart splitting, content editing, and batch export.',
        'parse_btn': 'Parse Link',
        'upload_btn': 'Upload File',
        'split_label': 'Split Count',
        'smart_split': 'Smart Split',
        'style_label': 'Layout Style',
        'theme_label': 'Theme',
        'highlight': 'Code Highlight',
        'hl_theme': 'Highlight Theme',
        'card_style': 'Card Template',
        'beautify': 'Beautify',
        'preview_mode': 'Preview Mode',
        'title_label': 'Auto Title',
        'desc_label': 'Auto Description',
        'screenshot_btn': 'Batch Export Images',
        'save_desc_btn': 'Save Copy',
        'history_btn': 'History',
        'batch_btn': 'Batch',
        'progress': 'Progress',
        'delete': 'Delete',
        'export': 'Batch Export Text',
        'export_img': 'Batch Export Images',
        'export_pdf': 'Batch Export PDF',
        'export_long': 'Batch Export Long Image',
        'beautify_batch': 'Batch Beautify',
        'lang': 'Language',
    }
}

def split_markdown_blocks(content, n):
    """优化的markdown内容分割函数，确保内容完整性"""
    blocks = []
    lines = content.split('\n')
    buf = []
    in_code = False
    code_lang = ''
    for line in lines:
        if line.strip().startswith('```'):
            if not in_code:
                if buf:
                    blocks.append({'type': 'text', 'content': '\n'.join(buf)})
                    buf = []
                in_code = True
                code_lang = line.strip()[3:].strip()
                buf = [line]
            else:
                buf.append(line)
                blocks.append({'type': 'code', 'content': '\n'.join(buf), 'lang': code_lang})
                buf = []
                in_code = False
                code_lang = ''
        else:
            buf.append(line)
    if buf:
        blocks.append({'type': 'code' if in_code else 'text', 'content': '\n'.join(buf), 'lang': code_lang})
    
    # 优化分割策略：确保内容不丢失
    if not blocks:
        return [[] for _ in range(n)]
    
    total_len = sum(len(b['content']) for b in blocks)
    if total_len == 0:
        return [[] for _ in range(n)]
        
    # 计算每段的目标长度，留有余量
    avg_len = max(total_len // n, 100)  # 确保最小长度
    
    result = []
    cur = []
    cur_len = 0
    
    for b in blocks:
        block_len = len(b['content'])
        
        # 如果当前块太大，且还有剩余分割数，则分割当前内容
        if cur and (cur_len + block_len > avg_len * 1.5) and len(result) < n-1:
            result.append(cur)
            cur = []
            cur_len = 0
        
        cur.append(b)
        cur_len += block_len
    
    # 处理剩余内容
    if cur:
        result.append(cur)
    
    # 确保返回n个分组，即使有些为空
    while len(result) < n:
        result.append([])
    
    # 如果分组数超过n，合并最后几组
    if len(result) > n:
        last_group = []
        for group in result[n-1:]:
            last_group.extend(group)
        result = result[:n-1] + [last_group]
    
    return result

def smart_split_text_content(content, target_count):
    """智能文本内容分割，按段落和长度平衡分配"""
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    if not lines:
        return [''] * target_count
    
    total_chars = sum(len(line) for line in lines)
    target_chars_per_group = max(total_chars // target_count, 50)  # 最少50字符
    
    groups = []
    current_group = []
    current_chars = 0
    
    for line in lines:
        line_chars = len(line)
        
        # 如果当前组已经足够长，且还有剩余分组数
        if current_group and (current_chars + line_chars > target_chars_per_group * 1.3) and len(groups) < target_count - 1:
            groups.append('\n'.join(current_group))
            current_group = []
            current_chars = 0
        
        current_group.append(line)
        current_chars += line_chars
    
    # 处理最后一组
    if current_group:
        groups.append('\n'.join(current_group))
    
    # 确保返回目标数量的分组
    while len(groups) < target_count:
        groups.append('')
    
    # 如果分组过多，合并末尾的组
    if len(groups) > target_count:
        last_content = '\n'.join(groups[target_count-1:])
        groups = groups[:target_count-1] + [last_content]
    
    return groups

THEME_QSS = {
    '极简白': '''
        QWidget { background: #f8f4ed; font-family: "微软雅黑", Arial, Roboto, sans-serif; }
        QLabel { color: #222; font-size: 18px; font-weight: 600; }
        QLineEdit, QTextEdit { border: 2px solid #e1cad2; border-radius: 8px; padding: 12px; background: #fff; font-size: 16px; color: #222; font-weight: 500; }
        QPushButton { background: #ff9e80; color: #fff; border-radius: 8px; padding: 12px 20px; font-size: 16px; margin: 0 8px; font-weight: 700; }
        QPushButton:hover { background: #ff7043; }
        QComboBox, QSpinBox { border: 2px solid #e1cad2; border-radius: 8px; padding: 8px; background: #fff; font-size: 16px; color: #222; font-weight: 500; }
        QProgressBar { border: 2px solid #f2e5e8; border-radius: 4px; text-align: center; background: #f2e5e8; font-size: 14px; height: 8px; }
        QProgressBar::chunk { background: #ff9e80; border-radius: 4px; }
        QFrame.card { background: #fff; border-radius: 12px; margin: 15px 10px; padding: 20px 15px 15px 15px; border: 1px solid #e1cad2; }
        QFrame.line { border-top: 2px solid #e8e0dc; margin: 15px 0; background: #fff; }
    ''',
    '暗色': '''
        QWidget { background: #23272e; font-family: "微软雅黑", Arial, Roboto, sans-serif; }
        QLabel { color: #f8f8f2; font-size: 16px; font-weight: 500; }
        QLineEdit, QTextEdit { border: 2px solid #44475a; border-radius: 8px; padding: 12px; background: #282a36; color: #f8f8f2; font-size: 16px; font-weight: 500; }
        QPushButton { background: #44475a; color: #f8f8f2; border-radius: 8px; padding: 12px 20px; font-size: 16px; margin: 0 8px; font-weight: 700; }
        QPushButton:hover { background: #6272a4; }
        QComboBox, QSpinBox { border: 2px solid #44475a; border-radius: 8px; padding: 8px; background: #282a36; color: #f8f8f2; font-size: 16px; font-weight: 500; }
        QProgressBar { border: 2px solid #44475a; border-radius: 4px; text-align: center; background: #282a36; font-size: 14px; }
        QProgressBar::chunk { background: #6272a4; }
        QFrame.card { background: #282a36; border-radius: 12px; margin: 15px 10px; padding: 20px 15px 15px 15px; border: 2px solid #44475a; }
        QFrame.line { border-top: 2px solid #44475a; margin: 15px 0; }
    ''',
    '蓝色': '''
        QWidget { background: #e3f2fd; font-family: "微软雅黑", Arial, Roboto, sans-serif; }
        QLabel { color: #1976d2; font-size: 16px; }
        QLineEdit, QTextEdit { border: 2px solid #90caf9; border-radius: 8px; padding: 8px; background: #fff; font-size: 16px; }
        QPushButton { background: #1976d2; color: #fff; border-radius: 8px; padding: 10px 24px; font-size: 16px; margin: 0 8px; font-weight: 600; }
        QPushButton:hover { background: #1565c0; }
        QComboBox, QSpinBox { border: 2px solid #90caf9; border-radius: 8px; padding: 6px; background: #fff; font-size: 16px; }
        QProgressBar { border: 2px solid #90caf9; border-radius: 4px; text-align: center; background: #e3f2fd; }
        QProgressBar::chunk { background: #1976d2; }
        QFrame.card { background: #fff; border-radius: 12px; margin: 15px 10px; padding: 20px 15px 15px 15px; border: 1px solid #90caf9; }
        QFrame.line { border-top: 2px solid #90caf9; margin: 10px 0; }
    ''',
    '绿色': '''
        QWidget { background: #e8f5e9; font-family: "微软雅黑", Arial, Roboto, sans-serif; }
        QLabel { color: #388e3c; font-size: 16px; }
        QLineEdit, QTextEdit { border: 2px solid #a5d6a7; border-radius: 8px; padding: 8px; background: #fff; font-size: 16px; }
        QPushButton { background: #388e3c; color: #fff; border-radius: 8px; padding: 10px 24px; font-size: 16px; margin: 0 8px; font-weight: 600; }
        QPushButton:hover { background: #2e7d32; }
        QComboBox, QSpinBox { border: 2px solid #a5d6a7; border-radius: 8px; padding: 6px; background: #fff; font-size: 16px; }
        QProgressBar { border: 2px solid #a5d6a7; border-radius: 4px; text-align: center; background: #e8f5e9; }
        QProgressBar::chunk { background: #388e3c; }
        QFrame.card { background: #fff; border-radius: 12px; margin: 15px 10px; padding: 20px 15px 15px 15px; border: 1px solid #a5d6a7; }
        QFrame.line { border-top: 2px solid #a5d6a7; margin: 10px 0; }
    ''',
    '橙色': '''
        QWidget { background: #fff3e0; font-family: "微软雅黑", Arial, Roboto, sans-serif; }
        QLabel { color: #f57c00; font-size: 16px; }
        QLineEdit, QTextEdit { border: 2px solid #ffcc80; border-radius: 8px; padding: 8px; background: #fff; font-size: 16px; }
        QPushButton { background: #f57c00; color: #fff; border-radius: 8px; padding: 10px 24px; font-size: 16px; margin: 0 8px; font-weight: 600; }
        QPushButton:hover { background: #ef6c00; }
        QComboBox, QSpinBox { border: 2px solid #ffcc80; border-radius: 8px; padding: 6px; background: #fff; font-size: 16px; }
        QProgressBar { border: 2px solid #ffcc80; border-radius: 4px; text-align: center; background: #fff3e0; }
        QProgressBar::chunk { background: #f57c00; }
        QFrame.card { background: #fff; border-radius: 12px; margin: 15px 10px; padding: 20px 15px 15px 15px; border: 1px solid #ffcc80; }
        QFrame.line { border-top: 2px solid #ffcc80; margin: 10px 0; }
    ''',
    '粉色': '''
        QWidget { background: #fff0fa; font-family: "微软雅黑", Arial, Roboto, sans-serif; }
        QLabel { color: #e573b4; font-size: 16px; }
        QLineEdit, QTextEdit { border: 2px solid #ffb6d5; border-radius: 8px; padding: 8px; background: #fff; font-size: 16px; }
        QPushButton { background: #ffb6d5; color: #fff; border-radius: 8px; padding: 10px 24px; font-size: 16px; margin: 0 8px; font-weight: 600; }
        QPushButton:hover { background: #e573b4; }
        QComboBox, QSpinBox { border: 2px solid #ffb6d5; border-radius: 8px; padding: 6px; background: #fff; font-size: 16px; }
        QProgressBar { border: 2px solid #ffb6d5; border-radius: 4px; text-align: center; background: #fff6fb; }
        QProgressBar::chunk { background: #e573b4; }
        QFrame.card { background: #fff; border-radius: 12px; margin: 15px 10px; padding: 20px 15px 15px 15px; border: 1px solid #ffb6d5; }
        QFrame.line { border-top: 2px solid #ffb6d5; margin: 10px 0; }
    ''',
    '暗黑粉': '''
        QWidget { background: #2d1e2f; font-family: "微软雅黑", Arial, Roboto, sans-serif; }
        QLabel { color: #ffb6d5; font-size: 16px; }
        QLineEdit, QTextEdit { border: 2px solid #ffb6d5; border-radius: 8px; padding: 8px; background: #3a2a3d; color: #fff; font-size: 16px; }
        QPushButton { background: #ffb6d5; color: #fff; border-radius: 8px; padding: 10px 24px; font-size: 16px; margin: 0 8px; font-weight: 600; }
        QPushButton:hover { background: #e573b4; }
        QComboBox, QSpinBox { border: 2px solid #ffb6d5; border-radius: 8px; padding: 6px; background: #3a2a3d; color: #fff; font-size: 16px; }
        QProgressBar { border: 2px solid #ffb6d5; border-radius: 4px; text-align: center; background: #3a2a3d; }
        QProgressBar::chunk { background: #e573b4; }
        QFrame.card { background: #3a2a3d; border-radius: 12px; margin: 15px 10px; padding: 20px 15px 15px 15px; border: 1px solid #ffb6d5; }
        QFrame.line { border-top: 2px solid #ffb6d5; margin: 10px 0; }
    ''',
    'retro': '''
        QFrame.card { background: #fdf6e3; border-radius: 24px; border: 2px dashed #b58900; padding: 32px 24px 20px 24px; }
        QLabel, QTextEdit { color: #b58900; font-family: 'Fira Mono', '微软雅黑', monospace; font-size: 1.18em; }
    ''',
    'apple': '''
        QFrame.card { background: #fffbe7; border-radius: 24px; border: 2px solid #e1e1e1; padding: 32px 24px 20px 24px; }
        QLabel, QTextEdit { color: #222; font-family: 'SF Pro Display', '微软雅黑', Arial, sans-serif; font-size: 1.18em; }
    ''',
    'cream': '''
        QFrame.card { background: #fff0e6; border-radius: 28px; border: 2px solid #ffd6b3; padding: 28px 20px 14px 20px; }
        QLabel, QTextEdit { color: #ff8c42; font-family: 'Comic Sans MS', '微软雅黑', Arial, sans-serif; font-size: 1.16em; }
    ''',
    'clean': '''
        QFrame.card { background: #ffffff; border-radius: 8px; border: 1px solid #e0e0e0; padding: 24px 20px 16px 20px; }
        QLabel, QTextEdit { color: #333; font-family: '微软雅黑', Arial, sans-serif; font-size: 1.12em; }
    ''',
}

CARD_QSS = {
    'minimal': '''
        QFrame.card { background: #fff; border-radius: 8px; border: 1px solid #e1cad2; padding: 20px 16px 12px 16px; }
        QLabel, QTextEdit { color: #222; font-family: '微软雅黑', Arial, sans-serif; font-size: 16px; font-weight: 600; }
    ''',
    'card': '''
        QFrame.card { background: #fffdf8; border-radius: 12px; border: 1px solid #ffbdbd; padding: 24px 18px 16px 18px; }
        QLabel, QTextEdit { color: #e60023; font-family: '微软雅黑', Arial, sans-serif; font-size: 17px; font-weight: bold; }
    ''',
    'simple': '''
        QFrame.card { background: #fff; border-radius: 8px; border: 1px solid #e0e0e0; padding: 16px 12px 10px 12px; }
        QLabel, QTextEdit { color: #1976d2; font-family: '微软雅黑', Arial, sans-serif; font-size: 15px; }
    ''',
    'clean': '''
        QFrame.card { background: #ffffff; border-radius: 6px; border: 1px solid #e0e0e0; padding: 18px 14px 12px 14px; }
        QLabel, QTextEdit { color: #333; font-family: '微软雅黑', Arial, sans-serif; font-size: 15px; }
    ''',
}

def add_card_shadow(widget, color="#e3eafc", blur=32, x_offset=0, y_offset=8):
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(blur)
    effect.setColor(QColor(color))
    effect.setOffset(x_offset, y_offset)
    widget.setGraphicsEffect(effect)

class EditDialog(QDialog):
    def __init__(self, orig_md, parent=None):
        super().__init__(parent)
        self.setWindowTitle('编辑')
        self.setMinimumSize(600, 400)
        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(orig_md)
        layout.addWidget(self.text_edit)
        btns = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        # 简化按钮样式
        for btn in btns.buttons():
            btn.setStyleSheet('QPushButton { background: #1976d2; color: #fff; border-radius: 8px; padding: 8px 20px; font-size: 14px; margin: 0 8px; font-weight: 500; } QPushButton:hover { background: #1565c0; }')
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)
        self.setLayout(layout)
    def get_md(self):
        return self.text_edit.toPlainText()

class ThumbButton(QPushButton):
    def __init__(self, idx, main_window, parent=None):
        super().__init__("", parent)
        self.idx = idx
        self.main_window = main_window
        self.setFixedSize(44, 44)
        self.setAcceptDrops(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet('''
            QPushButton {
                border-radius: 8px;
                border: 2px solid #e0e0e0;
                background: #fff;
                font-size: 16px;
                font-weight: bold;
                color: #FF2D55;
            }
            QPushButton:hover {
                border: 2px solid #FF2D55;
                background: #fff0fa;
            }
        ''')
        self.label = QLabel(str(idx+1), self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 20, 44, 24)
        self.img_label = QLabel(self)
        self.img_label.setGeometry(4, 4, 36, 24)
        self.img_label.setScaledContents(True)
        self.img_label.hide()
        self.thumbnail = None
        self.full_img = None
    
    def setPixmap(self, pixmap):
        self.thumbnail = pixmap
        self.img_label.setPixmap(pixmap)
        self.img_label.show()
    
    def setFullPixmap(self, pixmap):
        self.full_img = pixmap
    
    def enterEvent(self, event):
        super().enterEvent(event)
        # 简化悬停效果，移除复杂的预览
        self.setStyleSheet('border-radius:8px; border:2px solid #FF2D55; background:#fff0fa; font-size:16px; font-weight:bold; color:#FF2D55;')
    
    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.setStyleSheet('border-radius:8px; border:2px solid #e0e0e0; background:#fff; font-size:16px; font-weight:bold; color:#FF2D55;')
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(str(self.idx))
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)
        elif event.button() == Qt.RightButton:
            menu = QMenu(self)
            act_del = QAction('删除', self)
            act_del.triggered.connect(lambda: self.main_window.delete_thumb(self.idx))
            act_copy = QAction('复制', self)
            act_copy.triggered.connect(lambda: self.main_window.copy_thumb_content(self.idx))
            menu.addAction(act_del)
            menu.addAction(act_copy)
            menu.exec_(self.mapToGlobal(event.pos()))
        super().mousePressEvent(event)
    
    def dragEnterEvent(self, event):
        event.accept()
        self.setStyleSheet('border-radius:8px; border:2px solid #FF2D55; background:#fff0fa; font-size:16px; font-weight:bold; color:#FF2D55;')
    
    def dragLeaveEvent(self, event):
        self.setStyleSheet('border-radius:8px; border:2px solid #e0e0e0; background:#fff; font-size:16px; font-weight:bold; color:#FF2D55;')
    
    def dropEvent(self, event):
        src_idx = int(event.mimeData().text())
        dst_idx = self.idx
        self.main_window.handle_thumb_drag(src_idx, dst_idx)
        self.setStyleSheet('border-radius:8px; border:2px solid #FF2D55; background:#fff; font-size:16px; font-weight:bold; color:#FF2D55;')

class XHSWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = 'zh'
        self.setWindowTitle('博客转小红书截图生成工具')
        self.setMinimumSize(1100, 900)
        self.setWindowIcon(QIcon())
        self.preview_mode = 'horizontal'
        self.badge_text = '原创'  # 新增角标内容
        self.init_ui()
        self.last_content = ''
        self.last_title = ''
        self.last_desc = ''
        self.last_is_md = False
        self.preview_webviews = []
        self.preview_md_blocks = []
        self.highlight = True
        self.highlight_theme = 'github'
        self.selected_thumb_idx = 0
        self.batch_tasks = []

    def init_ui(self):
        t = i18n[self.lang]
        # 1. 主题QSS美化
        theme = getattr(self, 'theme_combo', None)
        theme_name = theme.currentText() if theme else '极简白'
        self.setStyleSheet(THEME_QSS.get(theme_name, THEME_QSS['极简白']))
        layout = QVBoxLayout()
        layout.setContentsMargins(48, 36, 48, 36)
        layout.setSpacing(22)
        # 顶部LOGO+产品名+描述
        logo_layout = QVBoxLayout()
        logo_row = QHBoxLayout()
        logo_label = QLabel()
        logo_label.setObjectName('LogoLabel')
        # 支持自定义LOGO图片（如有logo.png或1.jpg）
        try:
            logo_pix = QPixmap('xhs-tools/1.jpg')
            if not logo_pix.isNull():
                logo_label.setPixmap(logo_pix.scaled(40, 40))
            else:
                logo_pix2 = QPixmap('logo.png')
                if not logo_pix2.isNull():
                    logo_label.setPixmap(logo_pix2.scaled(40, 40))
                else:
                    logo_label.setText('🪐')
        except Exception:
            logo_label.setText('🪐')
        logo_label.setStyleSheet('font-size: 2.5em; margin-bottom: 0.7em; background: rgba(255,255,255,0.92); border-radius: 10px; padding: 4px 12px; box-shadow: 0 2px 8px rgba(230,0,35,0.13);')
        logo_label.setAlignment(Qt.AlignLeft)
        # 设置应用窗口图标
        self.setWindowIcon(QIcon('xhs-tools/1.jpg'))
        logo_row.addWidget(logo_label)
        title = QLabel(t['title'])
        title.setFont(QFont('微软雅黑', 26, QFont.Bold))
        title.setStyleSheet('color:#FF2D55; letter-spacing:2px; font-size:2.2em; font-weight:800;')
        title.setAlignment(Qt.AlignCenter)
        logo_row.addWidget(title, stretch=1)
        logo_row.addStretch(1)
        logo_layout.addLayout(logo_row)
        desc = QLabel(t['desc'])
        desc.setStyleSheet('font-size:1.22em;color:#222;text-align:center; margin-bottom:2em; font-weight:500;')
        desc.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(desc)
        # 右上角语言切换
        lang_row = QHBoxLayout()
        lang_row.addStretch(1)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['中文', 'English'])
        self.lang_combo.setCurrentIndex(0 if self.lang=='zh' else 1)
        self.lang_combo.currentIndexChanged.connect(self.on_lang_change)
        lang_row.addWidget(QLabel(t['lang']))
        lang_row.addWidget(self.lang_combo)
        logo_layout.addLayout(lang_row)
        layout.addLayout(logo_layout)
        # 2. 输入区卡片化
        input_card = QFrame()
        input_card.setObjectName('input_card')
        input_card.setStyleSheet('QFrame#input_card { background: #fff; border-radius: 12px; border: 1px solid #e1cad2; padding: 18px 18px 8px 18px; }')
        input_row = QHBoxLayout()
        input_row.setSpacing(12)
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText('请输入博客文章链接...')
        self.link_input.setMinimumWidth(320)
        self.parse_btn = QPushButton(t['parse_btn'])
        self.parse_btn.clicked.connect(self.handle_parse_link)
        self.upload_btn = QPushButton(t['upload_btn'])
        self.upload_btn.clicked.connect(self.handle_upload_file)
        self.style_label = QLabel(t['style_label'])
        self.style_combo = QComboBox()
        self.style_combo.addItems(list(STYLE_MAP.keys()))
        self.style_combo.currentIndexChanged.connect(self.refresh_previews)
        self.theme_label = QLabel(t['theme_label'])
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(THEME_QSS.keys()))
        self.theme_combo.currentIndexChanged.connect(self.on_theme_change)
        self.hl_checkbox = QCheckBox(t['highlight'])
        self.hl_checkbox.setChecked(True)
        self.hl_checkbox.stateChanged.connect(self.on_highlight_toggle)
        self.hl_theme_label = QLabel(t['hl_theme'])
        self.hl_theme_combo = QComboBox()
        self.hl_theme_combo.addItems(list(HIGHLIGHT_THEMES.keys()))
        self.hl_theme_combo.currentIndexChanged.connect(self.on_highlight_theme_change)
        self.badge_label = QLabel('角标内容:')
        self.badge_input = QLineEdit()
        self.badge_input.setText(self.badge_text)
        self.badge_input.setFixedWidth(100)
        self.badge_input.setStyleSheet('font-size:1.15em; color:#111; font-weight:500;')
        self.badge_input.textChanged.connect(self.on_badge_text_change)
        input_row.addWidget(self.link_input)
        input_row.addWidget(self.parse_btn)
        input_row.addWidget(self.upload_btn)
        self.split_label = QLabel(t['split_label'])
        self.split_spin = QSpinBox()
        self.split_spin.setRange(1, 18)
        self.split_spin.setValue(1)
        self.split_spin.valueChanged.connect(self.refresh_previews)
        self.smart_split_btn = QPushButton(t['smart_split'])
        self.smart_split_btn.setToolTip('根据内容结构智能推荐分割图片数量')
        self.smart_split_btn.clicked.connect(self.handle_smart_split)
        input_row.addWidget(self.split_label)
        input_row.addWidget(self.split_spin)
        input_row.addWidget(self.smart_split_btn)
        input_row.addWidget(self.style_label)
        input_row.addWidget(self.style_combo)
        input_row.addWidget(self.theme_label)
        input_row.addWidget(self.theme_combo)
        input_row.addWidget(self.hl_checkbox)
        input_row.addWidget(self.hl_theme_label)
        input_row.addWidget(self.hl_theme_combo)
        input_row.addWidget(self.badge_label)
        input_row.addWidget(self.badge_input)
        self.card_style_label = QLabel(t['card_style'])
        self.card_style_combo = QComboBox()
        style_icons = {
            '极简黑白': emoji_icon('⬛'),
            '杂志卡片': emoji_icon('📰'),
            '梦幻渐变': emoji_icon('🌈'),
            '清新自然': emoji_icon('🌿'),
            '暗黑科技': emoji_icon('🖤'),
            '卡哇伊风格': emoji_icon('🎀'),
            '简约清新风': emoji_icon('💧'),
            'emoji风': emoji_icon('😃'),
            '马卡龙风': emoji_icon('��'),
            '贴纸风': emoji_icon('📎'),
            '复古学习感': emoji_icon('📚'),
            '苹果备忘录': emoji_icon('🍏'),
            '奶油胶风': emoji_icon('🧁'),
            '纯白极简': emoji_icon('📄'),
        }
        self.card_style_combo.clear()
        for style in STYLE_MAP.keys():
            icon = style_icons.get(style, QIcon())
            self.card_style_combo.addItem(icon, style)
        self.card_style_combo.currentIndexChanged.connect(self.on_card_style_change)
        # 主题预览区
        self.theme_preview = QLabel()
        self.theme_preview.setFixedSize(120, 80)
        self.theme_preview.setStyleSheet('border:1.5px solid #e0e0e0; border-radius:16px; background:#fff;')
        self.update_theme_preview()
        self.card_style_combo.currentIndexChanged.connect(self.update_theme_preview)
        input_row.addWidget(self.card_style_label)
        input_row.addWidget(self.card_style_combo)
        input_row.addWidget(self.theme_preview)
        self.beautify_btn = QPushButton(t['beautify'])
        self.beautify_btn.setToolTip('自动选择推荐模板和美化参数')
        self.beautify_btn.clicked.connect(self.handle_beautify)
        input_row.addWidget(self.beautify_btn)
        input_card.setLayout(input_row)
        layout.addWidget(input_card)
        # 进度条
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setFixedHeight(18)
        layout.addWidget(self.progress)
        # 标题与描述
        td_row = QHBoxLayout()
        td_row.setSpacing(16)
        self.title_label = QLabel(t['title_label'])
        self.title_edit = QLineEdit()
        self.desc_label = QLabel(t['desc_label'])
        self.desc_edit = QTextEdit()
        self.desc_edit.setFixedHeight(48)
        td_row.addWidget(self.title_label)
        td_row.addWidget(self.title_edit, 2)
        td_row.addWidget(self.desc_label)
        td_row.addWidget(self.desc_edit, 3)
        layout.addLayout(td_row)
        # 预览模式切换
        mode_layout = QHBoxLayout()
        self.mode_label = QLabel(t['preview_mode'])
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['横向滑动', '竖向滑动'])
        self.mode_combo.currentIndexChanged.connect(self.on_mode_change)
        mode_layout.addWidget(self.mode_label)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch(1)
        layout.addLayout(mode_layout)
        # 3. 预览区卡片化
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.preview_frame = QFrame()
        self.preview_layout = QHBoxLayout()
        self.preview_frame.setLayout(self.preview_layout)
        self.scroll_area.setWidget(self.preview_frame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.scroll_area, stretch=1)
        # 缩略图导航条
        self.thumb_bar = QHBoxLayout()
        self.thumb_bar_widget = QWidget()
        self.thumb_bar_widget.setLayout(self.thumb_bar)
        self.thumb_scroll = QScrollArea()
        self.thumb_scroll.setWidgetResizable(True)
        self.thumb_scroll.setFixedHeight(70)
        self.thumb_scroll.setWidget(self.thumb_bar_widget)
        self.thumb_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.thumb_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.thumb_scroll)
        # 4. 底部操作按钮美化
        btn_row = QHBoxLayout()
        btn_row.setSpacing(32)
        self.screenshot_btn = QPushButton(t['screenshot_btn'])
        self.screenshot_btn.setFixedHeight(44)
        self.screenshot_btn.setMinimumWidth(120)
        self.screenshot_btn.clicked.connect(self.handle_screenshot)
        self.save_desc_btn = QPushButton(t['save_desc_btn'])
        self.save_desc_btn.setFixedHeight(44)
        self.save_desc_btn.setMinimumWidth(120)
        self.save_desc_btn.clicked.connect(self.handle_save_desc)
        self.history_btn = QPushButton(t['history_btn'])
        self.history_btn.setFixedHeight(44)
        self.history_btn.setMinimumWidth(120)
        self.history_btn.clicked.connect(self.show_history_dialog)
        self.batch_btn = QPushButton(t['batch_btn'])
        self.batch_btn.setFixedHeight(44)
        self.batch_btn.setMinimumWidth(120)
        self.batch_btn.clicked.connect(self.show_batch_dialog)
        btn_row.addStretch(1)
        btn_row.addWidget(self.screenshot_btn)
        btn_row.addWidget(self.save_desc_btn)
        btn_row.addWidget(self.history_btn)
        btn_row.addWidget(self.batch_btn)
        btn_row.addStretch(1)
        btn_bar_widget = QWidget()
        btn_bar_widget.setLayout(btn_row)
        btn_bar_widget.setFixedHeight(60)
        btn_bar_widget.setStyleSheet('background: #fff; border-radius: 8px; border: 1px solid #e0e0e0;')
        layout.addWidget(btn_bar_widget)
        self.setLayout(layout)
        self.apply_theme(theme_name)

    def on_highlight_toggle(self, state):
        self.highlight = (state == Qt.Checked)
        self.refresh_previews()
    def on_highlight_theme_change(self, idx):
        self.highlight_theme = HIGHLIGHT_THEMES[self.hl_theme_combo.currentText()]
        self.refresh_previews()
    def on_theme_change(self, idx):
        theme = self.theme_combo.currentText()
        self.apply_theme(theme)
    def apply_theme(self, theme):
        self.setStyleSheet(THEME_QSS.get(theme, THEME_QSS['极简白']))

    def on_card_style_change(self, idx):
        self.refresh_previews()
    def handle_beautify(self):
        # 根据内容长度推荐合适的模板
        content_length = len(self.last_content) if self.last_content else 0
        if content_length > 1000:  # 长文推荐纯白极简
            self.card_style_combo.setCurrentText('纯白极简')
            self.split_spin.setValue(max(3, min(8, content_length // 500)))
            QMessageBox.information(self, '一键美化', '长文已应用"纯白极简"模板，确保内容完整显示并优化分割数量！')
        else:  # 短文推荐杂志卡片
            self.card_style_combo.setCurrentText('杂志卡片')
            self.split_spin.setValue(max(2, self.split_spin.value()))
            QMessageBox.information(self, '一键美化', '已应用推荐模板"杂志卡片"并优化分割，欢迎继续微调！')
        self.refresh_previews()
    def get_style_type(self):
        style_name = self.card_style_combo.currentText()
        return STYLE_MAP.get(style_name, 'minimal')

    def save_history(self):
        if not self.last_content:
            return
        data = {
            'title': self.title_edit.text(),
            'desc': self.desc_edit.toPlainText(),
            'md_blocks': self.preview_md_blocks,
            'is_md': self.last_is_md,
            'template': self.get_style_type(),
            'theme': self.theme_combo.currentText(),
            'split': self.split_spin.value(),
            'card_style': self.card_style_combo.currentText(),
            'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        os.makedirs('history', exist_ok=True)
        fname = f"history/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{data['title'][:10]}.json"
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    def handle_parse_link(self):
        url = self.link_input.text().strip()
        if not url:
            QMessageBox.warning(self, '提示', '请输入有效链接')
            return
        self.progress.setVisible(True)
        self.progress.setValue(10)
        try:
            title, content = parse_article_from_url(url)
            self.progress.setValue(40)
            xhs_title = generate_title(title, content)
            xhs_desc = generate_desc(content)
            self.progress.setValue(70)
            self.last_title = xhs_title
            self.last_desc = xhs_desc
            self.last_content = content
            self.last_is_md = False
            self.title_edit.setText(xhs_title)
            self.desc_edit.setText(xhs_desc)
            self.refresh_previews()
            self.save_history()
            self.progress.setValue(100)
        except Exception as e:
            QMessageBox.critical(self, '解析失败', str(e))
        self.progress.setVisible(False)

    def handle_upload_file(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, '选择本地文件', '', '文档 (*.md *.txt *.html)')
        if not file_paths:
            return
        if len(file_paths) == 1:
            file_path = file_paths[0]
            self.progress.setVisible(True)
            self.progress.setValue(10)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                title = os.path.basename(file_path)
                self.progress.setValue(40)
                xhs_title = generate_title(title, content)
                xhs_desc = generate_desc(content)
                self.progress.setValue(70)
                self.last_title = xhs_title
                self.last_desc = xhs_desc
                self.last_content = content
                self.last_is_md = file_path.endswith('.md')
                self.title_edit.setText(xhs_title)
                self.desc_edit.setText(xhs_desc)
                self.refresh_previews()
                self.save_history()
                self.progress.setValue(100)
            except Exception as e:
                QMessageBox.critical(self, '解析失败', str(e))
            self.progress.setVisible(False)
        else:
            # 批量处理
            for file_path in file_paths:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    title = os.path.basename(file_path)
                    xhs_title = generate_title(title, content)
                    xhs_desc = generate_desc(content)
                    is_md = file_path.endswith('.md')
                    task = {
                        'title': xhs_title,
                        'desc': xhs_desc,
                        'content': content,
                        'is_md': is_md,
                        'file': file_path
                    }
                    self.batch_tasks.append(task)
                except Exception as e:
                    QMessageBox.warning(self, '批量处理失败', f'{file_path}: {e}')
            QMessageBox.information(self, '批量处理', f'已添加 {len(file_paths)} 篇文章到批量任务，可点击"批量处理"按钮查看。')

    def on_mode_change(self, idx):
        if idx == 0:
            self.preview_mode = 'horizontal'
        else:
            self.preview_mode = 'vertical'
        self.refresh_previews()

    def refresh_previews(self):
        # 清空原有预览
        for w in self.preview_webviews:
            w.setParent(None)
        self.preview_webviews = []
        self.preview_md_blocks = []
        # 切换布局
        if self.preview_mode == 'horizontal':
            new_layout = QHBoxLayout()
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        else:
            new_layout = QVBoxLayout()
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        QWidget().setLayout(self.preview_layout)  # 释放原布局
        self.preview_layout = new_layout
        self.preview_frame.setLayout(self.preview_layout)
        if not self.last_content:
            # 空状态美化
            empty = QLabel('请先上传或解析内容，图片预览将在此处展示')
            empty.setStyleSheet('color:#aaa;font-size:1.2em;padding:3em;')
            empty.setAlignment(Qt.AlignCenter)
            self.preview_layout.addWidget(empty)
            return
        n = self.split_spin.value()
        total = n
        thumb_pixmaps = []
        full_pixmaps = []
        if self.last_is_md:
            groups = split_markdown_blocks(self.last_content, n)
            for i, group in enumerate(groups):
                md = '\n'.join([b['content'] for b in group])
                self.preview_md_blocks.append(md)
                html_content = markdown.markdown(md, extensions=['extra', 'codehilite'])
                html = render_article_html(
                    self.last_title,
                    html_content,
                    self.last_desc if i == 0 else '',
                    self.get_style_type(),
                    is_html=True,
                    highlight=self.highlight,
                    highlight_theme=self.highlight_theme,
                    badge_text=self.badge_text
                )
                card = QFrame()
                card.setObjectName('card')
                card.setFrameShape(QFrame.StyledPanel)
                card.setStyleSheet(CARD_QSS.get(self.get_style_type(), CARD_QSS['minimal']))
                add_card_shadow(card)
                card_layout = QVBoxLayout()
                card_layout.setSpacing(16)
                # 顶部信息
                top_row = QHBoxLayout()
                top_label = QLabel(f'第{i+1}张 / 共{total}张')
                top_label.setStyleSheet('font-size:1.18em;color:#1976d2;font-weight:700;letter-spacing:1px;')
                top_row.addWidget(top_label)
                top_row.addStretch(1)
                card_layout.addLayout(top_row)
                # 主图区域 - 动态调整高度避免内容裁切 (Markdown)
                webview = QWebEngineView()
                webview.setHtml(html, QUrl('about:blank'))
                webview.setMinimumWidth(600)
                webview.setMaximumWidth(600)
                
                # 根据内容长度动态设置高度，确保内容完整显示
                content_length = len(md)
                if self.get_style_type() == 'clean':
                    # 纯白极简模板：更精确的高度计算
                    estimated_height = max(600, min(1400, 400 + content_length * 0.8))
                else:
                    # 其他模板保持原有逻辑，但增加最小高度
                    estimated_height = max(800, min(1400, 600 + content_length * 0.6))
                
                webview.setMinimumHeight(int(estimated_height))
                webview.setMaximumHeight(int(estimated_height * 1.2))  # 留一些余量
                webview.setStyleSheet('background:#fff;border-radius:18px;')
                card_layout.addWidget(webview)
                # 按钮区
                btn_row = QHBoxLayout()
                edit_btn = QPushButton('编辑')
                edit_btn.setFixedWidth(120)
                edit_btn.setStyleSheet('font-size:16px; font-weight:600; background:#1976d2; color:#fff; border-radius:8px; padding:8px 0;')
                edit_btn.clicked.connect(lambda _, idx=i: self.edit_card(idx))
                export_btn = QPushButton('导出本图')
                export_btn.setFixedWidth(140)
                export_btn.setStyleSheet('font-size:16px; font-weight:600; background:#1976d2; color:#fff; border-radius:8px; padding:8px 0;')
                export_btn.clicked.connect(lambda _, idx=i: self.export_single_image(idx))
                copy_content_btn = QPushButton('复制内容')
                copy_content_btn.setFixedWidth(120)
                copy_content_btn.setStyleSheet('font-size:16px; font-weight:600; background:#1976d2; color:#fff; border-radius:8px; padding:8px 0;')
                copy_content_btn.clicked.connect(lambda _, idx=i: self.copy_thumb_content(idx))
                copy_img_btn = QPushButton('复制图片')
                copy_img_btn.setFixedWidth(120)
                copy_img_btn.setStyleSheet('font-size:16px; font-weight:600; background:#1976d2; color:#fff; border-radius:8px; padding:8px 0;')
                copy_img_btn.clicked.connect(lambda _, idx=i: self.copy_card_image(idx))
                btn_row.addStretch(1)
                btn_row.addWidget(edit_btn)
                btn_row.addWidget(export_btn)
                btn_row.addWidget(copy_content_btn)
                btn_row.addWidget(copy_img_btn)
                btn_row.addStretch(1)
                card_layout.addLayout(btn_row)
                # 内容摘要与字数
                summary = md.strip().replace('\n', ' ')
                summary = summary[:30] + ('...' if len(summary) > 30 else '')
                stat_row = QHBoxLayout()
                stat_summary = QLabel(f'摘要：{summary}')
                stat_summary.setStyleSheet('font-size:14px; color:#000; font-weight:600; padding: 4px 12px 4px 0;')
                stat_row.addWidget(stat_summary)
                stat_row.addStretch(1)
                stat_count = QLabel(f'字数：{len(md)}')
                stat_count.setStyleSheet('font-size:14px; color:#000; font-weight:600; padding: 4px 0 4px 12px;')
                stat_row.addWidget(stat_count)
                card_layout.addLayout(stat_row)
                card_layout.addSpacing(12)
                card.setLayout(card_layout)
                self.preview_layout.addWidget(card)
                self.preview_webviews.append(webview)
                # 生成缩略图
                self.repaint()  # 确保webview渲染
                QTimer.singleShot(200, lambda wv=webview, idx=i: self._set_thumb_pixmap(wv, idx))
        else:
            # 使用优化的文本分割算法
            text_groups = smart_split_text_content(self.last_content, n)
            valid_groups = [group for group in text_groups if group.strip()]
            self.preview_md_blocks = valid_groups
            
            for i, md in enumerate(valid_groups):
                html = render_article_html(
                    self.last_title,
                    md,
                    self.last_desc if i == 0 else '',
                    self.get_style_type(),
                    highlight=self.highlight,
                    highlight_theme=self.highlight_theme,
                    badge_text=self.badge_text
                )
                card = QFrame()
                card.setObjectName('card')
                card.setFrameShape(QFrame.StyledPanel)
                card.setStyleSheet(CARD_QSS.get(self.get_style_type(), CARD_QSS['minimal']))
                add_card_shadow(card)
                card_layout = QVBoxLayout()
                card_layout.setSpacing(16)
                # 顶部信息
                top_row = QHBoxLayout()
                top_label = QLabel(f'第{i+1}张 / 共{len(valid_groups)}张')
                top_label.setStyleSheet('font-size:1.18em;color:#1976d2;font-weight:700;letter-spacing:1px;')
                top_row.addWidget(top_label)
                top_row.addStretch(1)
                card_layout.addLayout(top_row)
                # 主图区域 - 动态调整高度避免内容裁切 (Text)
                webview = QWebEngineView()
                webview.setHtml(html, QUrl('about:blank'))
                webview.setMinimumWidth(600)
                webview.setMaximumWidth(600)
                
                # 根据内容长度动态设置高度，确保内容完整显示
                content_length = len(md)
                if self.get_style_type() == 'clean':
                    # 纯白极简模板：更精确的高度计算
                    estimated_height = max(600, min(1400, 400 + content_length * 0.8))
                else:
                    # 其他模板保持原有逻辑，但增加最小高度
                    estimated_height = max(800, min(1400, 600 + content_length * 0.6))
                
                webview.setMinimumHeight(int(estimated_height))
                webview.setMaximumHeight(int(estimated_height * 1.2))  # 留一些余量
                webview.setStyleSheet('background:#fff;border-radius:18px;')
                card_layout.addWidget(webview)
                # 按钮区
                btn_row = QHBoxLayout()
                edit_btn = QPushButton('编辑')
                edit_btn.setFixedWidth(120)
                edit_btn.setStyleSheet('font-size:16px; font-weight:600; background:#1976d2; color:#fff; border-radius:8px; padding:8px 0;')
                edit_btn.clicked.connect(lambda _, idx=i: self.edit_card(idx))
                export_btn = QPushButton('导出本图')
                export_btn.setFixedWidth(140)
                export_btn.setStyleSheet('font-size:16px; font-weight:600; background:#1976d2; color:#fff; border-radius:8px; padding:8px 0;')
                export_btn.clicked.connect(lambda _, idx=i: self.export_single_image(idx))
                copy_content_btn = QPushButton('复制内容')
                copy_content_btn.setFixedWidth(120)
                copy_content_btn.setStyleSheet('font-size:16px; font-weight:600; background:#1976d2; color:#fff; border-radius:8px; padding:8px 0;')
                copy_content_btn.clicked.connect(lambda _, idx=i: self.copy_thumb_content(idx))
                copy_img_btn = QPushButton('复制图片')
                copy_img_btn.setFixedWidth(120)
                copy_img_btn.setStyleSheet('font-size:16px; font-weight:600; background:#1976d2; color:#fff; border-radius:8px; padding:8px 0;')
                copy_img_btn.clicked.connect(lambda _, idx=i: self.copy_card_image(idx))
                btn_row.addStretch(1)
                btn_row.addWidget(edit_btn)
                btn_row.addWidget(export_btn)
                btn_row.addWidget(copy_content_btn)
                btn_row.addWidget(copy_img_btn)
                btn_row.addStretch(1)
                card_layout.addLayout(btn_row)
                # 内容摘要与字数
                summary = md.strip().replace('\n', ' ')
                summary = summary[:30] + ('...' if len(summary) > 30 else '')
                stat_row = QHBoxLayout()
                stat_summary = QLabel(f'摘要：{summary}')
                stat_summary.setStyleSheet('font-size:14px; color:#000; font-weight:600; padding: 4px 12px 4px 0;')
                stat_row.addWidget(stat_summary)
                stat_row.addStretch(1)
                stat_count = QLabel(f'字数：{len(md)}')
                stat_count.setStyleSheet('font-size:14px; color:#000; font-weight:600; padding: 4px 0 4px 12px;')
                stat_row.addWidget(stat_count)
                card_layout.addLayout(stat_row)
                card_layout.addSpacing(12)
                card.setLayout(card_layout)
                self.preview_layout.addWidget(card)
                self.preview_webviews.append(webview)
                self.repaint()
                QTimer.singleShot(200, lambda wv=webview, idx=i: self._set_thumb_pixmap(wv, idx))
        # 生成缩略图按钮
        for i in reversed(range(self.thumb_bar.count())):
            w = self.thumb_bar.itemAt(i).widget()
            if w:
                w.setParent(None)
        self.thumb_buttons = []
        actual_count = len(self.preview_webviews)  # 使用实际生成的webview数量
        for i in range(actual_count):
            thumb_btn = ThumbButton(i, self)
            if i == self.selected_thumb_idx:
                thumb_btn.setStyleSheet('border-radius:8px; border:2px solid #FF2D55; background:#fff; font-size:16px; font-weight:bold; color:#FF2D55;')
            thumb_btn.clicked.connect(lambda _, idx=i: self.on_thumb_clicked(idx))
            self.thumb_bar.addWidget(thumb_btn)
            self.thumb_buttons.append(thumb_btn)
    
    def _set_thumb_pixmap(self, webview, idx):
        """延迟设置缩略图，避免频繁刷新"""
        if idx < len(self.thumb_buttons):
            # 简化缩略图生成，减少性能开销
            QTimer.singleShot(500, lambda: self._generate_thumb(webview, idx))
    
    def _generate_thumb(self, webview, idx):
        """生成缩略图"""
        try:
            if idx < len(self.thumb_buttons):
                pixmap = webview.grab().scaled(36, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.thumb_buttons[idx].setPixmap(pixmap)
                self.thumb_buttons[idx].setFullPixmap(webview.grab())
        except Exception as e:
            print(f"生成缩略图失败: {e}")

    def edit_card(self, idx):
        orig_md = self.preview_md_blocks[idx]
        dlg = EditDialog(orig_md, self)
        if dlg.exec_() == QDialog.Accepted:
            new_md = dlg.get_md()
            self.preview_md_blocks[idx] = new_md
            # 重新渲染该卡片
            if self.last_is_md:
                html_content = markdown.markdown(new_md, extensions=['extra', 'codehilite'])
                html = render_article_html(
                    self.last_title,
                    html_content,
                    self.last_desc if idx == 0 else '',
                    self.get_style_type(),
                    is_html=True,
                    highlight=self.highlight,
                    highlight_theme=self.highlight_theme,
                    badge_text=self.badge_text
                )
            else:
                html = render_article_html(
                    self.last_title,
                    new_md,
                    self.last_desc if idx == 0 else '',
                    self.get_style_type(),
                    highlight=self.highlight,
                    highlight_theme=self.highlight_theme,
                    badge_text=self.badge_text
                )
            self.preview_webviews[idx].setHtml(html)

    def handle_screenshot(self):
        if not self.preview_webviews:
            QMessageBox.warning(self, '提示', '请先解析链接或上传内容')
            return
        save_dir = QFileDialog.getExistingDirectory(self, '选择保存图片文件夹')
        if not save_dir:
            return
        self._save_all_previews(save_dir)

    def _save_all_previews(self, save_dir):
        self._save_preview_idx(0, save_dir)

    def _save_preview_idx(self, idx, save_dir):
        if idx >= len(self.preview_webviews):
            QMessageBox.information(self, '保存成功', f'已保存图片到：{save_dir}')
            return
        webview = self.preview_webviews[idx]
        def after_load(ok):
            if ok:
                # 直接grab内容
                img = webview.grab()
                img_path = os.path.join(save_dir, f'xhs_img_{idx+1}.png')
                img.save(img_path)
                try:
                    webview.loadFinished.disconnect()
                except Exception:
                    pass
                QTimer.singleShot(1000, lambda: self._save_preview_idx(idx+1, save_dir))
        webview.loadFinished.connect(after_load)
        # 不再setHtml/toHtml，直接截图当前内容
        QTimer.singleShot(1000, lambda: after_load(True))

    def handle_save_desc(self):
        file_path, _ = QFileDialog.getSaveFileName(self, '保存文案', '', '文本文件 (*.txt)')
        if not file_path:
            return
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.title_edit.text() + '\n' + self.desc_edit.toPlainText())
        QMessageBox.information(self, '保存成功', '文案已保存到：' + file_path)

    def export_single_image(self, idx):
        webview = self.preview_webviews[idx]
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        save_path, _ = QFileDialog.getSaveFileName(self, '导出本图片', f'xhs_img_{idx+1}.png', 'PNG图片 (*.png)')
        if not save_path:
            return
        img = webview.grab()
        img.save(save_path)
        QMessageBox.information(self, '导出成功', f'已保存图片到：{save_path}')

    def handle_smart_split(self):
        content = self.last_content
        if not content:
            QMessageBox.information(self, '提示', '请先上传或解析内容')
            return
        
        # 优化的智能分割算法
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        total_chars = sum(len(line) for line in lines)
        
        # 根据不同因素计算推荐分割数
        n_by_length = max(1, total_chars // 800)  # 按字符数：每800字一张
        n_by_lines = max(1, len(lines) // 15)     # 按行数：每15行一张  
        n_by_structure = 1
        
        # 检查结构化内容
        if self.last_is_md:
            n_title = sum(1 for l in lines if l.startswith('#'))
            n_code = sum(1 for l in lines if l.startswith('```'))
            n_by_structure = max(n_title, n_code // 2, 1)
        
        # 综合考虑各种因素
        n = min(max(n_by_length, n_by_lines, n_by_structure), 12)  # 最多12张
        n = max(n, 1)  # 最少1张
        
        self.split_spin.setValue(n)
        
        # 推荐使用纯白极简模板进行长文分割
        if total_chars > 1000:  # 长文推荐纯白模板
            self.card_style_combo.setCurrentText('纯白极简')
            QMessageBox.information(self, '智能推荐', f'根据内容结构，推荐分割为 {n} 张图片。\n长文推荐使用"纯白极简"模板以确保内容完整显示。')
        else:
            QMessageBox.information(self, '智能推荐', f'根据内容结构，推荐分割为 {n} 张图片。你可继续微调。')
        
        self.refresh_previews()

    def on_thumb_clicked(self, idx):
        self.selected_thumb_idx = idx
        # 简化缩略图高亮逻辑
        for i, btn in enumerate(self.thumb_buttons):
            if i == idx:
                btn.setStyleSheet('border-radius:8px; border:2px solid #FF2D55; background:#fff; font-size:16px; font-weight:bold; color:#FF2D55;')
            else:
                btn.setStyleSheet('border-radius:8px; border:2px solid #e0e0e0; background:#fff; font-size:16px; font-weight:bold; color:#FF2D55;')
        
        # 滚动主预览区到对应卡片
        if self.preview_webviews and idx < len(self.preview_webviews):
            target = self.preview_webviews[idx]
            self.scroll_area.ensureWidgetVisible(target)

    def handle_thumb_drag(self, src_idx, dst_idx):
        if src_idx == dst_idx:
            return
        # 交换内容顺序
        self.preview_md_blocks.insert(dst_idx, self.preview_md_blocks.pop(src_idx))
        self.selected_thumb_idx = dst_idx
        self.refresh_previews()

    def show_history_dialog(self):
        from PyQt5.QtWidgets import QDialog, QListWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
        dlg = QDialog(self)
        dlg.setWindowTitle('历史记录')
        dlg.setMinimumSize(600, 400)
        vbox = QVBoxLayout()
        listw = QListWidget()
        files = []
        if os.path.exists('history'):
            files = sorted([f for f in os.listdir('history') if f.endswith('.json')], reverse=True)
        for f in files:
            listw.addItem(f)
        vbox.addWidget(QLabel('双击历史记录可预览/恢复'))
        vbox.addWidget(listw)
        btns = QHBoxLayout()
        del_btn = QPushButton('删除')
        export_btn = QPushButton('导出')
        btns.addWidget(del_btn)
        btns.addWidget(export_btn)
        vbox.addLayout(btns)
        dlg.setLayout(vbox)
        def on_item_double_clicked():
            idx = listw.currentRow()
            if idx < 0:
                return
            fname = files[idx]
            with open(f'history/{fname}', 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.title_edit.setText(data['title'])
            self.desc_edit.setText(data['desc'])
            self.preview_md_blocks = data['md_blocks']
            self.last_is_md = data.get('is_md', False)
            self.split_spin.setValue(data.get('split', 1))
            self.card_style_combo.setCurrentText(data.get('card_style', '杂志卡片'))
            self.theme_combo.setCurrentText(data.get('theme', '极简白'))
            self.refresh_previews()
            dlg.accept()
        listw.itemDoubleClicked.connect(on_item_double_clicked)
        def on_del():
            idx = listw.currentRow()
            if idx < 0:
                return
            fname = files[idx]
            os.remove(f'history/{fname}')
            listw.takeItem(idx)
        del_btn.clicked.connect(on_del)
        def on_export():
            idx = listw.currentRow()
            if idx < 0:
                return
            fname = files[idx]
            from PyQt5.QtWidgets import QFileDialog
            save_path, _ = QFileDialog.getSaveFileName(self, '导出历史记录', fname, 'JSON文件 (*.json)')
            if save_path:
                with open(f'history/{fname}', 'r', encoding='utf-8') as fsrc, open(save_path, 'w', encoding='utf-8') as fdst:
                    fdst.write(fsrc.read())
        export_btn.clicked.connect(on_export)
        dlg.exec_()

    def show_batch_dialog(self):
        from PyQt5.QtWidgets import QDialog, QListWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QProgressBar
        dlg = QDialog(self)
        dlg.setWindowTitle('批量处理任务')
        dlg.setMinimumSize(700, 500)
        vbox = QVBoxLayout()
        listw = QListWidget()
        for t in self.batch_tasks:
            listw.addItem(t['title'])
        vbox.addWidget(QLabel('批量任务列表（双击可预览/导出）'))
        vbox.addWidget(listw)
        btns = QHBoxLayout()
        del_btn = QPushButton('删除')
        export_btn = QPushButton('批量导出文案')
        export_img_btn = QPushButton('批量导出图片')
        export_pdf_btn = QPushButton('批量导出PDF')
        export_long_btn = QPushButton('批量导出长图')
        beautify_btn = QPushButton('批量一键美化')
        btns.addWidget(del_btn)
        btns.addWidget(export_btn)
        btns.addWidget(export_img_btn)
        btns.addWidget(export_pdf_btn)
        btns.addWidget(export_long_btn)
        btns.addWidget(beautify_btn)
        vbox.addLayout(btns)
        progress = QProgressBar()
        progress.setVisible(False)
        vbox.addWidget(progress)
        dlg.setLayout(vbox)
        def on_item_double_clicked():
            idx = listw.currentRow()
            if idx < 0:
                return
            task = self.batch_tasks[idx]
            self.title_edit.setText(task['title'])
            self.desc_edit.setText(task['desc'])
            self.last_content = task['content']
            self.last_is_md = task['is_md']
            self.refresh_previews()
            dlg.accept()
        listw.itemDoubleClicked.connect(on_item_double_clicked)
        def on_del():
            idx = listw.currentRow()
            if idx < 0:
                return
            self.batch_tasks.pop(idx)
            listw.takeItem(idx)
        del_btn.clicked.connect(on_del)
        def on_export():
            from PyQt5.QtWidgets import QFileDialog
            save_dir = QFileDialog.getExistingDirectory(self, '选择导出文件夹')
            if not save_dir:
                return
            for i, task in enumerate(self.batch_tasks):
                fname = os.path.join(save_dir, f'batch_{i+1}_{task["title"][:10]}.txt')
                with open(fname, 'w', encoding='utf-8') as f:
                    f.write(task['title'] + '\n' + task['desc'] + '\n' + task['content'])
            QMessageBox.information(self, '批量导出', f'已导出 {len(self.batch_tasks)} 篇文章到 {save_dir}')
        export_btn.clicked.connect(on_export)
        def on_export_img():
            from PyQt5.QtWidgets import QFileDialog
            save_dir = QFileDialog.getExistingDirectory(self, '选择导出图片文件夹')
            if not save_dir:
                return
            progress.setVisible(True)
            progress.setMaximum(len(self.batch_tasks))
            progress.setValue(0)
            total = len(self.batch_tasks)
            def export_one(i):
                if i >= total:
                    progress.setVisible(False)
                    QMessageBox.information(self, '批量导出图片', f'已导出所有图片到 {save_dir}')
                    return
                task = self.batch_tasks[i]
                split_n = self.split_spin.value() if hasattr(self, 'split_spin') else 3
                card_style = self.get_style_type() if hasattr(self, 'get_style_type') else 'card'
                theme = self.theme_combo.currentText() if hasattr(self, 'theme_combo') else '极简白'
                if task['is_md']:
                    groups = split_markdown_blocks(task['content'], split_n)
                    md_blocks = ['\n'.join([b['content'] for b in g]) for g in groups]
                else:
                    paras = [line.strip() for line in task['content'].split('\n') if line.strip()]
                    n = split_n
                    chunk_size = (len(paras) + n - 1) // n
                    md_blocks = ['\n'.join(paras[j*chunk_size:(j+1)*chunk_size]) for j in range(n)]
                def export_subimg(j):
                    if j >= len(md_blocks):
                        progress.setValue(i+1)
                        QTimer.singleShot(100, lambda: export_one(i+1))
                        return
                    md = md_blocks[j]
                    html = render_article_html(
                        task['title'],
                        markdown.markdown(md, extensions=['extra', 'codehilite']) if task['is_md'] else md,
                        task['desc'] if j == 0 else '',
                        card_style,
                        is_html=task['is_md'],
                        highlight=True,
                        highlight_theme='github'
                    )
                    webview = QWebEngineView()
                    webview.setHtml(html, QUrl('about:blank'))
                    webview.setMinimumWidth(600)
                    webview.setMaximumWidth(600)
                    webview.setMinimumHeight(800)
                    def save_img():
                        img = webview.grab()
                        fname = os.path.join(save_dir, f'batch_{i+1}_{task["title"][:10]}_{j+1}.png')
                        img.save(fname)
                        QTimer.singleShot(100, lambda: export_subimg(j+1))
                    QTimer.singleShot(1000, save_img)
                export_subimg(0)
            export_one(0)
        export_img_btn.clicked.connect(on_export_img)
        def on_beautify():
            split_n = self.split_spin.value() if hasattr(self, 'split_spin') else 3
            card_style = self.card_style_combo.currentText() if hasattr(self, 'card_style_combo') else '杂志卡片'
            theme = self.theme_combo.currentText() if hasattr(self, 'theme_combo') else '极简白'
            for task in self.batch_tasks:
                task['split'] = split_n
                task['card_style'] = card_style
                task['theme'] = theme
            QMessageBox.information(self, '批量一键美化', f'已为所有批量任务应用当前模板、主题和分割数！')
        beautify_btn.clicked.connect(on_beautify)
        def on_export_pdf():
            save_dir = QFileDialog.getExistingDirectory(self, '选择导出PDF文件夹')
            if not save_dir:
                return
            progress.setVisible(True)
            progress.setMaximum(len(self.batch_tasks))
            progress.setValue(0)
            for i, task in enumerate(self.batch_tasks):
                split_n = self.split_spin.value() if hasattr(self, 'split_spin') else 3
                card_style = self.get_style_type() if hasattr(self, 'get_style_type') else 'card'
                if task['is_md']:
                    groups = split_markdown_blocks(task['content'], split_n)
                    md_blocks = ['\n'.join([b['content'] for b in g]) for g in groups]
                else:
                    paras = [line.strip() for line in task['content'].split('\n') if line.strip()]
                    n = split_n
                    chunk_size = (len(paras) + n - 1) // n
                    md_blocks = ['\n'.join(paras[j*chunk_size:(j+1)*chunk_size]) for j in range(n)]
                images = []
                for j, md in enumerate(md_blocks):
                    html = render_article_html(
                        task['title'],
                        markdown.markdown(md, extensions=['extra', 'codehilite']) if task['is_md'] else md,
                        task['desc'] if j == 0 else '',
                        card_style,
                        is_html=task['is_md'],
                        highlight=True,
                        highlight_theme='github'
                    )
                    webview = QWebEngineView()
                    webview.setHtml(html, QUrl('about:blank'))
                    webview.setMinimumWidth(600)
                    webview.setMaximumWidth(600)
                    webview.setMinimumHeight(800)
                    # 截图保存为临时图片
                    QTimer.singleShot(1000, lambda wv=webview, idx=i, subidx=j: None)
                    img = webview.grab()
                    img_path = os.path.join(save_dir, f'_tmp_{i}_{j}.png')
                    img.save(img_path)
                    images.append(img_path)
                # 导出为PDF
                pdf = FPDF(unit='pt', format=[600, 800])
                for img_path in images:
                    pdf.add_page()
                    pdf.image(img_path, 0, 0, 600, 800)
                pdf_name = os.path.join(save_dir, f'batch_{i+1}_{task["title"][:10]}.pdf')
                pdf.output(pdf_name, 'F')
                # 删除临时图片
                for img_path in images:
                    try:
                        os.remove(img_path)
                    except Exception:
                        pass
                progress.setValue(i+1)
            progress.setVisible(False)
            QMessageBox.information(self, '批量导出PDF', f'已导出所有PDF到 {save_dir}')
        export_pdf_btn.clicked.connect(on_export_pdf)
        def on_export_long():
            save_dir = QFileDialog.getExistingDirectory(self, '选择导出长图文件夹')
            if not save_dir:
                return
            progress.setVisible(True)
            progress.setMaximum(len(self.batch_tasks))
            progress.setValue(0)
            for i, task in enumerate(self.batch_tasks):
                split_n = self.split_spin.value() if hasattr(self, 'split_spin') else 3
                card_style = self.get_style_type() if hasattr(self, 'get_style_type') else 'card'
                if task['is_md']:
                    groups = split_markdown_blocks(task['content'], split_n)
                    md_blocks = ['\n'.join([b['content'] for b in g]) for g in groups]
                else:
                    paras = [line.strip() for line in task['content'].split('\n') if line.strip()]
                    n = split_n
                    chunk_size = (len(paras) + n - 1) // n
                    md_blocks = ['\n'.join(paras[j*chunk_size:(j+1)*chunk_size]) for j in range(n)]
                images = []
                for j, md in enumerate(md_blocks):
                    html = render_article_html(
                        task['title'],
                        markdown.markdown(md, extensions=['extra', 'codehilite']) if task['is_md'] else md,
                        task['desc'] if j == 0 else '',
                        card_style,
                        is_html=task['is_md'],
                        highlight=True,
                        highlight_theme='github'
                    )
                    webview = QWebEngineView()
                    webview.setHtml(html, QUrl('about:blank'))
                    webview.setMinimumWidth(600)
                    webview.setMaximumWidth(600)
                    webview.setMinimumHeight(800)
                    QTimer.singleShot(1000, lambda wv=webview, idx=i, subidx=j: None)
                    img = webview.grab()
                    images.append(img)
                # 拼接长图
                if images:
                    total_height = sum(img.height() for img in images)
                    long_img = Image.new('RGB', (images[0].width(), total_height), (255,255,255))
                    y = 0
                    for img in images:
                        # QPixmap/QImage 转 PIL Image
                        buffer = img.toImage().bits().asstring(img.width()*img.height()*4)
                        pil_img = Image.frombytes('RGBA', (img.width(), img.height()), buffer)
                        pil_img = pil_img.convert('RGB')
                        long_img.paste(pil_img, (0, y))
                        y += img.height()
                    fname = os.path.join(save_dir, f'batch_{i+1}_{task["title"][:10]}_long.png')
                    long_img.save(fname)
                progress.setValue(i+1)
            progress.setVisible(False)
            QMessageBox.information(self, '批量导出长图', f'已导出所有长图到 {save_dir}')
        export_long_btn.clicked.connect(on_export_long)
        dlg.exec_()

    def on_lang_change(self, idx):
        self.lang = 'zh' if idx == 0 else 'en'
        self.clearLayout(self.layout())
        self.init_ui()
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def delete_thumb(self, idx):
        if 0 <= idx < len(self.preview_md_blocks):
            self.preview_md_blocks.pop(idx)
            self.refresh_previews()
    def copy_thumb_content(self, idx):
        if 0 <= idx < len(self.preview_md_blocks):
            content = self.preview_md_blocks[idx]
            QApplication.clipboard().setText(content)

    def update_theme_preview(self):
        # 用QPixmap+QPainter绘制主题缩略图
        idx = self.card_style_combo.currentIndex()
        style_type = list(STYLE_MAP.values())[idx]
        pix = QPixmap(120, 80)
        pix.fill(Qt.white)
        painter = QPainter(pix)
        # 背景色
        bg = {
            'minimal': QColor('#fff'),
            'card': QColor('#f3f6fa'),
            'gradient': QColor('#f8ffae'),
            'fresh': QColor('#e0f7fa'),
            'darktech': QColor('#23272e'),
            'kawaii': QColor('#fff0fa'),
            'simple': QColor('#fff'),
            'emoji': QColor('#fffde7'),
            'macaron': QColor('#ffe0f7'),
            'sticker': QColor('#fff'),
            'retro': QColor('#fdf6e3'),
            'apple': QColor('#fffbe7'),
            'cream': QColor('#fff0e6'),
            'clean': QColor('#ffffff'),
        }.get(style_type, QColor('#fff'))
        painter.setBrush(bg)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(5, 5, 110, 70, 16, 16)
        # 边框
        border = {
            'minimal': QColor('#e0e0e0'),
            'card': QColor('#1976d2'),
            'gradient': QColor('#43c6ac'),
            'fresh': QColor('#4dd0e1'),
            'darktech': QColor('#44475a'),
            'kawaii': QColor('#ffb6d5'),
            'simple': QColor('#e0e0e0'),
            'emoji': QColor('#ffd54f'),
            'macaron': QColor('#a259ff'),
            'sticker': QColor('#43a047'),
            'retro': QColor('#b58900'),
            'apple': QColor('#e1e1e1'),
            'cream': QColor('#ffd6b3'),
            'clean': QColor('#e0e0e0'),
        }.get(style_type, QColor('#e0e0e0'))
        pen = painter.pen()
        pen.setColor(border)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRoundedRect(5, 5, 110, 70, 16, 16)
        # 标题
        painter.setPen(QColor('#222'))
        painter.setFont(QFont('微软雅黑', 10, QFont.Bold))
        painter.drawText(15, 35, list(STYLE_MAP.keys())[idx])
        # 示例内容
        painter.setFont(QFont('微软雅黑', 8))
        painter.drawText(15, 55, '主题预览')
        painter.end()
        self.theme_preview.setPixmap(pix)

    def copy_card_image(self, idx):
        if 0 <= idx < len(self.preview_webviews):
            img = self.preview_webviews[idx].grab()
            QApplication.clipboard().setPixmap(img)

    def on_badge_text_change(self, text):
        self.badge_text = text if text.strip() else '原创'
        self.refresh_previews()

def emoji_icon(emoji):
    pix = QPixmap(32, 32)
    pix.fill(Qt.transparent)
    painter = QPainter(pix)
    painter.setFont(QFont('Segoe UI Emoji', 20))
    painter.drawText(pix.rect(), Qt.AlignCenter, emoji)
    painter.end()
    return QIcon(pix)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = XHSWindow()
    win.show()
    sys.exit(app.exec_()) 