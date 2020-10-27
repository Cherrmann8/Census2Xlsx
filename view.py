from tkinter import *
from tkinter.ttk import *
import model
import logging
import json

"""
Author: Charles Herrmann
Date: 10/27/20
Description: GUI for Census2xlsx application
"""

logging.basicConfig(filename='c2x.log', filemode='w', level=logging.INFO)
logger = logging.getLogger('view')


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class GeoPage(Page):
    geos = {}
    geoIDs = []

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.loadGeos()

        listBoxFrame1 = Frame(self)
        label1 = Label(listBoxFrame1, text="States:", anchor='center')
        label1.pack(side="top", fill="both", expand=True)
        self.listbox1 = Listbox(listBoxFrame1)
        self.listbox1.pack(side='bottom', fill='both', expand=True)
        listBoxFrame1.pack(side='left', fill='both', expand=True)

        buttonFrame = Frame(self)
        add = Button(buttonFrame, text="Add", command=self.addButton)
        add.pack(side="top", fill="x", expand=False)
        remove = Button(buttonFrame, text="Remove", command=self.removeButtom)
        remove.pack(side="bottom", fill="x", expand=False)
        buttonFrame.pack(side='left', fill='x', expand=False)

        listBoxFrame2 = Frame(self)
        label4 = Label(listBoxFrame2, text="Selected Geographies:", anchor='center')
        label4.pack(side="top", fill="both", expand=True)
        self.listbox2 = Listbox(listBoxFrame2)
        self.listbox2.pack(side='bottom', fill='both', expand=True)
        listBoxFrame2.pack(side='right', fill='both', expand=True)

        self.fillListBox1()

    def loadGeos(self):
        logger.info("Loading geographies.json")
        with open('geographies.json', 'r') as loadfile:
            self.geos = json.load(loadfile)
        logger.info("geographies.json loaded")

    def fillListBox1(self):
        # print(self.geos)
        for state in self.geos.keys():
            self.listbox1.insert(END, state)

    def addButton(self):
        selection = self.listbox1.curselection()
        if len(selection) > 0:
            geo = self.listbox1.get(selection[0])
            if self.geos[geo]['ID'] not in self.geoIDs:
                self.listbox2.insert(END, geo)
                self.geoIDs.append(self.geos[geo]['ID'])

    def removeButtom(self):
        print(self.geoIDs)


class TablePage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="This is page 2")
        label.pack(side="top", fill="both", expand=True)


class ConfPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="This is page 3")
        label.pack(side="top", fill="both", expand=True)


class MainView(Frame):
    pageID = 0

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        # Header Frame - Contains app name and settings button
        headerFrame = Frame(self)
        label1 = Label(headerFrame, text="Cen2Xlsx")
        # TODO: Change this to picture of gear
        label2 = Label(headerFrame, text="Settings")

        headerFrame.pack(side="top", fill="x", expand=False)
        label1.pack(side="left")
        label2.pack(side="right")

        # Progress Frame - Contains images showing progression of user
        progressFrame = Frame(self)
        label2 = Label(progressFrame, text="(===PROGRESS===)")

        progressFrame.pack(side="top", fill="x", expand=False)
        label2.pack(side="top", anchor='center')

        # Pages Frame - Contains each page of the generation setup (Geographies, Tables, Confirmation)
        pagesFrame = Frame(self)
        self.p1 = GeoPage(self)
        self.p2 = TablePage(self)
        self.p3 = ConfPage(self)

        pagesFrame.pack(side="top", fill="both", expand=True)
        self.p1.place(in_=pagesFrame, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=pagesFrame, x=0, y=0, relwidth=1, relheight=1)
        self.p3.place(in_=pagesFrame, x=0, y=0, relwidth=1, relheight=1)

        # Navigation Frame - Contains the next, back, and generate buttons
        buttonFrame = Frame(self)
        self.next = Button(buttonFrame, text="Next", command=self.nextPage)
        self.prev = Button(buttonFrame, text="Back", command=self.lastPage)

        buttonFrame.pack(side="bottom", fill="x", expand=False)
        self.next.pack(side="right")
        self.prev.pack(side="left")

        self.show()

    def nextPage(self):
        if self.pageID < 2:
            self.pageID += 1
            self.show()

    def lastPage(self):
        if self.pageID > 0:
            self.pageID -= 1
            self.show()

    def show(self):
        if self.pageID == 0:
            self.p1.show()
            self.prev.pack_forget()
            self.next.pack(side="right")
        elif self.pageID == 1:
            self.p2.show()
            self.prev.pack(side="left")
            self.next.pack(side="right")
        elif self.pageID == 2:
            self.p3.show()
            self.prev.pack(side="left")
            self.next.pack_forget()


def setupUI(root):
    # setup window
    logger.info("Initializing view.py...")
    root.title("Cen2Xlsx")
    mainFrame = MainView(root)
    mainFrame.pack(side="top", fill="both", expand=True)
    root.wm_geometry("350x200")
    logger.info("view.py initialized successfully")


def main():
    logger.info("Started from view.py")
    root = Tk()
    setupUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# TODO: Code for dynamically size progress bar maybe?
# from tkinter import *
#
# # a subclass of Canvas for dealing with resizing of windows
# class ResizingCanvas(Canvas):
#     def __init__(self,parent,**kwargs):
#         Canvas.__init__(self,parent,**kwargs)
#         self.bind("<Configure>", self.on_resize)
#         self.height = self.winfo_reqheight()
#         self.width = self.winfo_reqwidth()
#
#     def on_resize(self,event):
#         # determine the ratio of old width/height to new width/height
#         wscale = float(event.width)/self.width
#         hscale = float(event.height)/self.height
#         self.width = event.width
#         self.height = event.height
#         # resize the canvas
#         self.config(width=self.width, height=self.height)
#         # rescale all the objects tagged with the "all" tag
#         self.scale("all",0,0,wscale,hscale)
#
# def main():
#     root = Tk()
#     myframe = Frame(root)
#     myframe.pack(fill=BOTH, expand=YES)
#     mycanvas = ResizingCanvas(myframe,width=850, height=400, bg="red", highlightthickness=0)
#     mycanvas.pack(fill=BOTH, expand=YES)
#
#     # add some widgets to the canvas
#     mycanvas.create_line(0, 0, 200, 100)
#     mycanvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
#     mycanvas.create_rectangle(50, 25, 150, 75, fill="blue")
#
#     # tag all of the drawn widgets
#     mycanvas.addtag_all("all")
#     root.mainloop()
#
# if __name__ == "__main__":
#     main()