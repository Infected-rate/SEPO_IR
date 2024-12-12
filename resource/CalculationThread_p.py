from PyQt5.QtCore import QThread, pyqtSignal

class CalculationThread(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(str)

    def __init__(self, processor):
        super().__init__()
        self.processor = processor

    def run(self):
        result = self.processor.calculateRatio(self.report_progress)
        self.result.emit(result)

    def report_progress(self, value):
        self.progress.emit(value)