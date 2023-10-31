import os
import tkinter as tk
from tkinter import ttk

import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap.constants import *

from controller.controller import Controller
from util.config import disclaimer
from util.summarizer import Summarizer
from view.ui import UI


class DisclaimerPage(tk.Frame):
    def __init__(self, master, gui):
        super().__init__(master)
        self.label = tk.Label(self, text=f"{disclaimer}\nStart the generation now?")
        self.label.pack(pady=20)
        self.next_button = ttk.Button(
            self, text="Next", bootstyle=PRIMARY, command=gui.next_page
        )
        self.next_button.pack()


class LoadingInsertPage(tk.Frame):
    def __init__(self, master, gui):
        super().__init__(master)
        self.gui = gui
        self.label = tk.Label(self, text="Loading images...")
        self.label.pack(pady=20)
        self.next_button = ttk.Button(
            self, text="Next", state=tk.DISABLED, bootstyle=PRIMARY
        )
        self.next_button.pack()

    def start_loading(self):
        if self.gui.c.event_is_set("insert_finished"):
            self.gui.c.clear_event("insert_finished")
            self.gui.next_page()
        else:
            # If the event hasn't happened yet, schedule the check_event function to run again
            self.after(100, self.start_loading)


class ChooseImagePage(tk.Frame):
    def __init__(self, master, gui):
        super().__init__(master)
        self.gui = gui
        self.image_elements = []
        self.image_date_number = None

    def __resize_image(self, image, max_width, max_height):
        # Calculate the aspect ratio to maintain the image's proportions
        width, height = image.size
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        return image.resize((new_width, new_height))

    def __image_selected_callback(self, index):
        selected_image = self.images[index]
        self.gui.c.select_image(self.image_date_number, selected_image)
        self.load_next_image_list()

    def load_next_image_list(self):
        try:
            self.image_date_number, self.images = self.gui.c.next_image_list()
        except StopIteration:
            self.gui.next_page()
            return

        # Store all image elements to prevent the garbage collector from deleting them
        del self.image_elements[:]
        # todo empty image container is shown when size of imagelist is smaller than before (list has 3 images, next list has 2 images => empty container for third one is shown)

        # todo fix window size smaller than image list
        for index, image_entry in enumerate(self.images):
            filename_label = tk.Label(self, text=image_entry.file_name)

            filename_label.grid(row=0, column=index)

            image = Image.open(
                f"{self.gui.c.args.get_image_folder_path()}/{image_entry.file_name}"
            )
            image = self.__resize_image(image, 200, 200)
            image = ImageTk.PhotoImage(image)
            self.image_elements.append(image)

            label = tk.Label(self, image=image)
            label.grid(row=1, column=index)

            label.bind(
                "<Button-1>", lambda event, i=index: self.__image_selected_callback(i)
            )

            button = tk.Button(
                self,
                text=f"Choose image {index + 1}",
                command=lambda i=index: self.__image_selected_callback(i),
            )
            button.grid(row=2, column=index)


class RenameImagesPage(tk.Frame):
    def __init__(self, master, gui):
        super().__init__(master)
        self.label = tk.Label(
            self,
            text="All files that can be imported will be renamed to the OneShot naming schema. Continue?",
        )
        self.label.pack(pady=20)
        self.next_button = ttk.Button(
            self, text="Next", bootstyle=PRIMARY, command=gui.next_page
        )
        self.next_button.pack()


class LoadingRenamePage(tk.Frame):
    def __init__(self, master, gui):
        super().__init__(master)
        self.gui = gui
        self.label = tk.Label(self, text="Renaming images...")
        self.label.pack(pady=20)
        self.next_button = ttk.Button(
            self, text="Next", state=tk.DISABLED, bootstyle=PRIMARY
        )
        self.next_button.pack()

    def start_loading(self):
        if self.gui.c.event_is_set("rename_finished"):
            self.gui.c.clear_event("rename_finished")
            self.gui.next_page()
        else:
            # If the event hasn't happened yet, schedule the check_event function to run again
            self.after(100, self.start_loading)


