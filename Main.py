import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QPoint


class DrawingArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desenho Digital")
        self.setFixedSize(800, 600)
        self.path = []
        self.current_path = []

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor("black"))
        painter.setPen(pen)
        for path in self.path:
            for i in range(1, len(path)):
                painter.drawLine(path[i - 1], path[i])
        if self.current_path:
            for i in range(1, len(self.current_path)):
                painter.drawLine(self.current_path[i - 1], self.current_path[i])

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.current_path:  # Inicia novo caminho apenas se não houver caminho atual
                self.current_path.append(event.pos())
            else:  # Continua caminho atual
                self.current_path.append(self.current_path[-1])  # Adiciona última posição novamente
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.current_path.append(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.path.append(self.current_path)  # Adiciona caminho atual ao caminho completo
            self.current_path = []  # Limpa caminho atual
            self.update()

    def clearDrawing(self):
        self.current_path = []
        self.path = []
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicativo de Desenho")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.drawing_area = DrawingArea()
        self.layout.addWidget(self.drawing_area)

        self.clear_button = QPushButton("Apagar")
        self.clear_button.clicked.connect(self.drawing_area.clearDrawing)
        self.layout.addWidget(self.clear_button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
