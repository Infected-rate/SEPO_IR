import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QListWidget, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QPushButton, QFrame, QSplitter, QMenu, QProgressBar
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem

import numpy as np
from calculate2 import ImageProcessor
from CalculationThread_p import CalculationThread
from CustomGraphicsView import CustomGraphicsView
from CropThread import CropThread


class ImageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.imagePath = None
        self.resultImagePath = None
        self.setWindowIcon(QIcon("./isw.png"))
        self.polygon_points = []
        self.image_pairs = {} 
        self.polygon_item = None
        self.is_drawing = False
        self.crop_mode = False
        self.start_point = None
        self.end_point = None
        self.image_history = []
        self.calculation_results = {}

        self.initUI()


    def initUI(self):
        self.setWindowTitle('lungCalculate')
        self.setGeometry(100, 100, 1200, 800)

        # 업로드 이미지
        uploadAction = QAction('Upload Image', self)
        uploadAction.triggered.connect(self.uploadImage)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(uploadAction)

        # Create widgets
        self.imageView1 = CustomGraphicsView(self)
        self.imageScene1 = QGraphicsScene(self)
        self.imageView1.setScene(self.imageScene1)
        self.imageView1.setAlignment(Qt.AlignCenter)
        self.imageView1.setDragMode(QGraphicsView.ScrollHandDrag)

        self.imageView2 = QGraphicsView(self)
        self.imageScene2 = QGraphicsScene(self)
        self.imageView2.setScene(self.imageScene2)
        self.imageView2.setAlignment(Qt.AlignCenter)
        self.imageView2.setDragMode(QGraphicsView.ScrollHandDrag)

        self.fileListWidget1 = QListWidget(self)
        self.fileListWidget2 = QListWidget(self)
        
        # 컨텍스트 메뉴 설정
        self.fileListWidget1.setContextMenuPolicy(Qt.CustomContextMenu)
        self.fileListWidget1.customContextMenuRequested.connect(self.showContextMenu)
        self.fileListWidget2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.fileListWidget2.customContextMenuRequested.connect(self.showContextMenu)

        self.resultTextEdit = QTextEdit(self)
        self.executeButton = QPushButton('Calculate', self)
        self.executeButton.clicked.connect(self.executePythonCode)

        # Create frames
        self.imageFrame = QFrame(self)
        self.imageFrame.setFrameShape(QFrame.Box)
        self.imageFrame.setLayout(QVBoxLayout())
        
        imageSplitter = QSplitter(Qt.Vertical)
        imageSplitter.addWidget(self.imageView1)
        imageSplitter.addWidget(self.imageView2)
        imageSplitter.setSizes([400, 400])
        
        self.imageFrame.layout().addWidget(imageSplitter)

        self.fileListFrame1 = QFrame(self)
        self.fileListFrame1.setFrameShape(QFrame.Box)
        self.fileListFrame1.setLayout(QVBoxLayout())
        self.fileListFrame1.layout().addWidget(self.fileListWidget1)

        self.fileListFrame2 = QFrame(self)
        self.fileListFrame2.setFrameShape(QFrame.Box)
        self.fileListFrame2.setLayout(QVBoxLayout())
        self.fileListFrame2.layout().addWidget(self.fileListWidget2)

        fileListSplitter = QSplitter(Qt.Vertical)
        fileListSplitter.addWidget(self.fileListFrame1)
        fileListSplitter.addWidget(self.fileListFrame2)
        fileListSplitter.setSizes([400, 400])

        self.resultFrame = QFrame(self)
        self.resultFrame.setFrameShape(QFrame.Box)
        self.resultFrame.setLayout(QVBoxLayout())
        self.resultFrame.layout().addWidget(self.resultTextEdit)
        self.resultFrame.layout().addWidget(self.executeButton)

        # Layout setup
        leftSplitter = QSplitter(Qt.Vertical)
        leftSplitter.addWidget(fileListSplitter)
        leftSplitter.addWidget(self.resultFrame)
        leftSplitter.setSizes([1000, 200])

        mainSplitter = QSplitter(Qt.Horizontal)
        mainSplitter.addWidget(leftSplitter)
        mainSplitter.addWidget(self.imageFrame)
        mainSplitter.setSizes([200, 1000])

        container = QWidget()
        container.setLayout(QHBoxLayout())
        container.layout().addWidget(mainSplitter)
        self.setCentralWidget(container)

        self.fileListWidget1.itemClicked.connect(self.onFileListItemClicked1)
        self.fileListWidget2.itemClicked.connect(self.onFileListItemClicked2)


        # Add progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setMaximum(100)
        self.progressBar.setTextVisible(True)
        self.progressBar.setFormat("%p%")
        self.progressBar.hide()  # Initially hidden

        # Modify layout to include progress bar
        self.resultFrame.layout().addWidget(self.progressBar)
        self.resultFrame.layout().addWidget(self.executeButton)

        # 메뉴바 추가
        self.create_menu_bar()


         # 메뉴바에 Edit 메뉴 추가
        menubar = self.menuBar()
        editMenu = menubar.addMenu('Edit')

        # Undo 액션 생성
        undoAction = QAction('Undo', self)
        undoAction.setShortcut('Ctrl+Z')
        undoAction.triggered.connect(self.undo_action)

        # Edit 메뉴에 Undo 액션 추가
        editMenu.addAction(undoAction)
        

        self.show()

    def create_menu_bar(self):
        menubar = self.menuBar()
        crop_menu = menubar.addMenu('Crop')
        
        select_action = QAction('Select', self)
        select_action.triggered.connect(self.activate_crop_mode)
        crop_menu.addAction(select_action)

    def activate_crop_mode(self):
        self.crop_mode = True
        self.imageView1.setCursor(Qt.CrossCursor)
        self.imageView1.setDragMode(QGraphicsView.NoDrag)

    
    def onFileListItemClicked1(self, item):
        filePath = item.text()
        self.displayImage(filePath, is_original=True)
        
        # 해당 원본 이미지에 대응하는 결과 이미지가 있는지 확인
        if filePath in self.image_pairs:
            result_path = self.image_pairs[filePath]
            self.displayImage(result_path, is_original=False)
            
            # 결과 이미지 리스트에서 해당 항목 선택
            items = self.fileListWidget2.findItems(result_path, Qt.MatchExactly)
            if items:
                self.fileListWidget2.setCurrentItem(items[0])
            
            # 계산 결과 표시
            if result_path in self.calculation_results:
                result = self.calculation_results[result_path]
                self.resultTextEdit.setText(str(result))
            else:
                self.resultTextEdit.setText("No calculation result available for this image.")
        else:
            # 대응하는 결과 이미지가 없으면 결과 화면 초기화
            self.imageScene2.clear()
            self.resultTextEdit.setText("No result image available for this original image.")
            # 결과 이미지 리스트의 선택 해제
            self.fileListWidget2.clearSelection()

    def onFileListItemClicked2(self, item):
        filePath = item.text()
        self.displayImage(filePath, is_original=False)
        
        # 해당 결과 이미지에 대응하는 원본 이미지 찾기
        original_path = next((key for key, value in self.image_pairs.items() if value == filePath), None)
        if original_path:
            self.displayImage(original_path, is_original=True)
            # 원본 이미지 리스트에서 해당 항목 선택
            items = self.fileListWidget1.findItems(original_path, Qt.MatchExactly)
            if items:
                self.fileListWidget1.setCurrentItem(items[0])
        else:
            # 대응하는 원본 이미지가 없으면 원본 화면 초기화
            self.imageScene1.clear()
            # 원본 이미지 리스트의 선택 해제
            self.fileListWidget1.clearSelection()
        
        # 계산 결과 표시
        if filePath in self.calculation_results:
            result = self.calculation_results[filePath]
            self.resultTextEdit.setText(str(result))
        else:
            self.resultTextEdit.setText("No calculation result available for this image.")

    def uploadImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '', 'Images (*.png *.xpm *.jpg *.jpeg *.bmp)', options=options)
        if fileName:
            self.fileListWidget1.addItem(fileName)
            self.displayImage(fileName, is_original=True)

    def displayImage(self, filePath, is_original=True):
        pixmap = QPixmap(filePath)
        
        if is_original:
            self.imagePath = filePath
            scene = self.imageScene1
            view = self.imageView1
            self.pixmap_item = QGraphicsPixmapItem(pixmap)
            scene.clear()
            scene.addItem(self.pixmap_item)
            if filePath not in self.image_history:  # 중복 추가 방지
                self.image_history.append(filePath)
        else:
            self.resultImagePath = filePath
            scene = self.imageScene2
            view = self.imageView2
            scene.clear()
            scene.addPixmap(pixmap)
        
        scene.setSceneRect(QRectF(pixmap.rect()))
        view.setScene(scene)
        view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)


    def resizeEvent(self, event):
        if self.imagePath:
            self.imageView1.fitInView(self.imageScene1.sceneRect(), Qt.KeepAspectRatio)
        if self.resultImagePath:
            self.imageView2.fitInView(self.imageScene2.sceneRect(), Qt.KeepAspectRatio)
        super().resizeEvent(event)

    
    def showChangeImage(self, filePath):
        # 기존 항목 찾기
        items = self.fileListWidget2.findItems(filePath, Qt.MatchExactly)
        
        if items:
            # 기존 항목이 있으면 제거
            for item in items:
                row = self.fileListWidget2.row(item)
                self.fileListWidget2.takeItem(row)
        
        # 새 항목 추가 (맨 위에 추가)
        self.fileListWidget2.insertItem(0, filePath)
        
        # 새로 추가된 항목 선택
        self.fileListWidget2.setCurrentRow(0)
        
        # 이미지 표시
        self.displayImage(filePath, is_original=False)


    def updateProgress(self, value):
        self.progressBar.setValue(value)

    def showResult(self, result):
        self.resultTextEdit.setText(result)
        
        font = QFont()
        font.setPointSize(20)
        self.resultTextEdit.setFont(font)
        
        # 결과 파일 이름 생성
        original_filename = os.path.basename(self.imagePath)
        filename, extension = os.path.splitext(original_filename)
        result_filename = f"{filename}_lungCalculate{extension}"
        
        # 결과 파일 경로 생성
        result_filepath = os.path.join(os.path.dirname(self.imagePath), result_filename)
        
        # 결과 이미지 저장
        self.calc_thread.processor.saveResultImage(result_filepath)
        
        # 계산 결과 저장
        self.calculation_results[result_filepath] = result
        
        # 원본 이미지와 결과 이미지 연결
        self.image_pairs[self.imagePath] = result_filepath
        
        self.showChangeImage(result_filepath)
        
        # Hide progress bar
        self.progressBar.hide()

    def wheelEvent(self, event):
        if self.imageView1.underMouse():
            view = self.imageView1
        elif self.imageView2.underMouse():
            view = self.imageView2
        else:
            return

        if event.angleDelta().y() > 0:
            factor = 1.25
        else:
            factor = 0.8
        view.scale(factor, factor)

    def crop_image(self):
        self.progressBar.setValue(0)
        self.progressBar.show()

        self.crop_thread = CropThread(self, self.start_point, self.end_point)
        self.crop_thread.progress.connect(self.updateProgress)
        self.crop_thread.result.connect(self.finishCrop)
        self.crop_thread.start()

    def finishCrop(self, cropped_file_path):
        self.progressBar.hide()
        self.add_to_original_list(cropped_file_path)
        self.displayImage(cropped_file_path, is_original=True)
        
        self.start_point = None
        self.end_point = None
        self.crop_mode = False
        self.imageView1.setCursor(Qt.ArrowCursor)
        self.imageView1.setDragMode(QGraphicsView.ScrollHandDrag)

    def add_to_original_list(self, file_path):
        # 원본 리스트에 새 항목 추가
        self.fileListWidget1.addItem(file_path)
        
        # 이미지 히스토리에 추가
        self.image_history.append(file_path)

    def undo_action(self):
        if len(self.image_history) > 1:
            self.image_history.pop()  # 현재 이미지 제거
            previous_image = self.image_history[-1]  # 이전 이미지 가져오기
            self.displayImage(previous_image, is_original=True)
        else:
            print("No more actions to undo")


    def executePythonCode(self):
        if self.imagePath:
            processor = ImageProcessor(self.imagePath)
            
            # Show progress bar
            self.progressBar.setValue(0)
            self.progressBar.show()

            def init_progress(value):
                self.progressBar.setValue(value)
        
            processor = ImageProcessor(self.imagePath, init_progress)
            
            # Create and start calculation thread
            self.calc_thread = CalculationThread(processor)
            self.calc_thread.progress.connect(self.updateProgress)
            self.calc_thread.result.connect(self.showResult)
            self.calc_thread.start()
        else:
            self.resultTextEdit.setText("No image selected.")

    def showContextMenu(self, position):
        sender = self.sender()
        menu = QMenu()
        deleteAction = menu.addAction("Delete")
        action = menu.exec_(sender.mapToGlobal(position))
        if action == deleteAction:
            self.deleteSelectedItem(sender)

    def deleteSelectedItem(self, listWidget):
        currentItem = listWidget.currentItem()
        if currentItem:
            filePath = currentItem.text()
            row = listWidget.row(currentItem)
            listWidget.takeItem(row)
            
            # 원본 이미지 리스트에서 삭제된 경우
            if listWidget == self.fileListWidget1:
                if self.imagePath == filePath:
                    self.imagePath = None
                    self.imageScene1.clear()
                if filePath in self.image_history:
                    self.image_history.remove(filePath)
                if filePath in self.image_pairs:
                    result_path = self.image_pairs[filePath]
                    del self.image_pairs[filePath]
                    # 연결된 결과 이미지도 삭제
                    items = self.fileListWidget2.findItems(result_path, Qt.MatchExactly)
                    if items:
                        self.fileListWidget2.takeItem(self.fileListWidget2.row(items[0]))
                    if result_path in self.calculation_results:
                        del self.calculation_results[result_path]
            
            # 결과 이미지 리스트에서 삭제된 경우
            elif listWidget == self.fileListWidget2:
                if self.resultImagePath == filePath:
                    self.resultImagePath = None
                    self.imageScene2.clear()
                # 계산 결과에서도 삭제
                if filePath in self.calculation_results:
                    del self.calculation_results[filePath]
                # 연결된 원본 이미지에서 참조 제거
                for orig, res in list(self.image_pairs.items()):
                    if res == filePath:
                        del self.image_pairs[orig]
                        break