class WriteExportPage(tk.Frame):
    def __init__(self, master, gui):
        super().__init__(master)
        self.label = tk.Label(
            self,
            text=f"The file '{gui.file_path}' already exists. Do you want to overwrite it?",
        )
        self.label.pack(pady=20)
        self.next_button = ttk.Button(
            self, text="Next", bootstyle=PRIMARY, command=gui.next_page
        )
        self.next_button.pack()


class LoadingWriteExportPage(tk.Frame):
    def __init__(self, master, gui):
        super().__init__(master)
        self.gui = gui
        self.label = tk.Label(self, text="Writing export...")
        self.label.pack(pady=20)
        self.next_button = ttk.Button(
            self, text="Next", state=tk.DISABLED, bootstyle=PRIMARY
        )
        self.next_button.pack()

    def start_loading(self):
        if self.gui.c.event_is_set("export_finished"):
            self.gui.c.clear_event("export_finished")
            self.gui.next_page()
        else:
            # If the event hasn't happened yet, schedule the check_event function to run again
            self.after(100, self.start_loading)


class AllDonePage(tk.Frame):
    def __init__(self, master, gui):
        super().__init__(master)
        self.gui = gui
        self.label = tk.Label(
            self, text=f"✔️ Import file written to '{gui.file_path}.'"
        )
        self.label.pack(pady=20)
        self.summarization_label = tk.Label(self, text="")
        self.summarization_label.pack(pady=20)
        self.close_button = ttk.Button(
            self, text="Close", command=self.gui.next_page, bootstyle=SUCCESS
        )
        self.close_button.pack()

    def show_summarization(self):
        self.summarization_label.config(text=Summarizer().summarize(self.gui.c.counts))


class GUI(UI):
    def __init__(self, controller: Controller, skip_confirm_actions: bool) -> None:
        super().__init__(controller, skip_confirm_actions)

        self.root = ttk.Window(themename="darkly")
        self.root.title("oneshot-import")
        self.root.geometry("1200x500")

        self.file_path = self.c.args.get_export_file_location()

        if self.skip_confirm_actions:
            # Argument `-y` was provided. No confirmation is needed.
            self.pages = [
                LoadingInsertPage(self.root, self),
                ChooseImagePage(self.root, self),
                LoadingRenamePage(self.root, self),
                LoadingWriteExportPage(self.root, self),
                AllDonePage(self.root, self),
            ]
        else:
            self.pages = [
                DisclaimerPage(self.root, self),
                LoadingInsertPage(self.root, self),
                ChooseImagePage(self.root, self),
                RenameImagesPage(self.root, self),
                LoadingRenamePage(self.root, self),
                WriteExportPage(self.root, self),
                LoadingWriteExportPage(self.root, self),
                AllDonePage(self.root, self),
            ]

        self.page_gen = self.__page_gen()

        self.next_page()

    def __page_gen(self):
        for page in self.pages:
            yield page

    def next_page(self):
        if hasattr(self, "current_page"):
            self.current_page.pack_forget()

        try:
            self.current_page = next(self.page_gen)
        except StopIteration:
            self.root.destroy()  # AllDone
            return

        self.current_page.pack(fill=tk.BOTH, expand=True)

        if isinstance(self.current_page, LoadingInsertPage):
            self.c.set_event("insert")
            self.current_page.start_loading()
        elif isinstance(self.current_page, ChooseImagePage):
            self.current_page.load_next_image_list()
        elif isinstance(self.current_page, LoadingRenamePage):
            self.c.count_selected()
            self.c.set_event("rename")
            self.current_page.start_loading()
        elif isinstance(self.current_page, WriteExportPage):
            # If the file already exists, the user should be asked if it can be overwritten
            if not (os.path.exists(self.file_path) and os.path.isfile(self.file_path)):
                # Question can be skipped, because file does not exist yet
                self.next_page()
        elif isinstance(self.current_page, LoadingWriteExportPage):
            self.c.set_event("export")
            self.current_page.start_loading()
        elif isinstance(self.current_page, AllDonePage):
            self.current_page.show_summarization()

    def start(self) -> None:
        self.root.mainloop()
