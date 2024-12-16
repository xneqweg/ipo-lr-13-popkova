from PIL import Image

class ImageHandler:
    def __init__(self):
        self.image = None

    def load_image(self, file_path):
        self.image = Image.open(file_path)

    def get_image(self):
        return self.image

    def resize(self, new_width=300, new_height=300):
        if self.image:
            self.image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def save_image(self, path):
        if self.image:
            self.image.save(path, format='PNG')