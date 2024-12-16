from PIL import ImageFilter, ImageDraw, ImageFont

class ImageProcessor:
    def __init__(self, image):
        self.image = image

    def apply_blur(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.BLUR)

    def add_text(self, text="Вариант 1", font_path='arial.ttf', font_size=20):
        if self.image:
            draw = ImageDraw.Draw(self.image)
            font = ImageFont.truetype(font_path, font_size)
            # Исправляем на использование textbbox
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            position = (self.image.width - text_width - 10, self.image.height - text_height - 10)
            draw.text(position, text, font=font, fill='white')