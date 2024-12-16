import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image, ImageFilter
from paket.image_handler import ImageHandler
from paket.image_processor import ImageProcessor
import os

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор изображений")
        self.image_handler = ImageHandler()
        self.image_processor = None
        self.original_image = None  # Сохраняем оригинальное изображение
        self.image_resized = False  # Флаг для отслеживания изменения размера изображения

        self.create_widgets()

    def create_widgets(self):
        self.upload_button = tk.Button(self.root, text="Загрузить изображение", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=500, height=500, bg='grey')
        self.canvas.pack(pady=10)

        self.resize_button = tk.Button(self.root, text="Изменить размер до 300x300", command=self.resize_image)
        self.resize_button.pack(pady=10)

        self.blur_button = tk.Button(self.root, text="Применить размытие", command=self.apply_blur)
        self.blur_button.pack(pady=10)

        self.add_text_button = tk.Button(self.root, text="Добавить текст", command=self.add_text)
        self.add_text_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Сохранить как PNG", command=self.save_image)
        self.save_button.pack(pady=10)

    def upload_image(self):
        initial_dir = os.path.dirname(__file__)
        file_path = filedialog.askopenfilename(initialdir=initial_dir)
        if file_path:
            self.image_handler.load_image(file_path)
            self.original_image = self.image_handler.get_image().copy()  # Сохраняем копию оригинального изображения
            self.image_processor = ImageProcessor(self.image_handler.get_image())
            self.image_resized = False  # Сбрасываем флаг при загрузке нового изображения
            self.display_original_image()

    def display_original_image(self):
        img = self.image_handler.get_image()
        canvas_width, canvas_height = 500, 500
        img_width, img_height = img.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        img_tk = ImageTk.PhotoImage(img_resized)
        self.canvas.create_image((canvas_width - new_width) // 2, (canvas_height - new_height) // 2, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk

    def display_image(self, img):
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk

    def resize_image(self):
        if self.image_handler.image:
            self.image_handler.resize()
            self.image_processor = ImageProcessor(self.image_handler.get_image())
            self.image_resized = True  # Устанавливаем флаг, что изображение изменено до 300x300
            self.display_image(self.image_handler.get_image())
        else:
            messagebox.showerror("Ошибка", "Изображение не загружено")

    def apply_blur(self):
        if self.image_processor:
            self.image_processor.apply_blur()
            self.display_image(self.image_processor.image)
        else:
            messagebox.showerror("Ошибка", "Изображение не загружено")

    def add_text(self):
        if not self.image_resized:
            messagebox.showerror("Ошибка", "Необходимо сначала изменить размер изображения до 300x300")
            return
        if self.image_processor:
            self.image_processor.add_text()
            self.display_image(self.image_processor.image)
        else:
            messagebox.showerror("Ошибка", "Изображение не загружено")

    def save_image(self):
        if self.image_processor and self.image_processor.image:
            initial_dir = os.path.dirname(__file__)
            save_path = filedialog.asksaveasfilename(initialdir=initial_dir, defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                self.image_handler.save_image(save_path)
                messagebox.showinfo("Успех", "Изображение успешно сохранено")
        else:
            messagebox.showerror("Ошибка", "Нет изображения для сохранения")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()