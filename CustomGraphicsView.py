import sys
import os
from PyQt5.QtGui import  QPen
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsView, QGraphicsRectItem

class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.temp_rect = None
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if self.parent.crop_mode and event.button() == Qt.LeftButton:
            self.parent.start_point = self.mapToScene(event.pos())
            self.parent.end_point = self.parent.start_point
            self.temp_rect = QGraphicsRectItem(QRectF(self.parent.start_point, self.parent.end_point))
            self.temp_rect.setPen(QPen(Qt.red, 10, Qt.SolidLine))
            self.scene().addItem(self.temp_rect)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.parent.crop_mode:
            self.setCursor(Qt.CrossCursor)
            if event.buttons() & Qt.LeftButton:
                self.parent.end_point = self.mapToScene(event.pos())
                if self.temp_rect:
                    self.temp_rect.setRect(QRectF(self.parent.start_point, self.parent.end_point).normalized())
        else:
            self.setCursor(Qt.ArrowCursor)
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.parent.crop_mode and event.button() == Qt.LeftButton:
            self.parent.end_point = self.mapToScene(event.pos())
            if self.temp_rect:
                self.scene().removeItem(self.temp_rect)
                self.temp_rect = None
            self.parent.crop_image()
        else:
            super().mouseReleaseEvent(event)

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super().leaveEvent(event)