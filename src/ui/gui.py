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
        self, image_name1: str, image_name2: str, image_folder_path: str, _date_time
    ):
        self.selected_index = None
        self.root = tk.Tk()
        self.root.title("Choose image")

        filename_label1 = tk.Label(self.root, text=image_name1)
        filename_label1.grid(row=0, column=0)
        image1 = Image.open(f"{image_folder_path}/{image_name1}")
        image1 = self.__resize_image(image1, 400, 400)
        image1 = ImageTk.PhotoImage(image1)
        label1 = tk.Label(self.root, image=image1)
        label1.grid(row=1, column=0)
        button1 = tk.Button(
            self.root,
            text="Choose image 1",
            command=lambda: self.__image_selected_callback(1),
        )
        button1.grid(row=2, column=0)

        filename_label1 = tk.Label(self.root, text=image_name2)
        filename_label1.grid(row=0, column=1)
        image2 = Image.open(f"{image_folder_path}/{image_name2}")
        image2 = self.__resize_image(image2, 400, 400)
        image2 = ImageTk.PhotoImage(image2)
        label2 = tk.Label(self.root, image=image2)
        label2.grid(row=1, column=1)
        button2 = tk.Button(
            self.root,
            text="Choose image 2",
            command=lambda: self.__image_selected_callback(2),
        )
        button2.grid(row=2, column=1)

        self.root.mainloop()

        return self.selected_index
