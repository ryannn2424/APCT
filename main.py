import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image
import datetime

class MainApp(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.geometry("400x600")
        self.title("Note Taker")

        self.columnconfigure(0, weight=1)

        self.TopBar(self).grid(row=0, column=0, sticky="news")
        self.NoteCell(self, name="Note1").grid(row=1, column=0, sticky="news", pady=2)
        self.NoteCell(self, name="Note2").grid(row=2, column=0, sticky="news", pady=2)
        self.NoteCell(self, name="Note3").grid(row=3, column=0, sticky="news", pady=2)

        self.mainloop()

    class TopBar(ctk.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)


            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=20)
            self.columnconfigure(2, weight=1)

            currentDate = datetime.datetime.now()

            NewNoteButton = ctk.CTkLabel(self, text="", font=ctk.CTkFont(family="JetBrainsMono NFM Regular", size=40))
            NewNoteButton.grid(row=0, column=0, sticky="news", padx=5)
            NewNoteButton.bind("<Button-1>", lambda event: self.createNewNoteGUI())

            nameAndDateFrame = ctk.CTkFrame(self, fg_color="transparent")
            nameAndDateFrame.grid(column=1, row=0, sticky="news")
            nameAndDateFrame.rowconfigure(0, weight=1)
            nameAndDateFrame.columnconfigure(0, weight=1)

            programTitle = ctk.CTkLabel(nameAndDateFrame, text="Note Taker", font=ctk.CTkFont(family="Arial Bold", size=15))
            programTitle.grid(row=0, column=0)

            currentDateLabel = ctk.CTkLabel(nameAndDateFrame, text=f"{currentDate.strftime("%B")} {currentDate.strftime("%d")}, {currentDate.strftime("%Y")}",  font=ctk.CTkFont(family="Arial", size=10))
            currentDateLabel.grid(row=1, column=0, sticky="news")

            editNoteButton = ctk.CTkLabel(self, text="", font=ctk.CTkFont(family="JetBrainsMono NFM Regular", size=40))
            editNoteButton.grid(row=0, column=2, sticky="news", padx=5)

        def createNewNoteGUI(self):
            popup = ctk.CTkToplevel(self)
            popup.title("Create New Note")
            popup.geometry("240x130")
            
            selectedImage = "./image-not-found-icon.png"

            popup.columnconfigure(0, weight=1)
            # popup.columnconfigure(1, weight=4)
            popup.rowconfigure(0, weight=1)
            popup.rowconfigure(1, weight=1)

            containerFrame = ctk.CTkFrame(popup)
            containerFrame.grid(row=0, column=0, sticky="news")
            containerFrame.rowconfigure(0, weight=1)
            containerFrame.columnconfigure(0, weight=1)
            containerFrame.columnconfigure(1, weight=10)

            nameFrame = ctk.CTkFrame(containerFrame)
            nameFrame.grid(row=0,column=0, sticky="news")
            nameFrame.rowconfigure(0, weight=1)
            nameFrame.rowconfigure(1, weight=1)

            EntryLabel = ctk.CTkLabel(nameFrame, text="New Note Name")
            EntryLabel.grid(row=0, column=0, sticky="news")

            Entry = ctk.CTkEntry(nameFrame, placeholder_text="Enter name...")
            Entry.grid(row=1, column=0, sticky="news", padx=5)

            iconFrame = ctk.CTkFrame(containerFrame)
            iconFrame.grid(row=0,column=1, sticky="news")
            iconFrame.rowconfigure(0, weight=1)
            iconFrame.rowconfigure(1, weight=1)
            iconFrame.columnconfigure(0, weight=1)

            defaultIcon = ctk.CTkImage(Image.open('./openFile.png'), size=(50, 50))

            iconLabel = ctk.CTkLabel(iconFrame, text="Choose Icon")
            iconLabel.grid(row=0, column=0, sticky="news")

            iconPickerLabel = ctk.CTkLabel(iconFrame, text="", image=defaultIcon)
            iconPickerLabel.grid(column=0, row=1, sticky="news")
            iconPickerLabel.bind("<Button-1>", lambda event: selectIcon())

            buttonFrame = ctk.CTkFrame(popup)
            buttonFrame.grid(column=0, row=1, sticky="news")
            buttonFrame.rowconfigure(0, weight=1)
            buttonFrame.columnconfigure(0, weight=1)
            buttonFrame.columnconfigure(1, weight=1)

            cancelButton = ctk.CTkButton(buttonFrame, text="Cancel", command=popup.destroy)
            cancelButton.grid(column=0, row=0, sticky="news")

            createButton = ctk.CTkButton(buttonFrame, text="Create Note")
            createButton.grid(column=1, row=0, sticky="news")

            popup.after(100, popup.lift)
            
            def selectIcon():
                selectedImage = filedialog.askopenfilename()
                iconPickerLabel.configure(image=ctk.CTkImage(Image.open(selectedImage), size=(50, 50)))
                iconPickerLabel.image = ctk.CTkImage(Image.open(selectedImage), size=(50, 50))
                popup.after(100, popup.lift)



    class NoteCell(ctk.CTkFrame):
        def __init__(self, master, icon="./image-not-found-icon.png", name="placeholdStr", **kwargs):
            super().__init__(master, **kwargs)
            
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=100)

            backgroundColor = ("#FFFFFF", "#3A3B3C")

            image = ctk.CTkImage(light_image=Image.open(icon), dark_image=Image.open(icon), size=(50, 50))

            IconFrame = ctk.CTkFrame(self, width=70, height=70, fg_color="transparent")
            IconFrame.grid(column=0, row=0, sticky="news")
            IconFrame.rowconfigure(0, weight=1)
            IconFrame.columnconfigure(0, weight=1)

            iconLabel = ctk.CTkLabel(self, text="", image=image, bg_color=backgroundColor)
            iconLabel.grid(column=0, row=0, sticky="news")

            NameFrame = ctk.CTkFrame(self, height=70, fg_color=backgroundColor)
            NameFrame.grid(column=1, row=0, sticky="news")
            NameFrame.rowconfigure(0, weight=14)
            NameFrame.rowconfigure(1, weight=1)

            nameLabel = ctk.CTkLabel(NameFrame, text=name, font=ctk.CTkFont("Ariel", size=24), anchor="sw")
            nameLabel.grid(column=0, row=0, sticky="news")
            
            dateLabel = ctk.CTkLabel(NameFrame, text="Date", font=ctk.CTkFont("Ariel", size=12), anchor="w")
            dateLabel.grid(column=0, row=1, sticky="news")



MainApp()