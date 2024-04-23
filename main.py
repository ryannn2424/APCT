import customtkinter as ctk
from customtkinter import filedialog
import tkinter.messagebox as tmsg
from PIL import Image
import datetime
import os

class MainApp(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.geometry("400x600")
        self.title("Note Taker")
        self.mode = "Normal"

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        self.rowconfigure(2, weight=1)

        self.noteContainer= self.NoteContainer(self, cellClassRef=self.NoteCell)
        self.noteContainer.grid(row=1, column=0, sticky="news")

        self.editingWidget = self.EditingMenu(self)

        self.TopBar(self, self.noteContainer).grid(row=0, column=0, sticky="news")

        self.ButtonBar = self.BottomButtonBar(self)
        self.ButtonBar.grid(row=2, column=0, sticky="news")

        self.mainloop()

    def switchEditMode(self):
        if self.mode == "Normal":
            if self.noteContainer.selectedCell is not None:
                self.mode = "Edit"
                print('run')
                self.editingWidget.grid(row=1, column=0, sticky="news")
                self.editingWidget.loadMenu(self.noteContainer.selectedCell)
        else:
            self.mode = "Normal"

    class EditingMenu(ctk.CTkFrame):
        def __init__(self, master, selectedCell=None, **kwargs):
            super().__init__(master, **kwargs)
            
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

            if selectedCell is not None:
                self.selectedCell = selectedCell
                self.icon = selectedCell.image

            self.iconLabel = ctk.CTkLabel(self, text="")
            self.iconLabel.grid(row=0, column=0, sticky="news")

        def loadMenu(self, selectedCell):
            self.selectedCell = selectedCell
            self.icon = selectedCell.image

            self.iconLabel.configure(image=self.icon)




    class BottomButtonBar(ctk.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, fg_color="transparent", **kwargs)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)

            self.master = master

            self.actionButton = ctk.CTkButton(self, text="Edit Selected Note", command=lambda: self.actionButtonCommand())
            self.actionButton.grid(column=0, row=0, sticky="news", padx=2)

            ctk.CTkButton(self, text="Settings").grid(column=1, row=0, sticky="news", padx=2)

        def actionButtonCommand(self):
            if self.master.mode == "Delete":
                if tmsg.askyesno("Delete Note", "Are you sure you want to delete this note?"):
                    self.master.noteContainer.selectedCell.deleteSelf()
            elif self.master.mode == "Normal":
                self.master.switchEditMode()


    class NoteContainer(ctk.CTkFrame):
        def __init__(self, master, cellClassRef, **kwargs):
            super().__init__(master, fg_color="transparent", **kwargs)

            self.cellClassRef = cellClassRef
            self.noteIndex = 0
            self.selectedCell = None
            self.master = master
            # self.cellList = []

            self.columnconfigure(0, weight=1)

            savedNotesFiles = []
            for file in os.listdir('./Notes'):
                if file.endswith(".txt"):
                    savedNotesFiles.append(file)

            for file in savedNotesFiles:
                with open(f"Notes/{file}", "r") as noteFile:
                    name = noteFile.readline().strip()
                    date = noteFile.readline().strip()
                    iconPath = noteFile.readline().strip()
                    filePath = f"Notes/{file}"
                    self.addCell(name, iconPath, date, filePath)

        def addCell(self, name, iconPath, date, filepath=None):
            if filepath == None: filepath = f"Notes/{name}.txt"
            newCell = self.cellClassRef(self, name=name, icon=iconPath, date=date, filelocation=filepath)
            newCell.grid(row=self.noteIndex, column=0, sticky="news", pady=2)
            # self.cellList.append(newCell)
            with open(f"Notes/{name}.txt", "w") as noteFile:
                noteFile.write(f"{name}\n{date}\n{iconPath}\n")
            self.noteIndex += 1

    class TopBar(ctk.CTkFrame):
        def __init__(self, master, cellContainerRef, **kwargs):
            super().__init__(master, **kwargs)
            self.master = master

            self.cellContainerRef = cellContainerRef

            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=20)
            self.columnconfigure(2, weight=1)

            self.currentDate = datetime.datetime.now()

            NewNoteButton = ctk.CTkLabel(self, text="", font=ctk.CTkFont(family="JetBrainsMono NFM Regular", size=40))
            NewNoteButton.grid(row=0, column=0, sticky="news", padx=5)
            NewNoteButton.bind("<Button-1>", lambda event: self.createNewNoteGUI())

            nameAndDateFrame = ctk.CTkFrame(self, fg_color="transparent")
            nameAndDateFrame.grid(column=1, row=0, sticky="news")
            nameAndDateFrame.rowconfigure(0, weight=1)
            nameAndDateFrame.columnconfigure(0, weight=1)

            programTitle = ctk.CTkLabel(nameAndDateFrame, text="Note Taker", font=ctk.CTkFont(family="Arial Bold", size=15))
            programTitle.grid(row=0, column=0)

            self.currentDateLabel = ctk.CTkLabel(nameAndDateFrame, text=f"{self.currentDate.strftime("%B")} {self.currentDate.strftime("%d")}, {self.currentDate.strftime("%Y")}",  font=ctk.CTkFont(family="Arial", size=10))
            self.currentDateLabel.grid(row=1, column=0, sticky="news")

            self.deleteNoteButton = ctk.CTkLabel(self, text="", font=ctk.CTkFont(family="JetBrainsMono NFM Regular", size=40))
            self.deleteNoteButton.grid(row=0, column=2, sticky="news", padx=5)
            self.deleteNoteButton.bind("<Button-1>", lambda event: self.DeleteMode())

        def DeleteMode(self):
            if self.master.mode != "Delete":
                self.master.ButtonBar.actionButton.configure(text="Delete Selected Note")
                self.master.mode="Delete"
                if self.master.noteContainer.selectedCell is not None:
                    # self.master.noteContainer.selectedCell.delete()
                    # self.master.noteContainer.selectedCell = None
                    self.master.noteContainer.selectedCell.configure(fg_color="#8F0000")
                    self.master.noteContainer.selectedCell.IconFrame.configure(fg_color="#8F0000")
                    self.master.noteContainer.selectedCell.NameFrame.configure(fg_color="#8F0000")
                    self.deleteNoteButton.configure(text="󰜺", font=ctk.CTkFont(family="JetBrainsMono NFM Regular", size=40))
            else:
                self.master.ButtonBar.actionButton.configure(text="Edit Selected Note")
                self.master.mode="Normal"
                if self.master.noteContainer.selectedCell is not None:
                    self.master.noteContainer.selectedCell.configure(fg_color="#428CD4")
                    self.master.noteContainer.selectedCell.IconFrame.configure(fg_color="#428CD4")
                    self.master.noteContainer.selectedCell.NameFrame.configure(fg_color="#428CD4")
                    self.deleteNoteButton.configure(text="", font=ctk.CTkFont(family="JetBrainsMono NFM Regular", size=40))

        def createNewNoteGUI(self):
            popup = ctk.CTkToplevel(self)
            popup.title("Create New Note")
            popup.geometry("300x150")
            
            self.selectedImage = "./image-not-found-icon.png"

            popup.columnconfigure(0, weight=1)
            # popup.columnconfigure(1, weight=4)
            popup.rowconfigure(0, weight=2)
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

            createButton = ctk.CTkButton(buttonFrame, text="Create Note", command= lambda: createCell())
            createButton.grid(column=1, row=0, sticky="news")

            popup.after(100, popup.lift)
            
            def selectIcon():
                self.selectedImage = filedialog.askopenfilename()
                iconPickerLabel.configure(image=ctk.CTkImage(Image.open(self.selectedImage), size=(50, 50)))
                iconPickerLabel.image = ctk.CTkImage(Image.open(self.selectedImage), size=(50, 50))
                popup.after(100, popup.lift)

            def createCell():
                if self.selectedImage == "./openFile.png":
                    self.selectedImage = "./image-not-found-icon.png"
                self.cellContainerRef.addCell(Entry.get(), self.selectedImage, f"{self.currentDate.strftime("%B")} {self.currentDate.strftime("%d")}, {self.currentDate.strftime("%Y")} - {self.currentDate.strftime('%I')}: {self.currentDate.strftime('%M')} {self.currentDate.strftime('%p')}")
                popup.destroy()

    class NoteCell(ctk.CTkFrame):
        def __init__(self, master, icon="./image-not-found-icon.png", name="placeholdStr", date="placeholdStr", filelocation="placeholdStr", **kwargs):
            super().__init__(master, **kwargs)
            
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=100)

            self.filelocation = filelocation
            backgroundColor = ("#FFFFFF", "#3A3B3C")

            self.image = ctk.CTkImage(light_image=Image.open(icon), dark_image=Image.open(icon), size=(50, 50))

            self.IconFrame = ctk.CTkFrame(self, width=70, height=70, fg_color="transparent")
            self.IconFrame.grid(column=0, row=0, sticky="news")
            self.IconFrame.rowconfigure(0, weight=1)
            self.IconFrame.columnconfigure(0, weight=1)

            iconLabel = ctk.CTkLabel(self, text="", image=self.image, bg_color=backgroundColor)
            iconLabel.grid(column=0, row=0, sticky="news")

            self.NameFrame = ctk.CTkFrame(self, height=70, fg_color=backgroundColor)
            self.NameFrame.grid(column=1, row=0, sticky="news")
            self.NameFrame.rowconfigure(0, weight=14)
            self.NameFrame.rowconfigure(1, weight=1)

            nameLabel = ctk.CTkLabel(self.NameFrame, text=name, font=ctk.CTkFont("Ariel", size=24), anchor="sw")
            nameLabel.grid(column=0, row=0, sticky="news")
            
            dateLabel = ctk.CTkLabel(self.NameFrame, text=date, font=ctk.CTkFont("Ariel", size=12), anchor="w")
            dateLabel.grid(column=0, row=1, sticky="news")

            self.bind("<Button-1>", lambda event: self.selectSelf())
            self.IconFrame.bind("<Button-1>", lambda event: selectSelf())
            iconLabel.bind("<Button-1>", lambda event: selectSelf())
            self.NameFrame.bind("<Button-1>", lambda event: selectSelf())
            nameLabel.bind("<Button-1>", lambda event: selectSelf())
            dateLabel.bind("<Button-1>", lambda event: selectSelf())


            def selectSelf():
                print(master.selectedCell)
                if self.master.selectedCell != self:
                    if self.master.master.mode == "Delete":
                        self.configure(fg_color="#8F0000")
                        self.IconFrame.configure(fg_color="#8F0000")
                        self.NameFrame.configure(fg_color="#8F0000")
                    else:
                        self.configure(fg_color="#428CD4")
                        self.IconFrame.configure(fg_color="#428CD4")
                        self.NameFrame.configure(fg_color="#428CD4")

                    if self.master.selectedCell != None:
                        self.master.selectedCell.configure(fg_color="#3A3B3C")
                        self.master.selectedCell.IconFrame.configure(fg_color="#3A3B3C")
                        self.master.selectedCell.NameFrame.configure(fg_color="#3A3B3C")

                    self.master.selectedCell = self

        def deleteSelf(self):
            self.master.selectedCell = None
            os.remove(self.filelocation)
            self.destroy()




MainApp()