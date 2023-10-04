from ui.ui import UI
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class GUI(UI):
    def __init__(self, auto_decide: bool) -> None:
        super().__init__(auto_decide)
        self.selected_index = None
        self.root = None

    def inform(self, msg) -> None:
        self.root = tk.Tk()
        self.root.title("OneShot import")
        messagebox.showinfo("Information", msg)
        self.root.mainloop()
        # self.root.quit()
        # self.root.destroy()

    def confirm(self, msg: str, default_is_no=True) -> bool:
        self.root = tk.Tk()
        self.root.title("OneShot import")
        result = messagebox.askyesno(
            "Confirmation", msg, default="no" if default_is_no else "yes"
        )
        self.root.mainloop()
        # self.root.quit()
        # self.root.destroy()
        return result

    def __image_selected_callback(self, index):
        self.root.quit()
        self.root.destroy()
        self.selected_index = index

    def __resize_image(self, image, max_width, max_height):
        # Calculate the aspect ratio to maintain the image's proportions
        width, height = image.size
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        return image.resize((new_width, new_height))

    def choose_image(
        self,
        images: list,  # of ImageEntries
        image_folder_path: str,
        _date_time,
    ):
        self.selected_index = 0
        self.root = tk.Tk()
        self.root.title("Choose image")

        for index, image in enumerate(images):
            filename_label = tk.Label(self.root, text=image.file_name)
            filename_label.grid(row=0, column=index)

            image = Image.open(f"{image_folder_path}/{image.file_name}")
            image = self.__resize_image(image, 400, 400)
            image = ImageTk.PhotoImage(image)

            label = tk.Label(self.root, image=image)
            label.grid(row=1, column=index)

            button = tk.Button(
                self.root,
                text=f"Choose image {index + 1}",
                command=lambda i=index: self.__image_selected_callback(i),
            )
            button.grid(row=2, column=index)

        self.root.mainloop()

        return self.selected_index
