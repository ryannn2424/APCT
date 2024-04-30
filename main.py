import customtkinter as ctk
from customtkinter import filedialog
import tkinter.messagebox as tmsg
from PIL import Image
import datetime
import os
import webbrowser

class MainApp(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.geometry("400x600")
        self.title("Note Taker")
        self.mode = "Normal"
        self.isEdited = False

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=100)
        self.rowconfigure(2, weight=1)

        self.noteContainer= self.NoteContainer(self, cellClassRef=self.NoteCell)
        self.noteContainer.grid(row=1, column=0, sticky="news")

        self.editingWidget = self.EditingMenu(self)

        self.topBar = self.TopBar(self, self.noteContainer)
        self.topBar.grid(row=0, column=0, sticky="news")

        self.ButtonBar = self.BottomButtonBar(self)
        self.ButtonBar.grid(row=2, column=0, sticky="news")

        self.mainloop()

    def switchEditMode(self):
        if self.mode == "Normal":
            if self.noteContainer.selectedCell is not None:
                self.mode = "Edit"
                self.noteContainer.grid_forget()
                self.editingWidget.grid(row=1, column=0, sticky="news")
                self.editingWidget.loadMenu(self.noteContainer.selectedCell)
                self.ButtonBar.actionButton.configure(text="Save Note", command=self.editingWidget.saveToFile)
                self.ButtonBar.secondaryButton.configure(text="Close Note")
                self.topBar.NewNoteButton.configure(text="")
                self.topBar.NewNoteButton.unbind("<Button-1>")
                self.topBar.deleteNoteButton.configure(text="")
                self.topBar.deleteNoteButton.unbind("<Button-1>")
        else:
            self.mode = "Normal"
            self.ButtonBar.secondaryButton.configure(text="Settings", command=self.ButtonBar.secondaryButtonCommand)
            self.editingWidget.grid_forget()
            self.ButtonBar.actionButton.configure(text="Edit Selected Note", command=self.ButtonBar.actionButtonCommand)
            self.noteContainer.grid(row=1, column=0, sticky="news")
            self.topBar.NewNoteButton.configure(text="")
            self.topBar.NewNoteButton.bind("<Button-1>", lambda event: self.topBar.createNewNoteGUI())
            self.topBar.deleteNoteButton.configure(text="")
            self.topBar.deleteNoteButton.bind("<Button-1>", lambda event: self.topBar.DeleteMode())


    class EditingMenu(ctk.CTkFrame):
        def __init__(self, master, selectedCell=None, **kwargs):
            super().__init__(master, **kwargs)
            
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=20)

            if selectedCell is not None:
                self.selectedCell = selectedCell
                self.icon = selectedCell.image

            infoFrame = ctk.CTkFrame(self)
            infoFrame.grid(row=0, column=0, sticky="news")
            infoFrame.rowconfigure(0, weight=1)

            self.iconLabel = ctk.CTkLabel(infoFrame, text="")
            self.iconLabel.grid(row=0, column=0, sticky="ns", padx=5)
            self.iconLabel.bind("<Button-1>", lambda event : self.changeIcon())

            self.noteTitle = ctk.CTkLabel(infoFrame, text="NoteTitle", font=ctk.CTkFont("Ariel", size=24))
            self.noteTitle.grid(row=0, column=1, sticky="ns", padx=5)
            self.noteTitle.bind("<Button-1>", lambda event : self.renameNote())

            self.noteText = ctk.CTkTextbox(self)
            self.noteText.grid(row=1, column=0, sticky="news")
            self.noteText.bind("<KeyPress>", lambda event: self.changeEditStatus())

        def changeEditStatus(self):
            self.master.isEdited = True

        def renameNote(self):
            newName = ctk.CTkInputDialog(text="Enter new note name", title="Rename Note").get_input()
            if newName is not None:
                self.noteTitle.configure(text=newName)
                self.selectedCell.name = newName
                self.selectedCell.nameLabel.configure(text=newName)

                with open(self.selectedCell.filelocation, "r") as file:
                    lines = file.readlines()

                lines[0] = f"{newName}\n"

                with open(self.selectedCell.filelocation, "w") as file:
                    file.writelines(lines)

                directory, filename = os.path.split(self.selectedCell.filelocation)
                os.rename(self.selectedCell.filelocation, os.path.join(directory, newName + ".txt"))
                self.selectedCell.filelocation = os.path.join(directory, newName + ".txt")

        def changeIcon(self):
            newIconPath = filedialog.askopenfile().name

            with open(self.selectedCell.filelocation, "r") as file:
                    lines = file.readlines()

            lines[2] = f"{newIconPath}\n"

            with open(self.selectedCell.filelocation, "w") as file:
                file.writelines(lines)

            newImage = ctk.CTkImage(Image.open(newIconPath), size=(50, 50))
            self.iconLabel.configure(image=newImage)
            self.selectedCell.iconLabel.configure(image=newImage)
            

        def loadMenu(self, selectedCell):
            self.selectedCell = selectedCell
            self.icon = selectedCell.image
            self.iconLabel.configure(image=self.icon)
            self.noteTitle.configure(text=self.selectedCell.name)

            self.noteText.delete("0.0", "end")

            with open(self.selectedCell.filelocation, "r") as file:
                self.noteText.insert("0.0", ''.join(file.readlines()[3:]))

        def saveToFile(self, filepath=None):
            if filepath is None:
                filepath = self.selectedCell.filelocation
            with open(filepath, "r") as file:
                noteMetadata = []
                noteMetadata.append(file.readline().strip())
                noteMetadata.append(file.readline().strip())
                noteMetadata.append(file.readline().strip())

            with open(filepath, 'w') as file:
                newNote = f"{noteMetadata[0]}\n{noteMetadata[1]}\n{noteMetadata[2]}\n{self.noteText.get("0.0", "end")}"
                file.write(newNote)

            self.master.isEdited = False

        

    class BottomButtonBar(ctk.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, fg_color="transparent", **kwargs)
            self.columnconfigure(0, weight=1)

            self.master = master
            
            interactionButtonsFrame = ctk.CTkFrame(self)
            interactionButtonsFrame.grid(row=0, column=0, columnspan=2, sticky="news")
            interactionButtonsFrame.columnconfigure(0, weight=1)
            interactionButtonsFrame.columnconfigure(1, weight=1)
            
            helpButtonFrame = ctk.CTkFrame(self)
            helpButtonFrame.grid(row=1, column=0, sticky="news", pady=2)
            helpButtonFrame.columnconfigure(0, weight=1)

            self.actionButton = ctk.CTkButton(interactionButtonsFrame, text="Edit Selected Note", command=lambda: self.actionButtonCommand())
            self.actionButton.grid(column=0, row=0, sticky="news", padx=2)

            self.secondaryButton = ctk.CTkButton(interactionButtonsFrame, text="Settings", command=lambda: self.secondaryButtonCommand())
            self.secondaryButton.grid(column=1, row=0, sticky="news", padx=2)
            
            self.helpButton = ctk.CTkButton(helpButtonFrame, text="Help", command=lambda: self.helpButtonCommand())
            self.helpButton.grid(column=0, row=0, sticky="news", padx=2)

        def helpButtonCommand(self):
            if tmsg.askyesno("Help", "Do you want to open the Instructions Page?"):
                webbrowser.open(f"file://{os.getcwd()}/help.html")
                
        def actionButtonCommand(self):
            if self.master.mode == "Delete":
                if tmsg.askyesno("Delete Note", "Are you sure you want to delete this note?"):
                    self.master.noteContainer.selectedCell.deleteSelf()
            elif self.master.mode == "Normal":
                self.master.switchEditMode()

        def secondaryButtonCommand(self):
            if self.master.mode == "Edit":
                if self.master.isEdited:
                    if tmsg.askyesno("Unsaved File", "You have unsaved changes. Are you sure you want to close this note?"):
                        self.master.switchEditMode()
                else:
                    self.master.switchEditMode()
            elif self.master.mode == "Normal" or self.master.mode == "Delete":
                popup = ctk.CTkToplevel(self)
                currentTheme = ctk.StringVar()
                currentTheme.set(ctk.get_appearance_mode())
                ctk.CTkLabel(popup, text="Current Theme").pack(padx=5, pady=5)
                
                themeSelector = ctk.CTkOptionMenu(popup, variable=currentTheme, values=["Light", "Dark"], command=lambda new_theme: ctk.set_appearance_mode(new_theme))
                themeSelector.pack(padx=5, pady=5)
                
                popup.after(100, popup.lift)
                
                



    class NoteContainer(ctk.CTkFrame):
        def __init__(self, master, cellClassRef, **kwargs):
            super().__init__(master, fg_color="transparent", **kwargs)
            
            def populatePathList(pathList):
                for file in os.listdir('./Notes'):
                    if file.endswith(".txt"):
                        pathList.append(file)

            def populateNoteContainer(noteList):
                
                populatePathList(noteList)
                
                for file in savedNotesFiles:
                    with open(f"Notes/{file}", "r") as noteFile:
                        name = noteFile.readline().strip()
                        date = noteFile.readline().strip()
                        iconPath = noteFile.readline().strip()
                        filePath = f"Notes/{file}"
                        self.addCell(name, iconPath, date, filePath)

            self.cellClassRef = cellClassRef
            self.noteIndex = 0
            self.selectedCell = None
            self.master = master

            self.columnconfigure(0, weight=1)

            savedNotesFiles = []

            populateNoteContainer(savedNotesFiles)

        def addCell(self, name, iconPath, date, filepath=None, createFile=False):
            if filepath == None: filepath = f"Notes/{name}.txt"
            newCell = self.cellClassRef(self, name=name, icon=iconPath, date=date, filelocation=filepath)
            newCell.grid(row=self.noteIndex, column=0, sticky="news", pady=2)
            if createFile:
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

            self.NewNoteButton = ctk.CTkLabel(self, text="", font=ctk.CTkFont(family="JetBrainsMono NFM Regular", size=40))
            self.NewNoteButton.grid(row=0, column=0, sticky="news", padx=5)
            self.NewNoteButton.bind("<Button-1>", lambda event: self.createNewNoteGUI())

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
                self.cellContainerRef.addCell(Entry.get(), self.selectedImage, f"{self.currentDate.strftime("%B")} {self.currentDate.strftime("%d")}, {self.currentDate.strftime("%Y")} - {self.currentDate.strftime('%I')}: {self.currentDate.strftime('%M')} {self.currentDate.strftime('%p')}", createFile=True)
                popup.destroy()

    class NoteCell(ctk.CTkFrame):
        def __init__(self, master, icon="./image-not-found-icon.png", name="placeholdStr", date="placeholdStr", filelocation="placeholdStr", **kwargs):
            super().__init__(master, **kwargs)
            
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=100)

            self.filelocation = filelocation
            self.name = name
            backgroundColor = ("#FFFFFF", "#3A3B3C")
            
            try:
                self.image = ctk.CTkImage(light_image=Image.open(icon), dark_image=Image.open(icon), size=(50, 50))
            except:
                self.image = ctk.CTkImage(light_image=Image.open("./image-not-found-icon.png"), dark_image=Image.open("./image-not-found-icon.png"), size=(50, 50))

            self.IconFrame = ctk.CTkFrame(self, width=70, height=70, fg_color="transparent")
            self.IconFrame.grid(column=0, row=0, sticky="news")
            self.IconFrame.rowconfigure(0, weight=1)
            self.IconFrame.columnconfigure(0, weight=1)

            self.iconLabel = ctk.CTkLabel(self, text="", image=self.image, bg_color=backgroundColor)
            self.iconLabel.grid(column=0, row=0, sticky="news")

            self.NameFrame = ctk.CTkFrame(self, height=70, fg_color=backgroundColor)
            self.NameFrame.grid(column=1, row=0, sticky="news")
            self.NameFrame.rowconfigure(0, weight=14)
            self.NameFrame.rowconfigure(1, weight=1)

            self.nameLabel = ctk.CTkLabel(self.NameFrame, text=name, font=ctk.CTkFont("Ariel", size=24), anchor="sw")
            self.nameLabel.grid(column=0, row=0, sticky="news")
            
            dateLabel = ctk.CTkLabel(self.NameFrame, text=date, font=ctk.CTkFont("Ariel", size=12), anchor="w")
            dateLabel.grid(column=0, row=1, sticky="news")

            self.bind("<Button-1>", lambda event: self.selectSelf())
            self.IconFrame.bind("<Button-1>", lambda event: selectSelf())
            self.iconLabel.bind("<Button-1>", lambda event: selectSelf())
            self.NameFrame.bind("<Button-1>", lambda event: selectSelf())
            self.nameLabel.bind("<Button-1>", lambda event: selectSelf())
            dateLabel.bind("<Button-1>", lambda event: selectSelf())


            def selectSelf():
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