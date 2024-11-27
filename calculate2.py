import cv2
import numpy as np
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar
import sys

class ImageProcessor:
    def __init__(self, image_path, progress_callback=None):
        Image.MAX_IMAGE_PIXELS = None
        self.image_path = image_path

        if progress_callback:
            progress_callback(10)  # 10% progress after initializing

        # Use cv2.IMREAD_REDUCED_COLOR_2 to load image at reduced size
        self.image = cv2.imread(image_path, cv2.IMREAD_REDUCED_COLOR_2)

        if progress_callback:
            progress_callback(20)

        # Convert to HSV color space only once
        self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        self.result_combined = None
        self.combined_path = None

    def set_mask(self, lower_bound, upper_bound):
        return cv2.inRange(self.hsv, lower_bound, upper_bound)

    def process_image(self, lower_white, upper_white, lower_pink, upper_pink, progress_callback):
        # Create masks
        mask_white = self.set_mask(lower_white, upper_white)
        mask_pink = self.set_mask(lower_pink, upper_pink)
        progress_callback(50)

        # Combine masks using bitwise OR
        mask_combined = cv2.bitwise_or(mask_white, mask_pink)
        progress_callback(75)

        # Apply combined mask to original image
        self.result_combined = cv2.bitwise_and(self.image, self.image, mask=mask_combined)
        progress_callback(90)

    def save_images(self, combined_path):
        cv2.imwrite(combined_path, self.result_combined)

    def saveResultImage(self, filepath):
        if self.result_combined is None:
            print("Error: result_combined is not initialized. Please run process_image first.")
            return
        cv2.imwrite(filepath, self.result_combined)

    def calculate_pixel_ratio(self, combined_image, pink_mask):
        # Count non-black pixels in combined image
        non_black_pixels = cv2.countNonZero(cv2.cvtColor(combined_image, cv2.COLOR_BGR2GRAY))

        # Count pink pixels
        pink_pixels = cv2.countNonZero(pink_mask)

        result = pink_pixels / non_black_pixels if non_black_pixels > 0 else 0
        return str(round(result * 100, 2))

    def calculateRatio(self, progress_callback):
        lower_white = np.array([90, 10, 200], dtype=np.uint8)
        upper_white = np.array([140, 25, 255], dtype=np.uint8)
        lower_pink = np.array([140, 50, 50])
        upper_pink = np.array([170, 255, 255])

        self.process_image(lower_white, upper_white, lower_pink, upper_pink, progress_callback)

        self.combined_path = "./Result_whiteandpink_only.png"
        self.save_images(self.combined_path)
        progress_callback(95)

        # Calculate ratio without saving intermediate images
        pink_mask = self.set_mask(lower_pink, upper_pink)
        ratio = self.calculate_pixel_ratio(self.result_combined, pink_mask)
        progress_callback(100)
        return f"{ratio}%"

    def findUrl(self):
        return self.combined_path