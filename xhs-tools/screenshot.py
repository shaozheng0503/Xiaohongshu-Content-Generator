from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter

def save_webview_as_image(webview, file_path):
    def _capture():
        page = webview.page()
        size = webview.size()
        img = QImage(size, QImage.Format_ARGB32)
        painter = None
        try:
            painter = QPainter(img)
            page.view().render(painter)
            img.save(file_path)
        finally:
            if painter:
                painter.end()
    QTimer.singleShot(500, _capture) 