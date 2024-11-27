
from PyQt5.QtCore import  QRectF, QThread, pyqtSignal


class CropThread(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(str)

    def __init__(self, image_app, start_point, end_point):
        super().__init__()
        self.image_app = image_app
        self.start_point = start_point
        self.end_point = end_point

    def run(self):
        rect = QRectF(self.start_point, self.end_point).normalized()
        cropped_pixmap = self.image_app.pixmap_item.pixmap().copy(rect.toRect())
        
        # Simulate a time-consuming process
        for i in range(101):
            self.progress.emit(i)
            self.msleep(30)  # Sleep for 30ms

        # Save the cropped image
        cropped_file_path = self.image_app.imagePath.rsplit('.', 1)[0] + '_cropped.' + self.image_app.imagePath.rsplit('.', 1)[1]
        cropped_pixmap.save(cropped_file_path)
        
        self.result.emit(cropped_file_path)