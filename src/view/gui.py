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
    def __init__(self, master, gui):
        super().__init__(master)
        self.label = tk.Label(self, text=disclaimer)
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
            # If the event hasn't happened yet, schedule the check_event function to run again in 1000 milliseconds
            self.after(100, self.start_loading)


class ChooseImagePage(tk.Frame):
    def __init__(self, master, gui):
        super().__init__(master)
        self.gui = gui

    def load_image_list(self):
        self.label = tk.Label(self, text=f"{self.gui.c.next_image_list()}")
        self.label.pack(pady=20)
        self.next_button = ttk.Button(
            self, text="Next", bootstyle=PRIMARY, command=self.gui.next_page
        )
        self.next_button.pack()


class ChooseImagePage(tk.Frame):
    # todo: display images and put selected image in c.selected_images
    def __init__(self, master, gui):
        super().__init__(master)
        self.gui = gui
        self.label = tk.Label(self, text="")
        self.label.pack(pady=20)
        self.next_button = ttk.Button(
            self, text="Next", command=self.load_next_image_list
        )
        self.next_button.pack()

    def load_next_image_list(self):
        try:
            images = self.gui.c.next_image_list()
            self.label.config(text=images)
        except StopIteration:
            self.gui.next_page()


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
    def __init__(
        self, controller: Controller, auto_decide: bool, confirm_actions: bool
    ) -> None:
        super().__init__(controller, auto_decide, confirm_actions)

        self.selected_index = None

        self.root = ttk.Window(themename="darkly")
        self.root.title("oneshot-import")
        self.root.geometry("1200x500")

        self.current_page = 0

        self.pages = [
            DisclaimerPage(self.root, self),
            LoadingInsertPage(self.root, self),
            ChooseImagePage(self.root, self),
            AllDonePage(self.root),
        ]

        self.pages[self.current_page].pack(fill=tk.BOTH, expand=True)

    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.pages[self.current_page - 1].pack_forget()
            self.pages[self.current_page].pack(fill=tk.BOTH, expand=True)
            if self.current_page == 1:  # LoadingInsertPage
                self.c.set_event("insert")
                self.pages[self.current_page].start_loading()
            elif self.current_page == 2:  # ChooseImagePage
                self.pages[self.current_page].load_next_image_list()

    def start(self) -> None:
        self.root.mainloop()

    # // def __inform(self, msg) -> None:
    # //     self.root.title("OneShot import")
    # //     messagebox.showinfo("Information", msg)
    # //     self.root.mainloop()
    # //     # self.root.quit()
    # //     # self.root.destroy()

    # // def __confirm(self, msg: str, default_is_no=True) -> bool:
    # //     self.root.title("OneShot import")
    # //     result = messagebox.askyesno(
    # //         "Confirmation", msg, default="no" if default_is_no else "yes"
    # //     )
    # //     self.root.mainloop()
    # //     # self.root.quit()
    # //     # self.root.destroy()
    # //     return result

    # // def __image_selected_callback(self, index):
    # //     # self.root.quit()
    # //     # self.root.destroy()
    # //     self.selected_index = index

    # // def __resize_image(self, image, max_width, max_height):
    # //     # Calculate the aspect ratio to maintain the image's proportions
    # //     width, height = image.size
    # //     ratio = min(max_width / width, max_height / height)
    # //     new_width = int(width * ratio)
    # //     new_height = int(height * ratio)
    # //     return image.resize((new_width, new_height))

    # // def __choose_image(
    # //     self,
    # //     images: list,  # of ImageEntries
    # //     image_folder_path: str,
    # //     _date_time,
    # // ):
    # //     self.selected_index = 0
    # //     self.root.title("Choose image")

    # //     # Store all image elements to prevent the garbage collector from deleting them
    # //     image_elements = []

    # //     for index, image_entry in enumerate(images):
    # //         filename_label = tk.Label(self.root, text=image_entry.file_name)
    # //         filename_label.grid(row=0, column=index)

    # //         image = Image.open(f"{image_folder_path}/{image_entry.file_name}")
    # //         image = self.__resize_image(image, 400, 400)
    # //         image = ImageTk.PhotoImage(image)
    # //         image_elements.append(image)

    # //         label = tk.Label(self.root, image=image)
    # //         label.grid(row=1, column=index)

    # //         button = tk.Button(
    # //             self.root,
    # //             text=f"Choose image {index + 1}",
    # //             command=lambda i=index: self.__image_selected_callback(i),
    # //         )
    # //         button.grid(row=2, column=index)

    # //     self.root.mainloop()

    # //     return self.selected_index
