import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from util.config import disclaimer
from view.ui import UI
from controller.controller import Controller


class DisclaimerPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(self, text=disclaimer)
        self.label.pack(pady=20)
        self.next_button = ttk.Button(self, text="Next", bootstyle=SUCCESS)
        self.next_button.pack()


class LoadingPage(tk.Frame):
    def __init__(self, master, gui):
        super().__init__(master)
        self.gui = gui
        self.label = tk.Label(self, text="Loading...")
        self.label.pack(pady=20)
        self.next_button = ttk.Button(
            self, text="Next", state=tk.DISABLED, bootstyle=SUCCESS
        )
        self.next_button.pack()

    def start_loading(self):
        self.next_button.config(state=tk.DISABLED)
        self.after(3000, self.loading_complete)

    def loading_complete(self):
        self.gui.next_page()
        self.next_button.config(state=tk.NORMAL)


class AllDonePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(self, text="All Done!")
        self.label.pack(pady=20)
        self.close_button = ttk.Button(
            self, text="Close", command=self.master.destroy, bootstyle=SUCCESS
        )
        self.close_button.pack()


class GUI(UI):
    def __init__(self, controller: Controller, auto_decide: bool) -> None:
        super().__init__(controller, auto_decide)

        self.selected_index = None

        self.root = ttk.Window(themename="darkly")
        self.root.title("oneshot-import")
        self.root.geometry("1200x500")

        self.current_page = 0

        self.pages = [
            DisclaimerPage(self.root),
            LoadingPage(self.root, self),
            AllDonePage(self.root),
        ]

        self.pages[self.current_page].pack(fill=tk.BOTH, expand=True)
        self.pages[self.current_page].next_button.config(command=self.next_page)

    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.pages[self.current_page - 1].pack_forget()
            self.pages[self.current_page].pack(fill=tk.BOTH, expand=True)
            if self.current_page == 1:
                self.pages[self.current_page].start_loading()

    def start(self, confirm_actions: bool) -> None:
        # * 1. Ask to start or to open folder
        self.root.mainloop()

    def inform(self, msg) -> None:
        self.root.title("OneShot import")
        messagebox.showinfo("Information", msg)
        self.root.mainloop()
        # self.root.quit()
        # self.root.destroy()

    def confirm(self, msg: str, default_is_no=True) -> bool:
        self.root.title("OneShot import")
        result = messagebox.askyesno(
            "Confirmation", msg, default="no" if default_is_no else "yes"
        )
        self.root.mainloop()
        # self.root.quit()
        # self.root.destroy()
        return result

    def __image_selected_callback(self, index):
        # self.root.quit()
        # self.root.destroy()
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
        self.root.title("Choose image")

        # Store all image elements to prevent the garbage collector from deleting them
        image_elements = []

        for index, image_entry in enumerate(images):
            filename_label = tk.Label(self.root, text=image_entry.file_name)
            filename_label.grid(row=0, column=index)

            image = Image.open(f"{image_folder_path}/{image_entry.file_name}")
            image = self.__resize_image(image, 400, 400)
            image = ImageTk.PhotoImage(image)
            image_elements.append(image)

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
