"""
Author: Charles Herrmann
Date: 9/28/20
Description: Prototype GUI for Census2xlsx application
"""

import getopt
import logging
import json
import threading
import queue
import time
from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkfont
import census2xlsx

windowSize = "600x400"


class Generator(threading.Thread):
    def __init__(self, lock, monitorQueue, logger, dirs, geos, indicators, filename):
        threading.Thread.__init__(self)
        self.lock = lock
        self.monitorQueue = monitorQueue
        self.logger = logger
        self.cmodel = model.CensusModel(dirs[0], dirs[1], dirs[2])
        self.geos = geos
        self.indicators = indicators
        self.filename = filename

    def run(self):
        if self.logger:
            self.logger.info(str(time.time()) + " Thread Starting")

        self.lock.acquire()
        self.monitorQueue.put(40)
        self.lock.release()

        self.cmodel.gen_data(self.geos, self.indicators, self.filename + ".xlsx")

        self.lock.acquire()
        self.monitorQueue.put(20)
        self.lock.release()

        time.sleep(0.8)

        if self.logger:
            self.logger.info(str(time.time()) + " Thread Sending")

        self.lock.acquire()
        self.monitorQueue.put(40)
        self.lock.release()

        if self.logger:
            self.logger.info(str(time.time()) + " Thread Done")


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self)

    def show(self):
        self.lift()


class GeoPage(Page):
    geos = {}
    selectedGeos = {}
    levelID = -1
    geoLevels = [
        "Select a Geographic Level",
        "State Level",
        "County Level",
        "Place Level",
    ]

    def __init__(self, *args, **kwargs):
        Page.__init__(self, args, kwargs)
        # Load all the geographic data (all states, counties, and places)
        self.loadGeos(args[0])

        # Init and add the geographies box to the page
        self.geoFrame = Frame(self, borderwidth=2, relief=GROOVE)
        self.levelVar = StringVar(self.geoFrame)
        self.levelVar.set(self.geoLevels[0])
        self.levelMenu = OptionMenu(self.geoFrame, self.levelVar, *self.geoLevels)
        self.levelVar.trace("w", self.levelMenuEvent)
        # self.stateFrame = Frame(self.geoFrame)
        self.label1 = Label(self.geoFrame, text="")
        # self.resetLabel1 = Button(self.stateFrame, text="reset")
        self.label2 = Label(self.geoFrame, text="")
        self.listbox1 = Listbox(self.geoFrame, borderwidth=2, relief=GROOVE)
        self.listbox2 = Listbox(self.geoFrame, borderwidth=2, relief=GROOVE)
        self.listbox1.bind("<Double-1>", self.l1double)
        # self.listbox1.bind('<Button-1>', self.stateMenuEvent)
        # self.listbox1.bind('<Double-1>', self.stateMenuEvent)
        self.geoFrame.pack(side="left", fill="both", expand=True)
        self.levelMenu.pack(side="top", fill="x", expand=False)

        for state in self.geos.keys():
            self.listbox1.insert(END, state)

        buttonFrame = Frame(self)
        add = Button(buttonFrame, text="Add", command=self.addButton)
        remove = Button(buttonFrame, text="Remove", command=self.removeButton)
        buttonFrame.pack(side="left", fill="x", expand=False)
        add.pack(side="top", fill="x", expand=False)
        remove.pack(side="bottom", fill="x", expand=False)

        # Init and add the selection box to the page
        selectionFrame = Frame(self, borderwidth=2, relief=GROOVE)
        label4 = Label(selectionFrame, text="Report Area", anchor="center")
        self.listbox3 = Listbox(selectionFrame, borderwidth=1, relief=GROOVE)
        selectionFrame.pack(side="left", fill="both", expand=True)
        label4.pack(side="top", fill="x", expand=False)
        self.listbox3.pack(side="bottom", fill="both", expand=True)

    def loadGeos(self, parent):
        # logger.info("Loading geographies.json")
        # with open(parent.getDir(0) + "/geographies.json", "r") as loadfile:
        with open(
            parent.getDir(0) + "./src/assets/data/geographies.json", "r"
        ) as loadfile:
            self.geos = json.load(loadfile)
        # logger.info("geographies.json loaded")

    def l1double(self, *args):
        if self.levelID == 0:
            selection = self.listbox1.curselection()
            if len(selection) > 0:
                geo = self.listbox1.get(selection[0])
                self.addGeo(geo)
        elif self.levelID > 0:
            self.stateSelected(args)

    def stateSelected(self, *args):
        self.label1.config(text=self.listbox1.get(self.listbox1.curselection()[0]))
        self.listbox1.pack_forget()
        # self.resetLabel1.pack()
        self.label2.pack(side="top", fill="x", expand=False)
        self.listbox2.pack(side="top", fill="both", expand=True)
        self.fillListBox2()

    def levelMenuEvent(self, *args):
        newLevelID = -1

        if self.levelVar.get() == self.geoLevels[1]:
            newLevelID = 0
        elif self.levelVar.get() == self.geoLevels[2]:
            newLevelID = 1
        elif self.levelVar.get() == self.geoLevels[3]:
            newLevelID = 2
        # else:
        # logger.error("GeoPage optMenu has invalid state")

        if newLevelID != -1:
            if newLevelID != self.levelID:
                self.levelID = newLevelID
                # TODO: bring stateFrame back
                # self.stateFrame.pack_forget()
                # self.resetLabel1.pack_forget()
                self.label1.pack_forget()
                self.label2.pack_forget()
                self.listbox1.pack_forget()
                self.listbox2.pack_forget()
                if self.levelID == 0:
                    self.resetState()
                elif self.levelID == 1:
                    self.resetState()
                    self.label2.config(text="Select a County")
                elif self.levelID == 2:
                    self.resetState()
                    self.label2.config(text="Select a Place")
        else:
            print("ERROR: GeoPage has invalid levelID")

    """Fills either the counties or places list boxes"""

    def fillListBox2(self):
        # Fill in the counties for the chosen state
        if self.levelID == 1:
            for county in self.geos[self.label1.cget("text")]["Counties"]:
                self.listbox2.insert(END, county)
        # Fill in the places for the chosen state
        elif self.levelID == 2:
            for county in self.geos[self.label1.cget("text")]["Places"]:
                self.listbox2.insert(END, county)

    """Reset the State Label and show listbox1"""

    def resetState(self):
        self.label1.config(text="Select a State")
        self.label1.pack(side="top", fill="x", expand=False)
        # self.stateFrame.pack(side="top", fill="x", expand=False)
        self.listbox1.pack(side="top", fill="both", expand=True)
        # Empty listbox2 of any elements
        self.listbox2.delete(0, END)

    def addGeo(self, geo):
        if self.levelID == 0:
            if geo not in self.selectedGeos:
                self.selectedGeos[geo] = {}
                self.listbox3.insert(END, geo)
            self.selectedGeos[geo]["ID"] = self.geos[geo]["ID"]
            self.selectedGeos[geo]["selected"] = True
        elif self.levelID == 1:
            if self.label1.cget("text") not in self.selectedGeos:
                self.selectedGeos[self.label1.cget("text")] = {}
                self.selectedGeos[self.label1.cget("text")]["ID"] = self.geos[
                    self.label1.cget("text")
                ]["ID"]
                self.selectedGeos[self.label1.cget("text")]["selected"] = False
            if "Counties" not in self.selectedGeos[self.label1.cget("text")]:
                self.selectedGeos[self.label1.cget("text")]["Counties"] = {}
            if geo not in self.selectedGeos[self.label1.cget("text")]["Counties"]:
                self.listbox3.insert(END, geo)
                self.selectedGeos[self.label1.cget("text")]["Counties"][
                    geo
                ] = self.geos[self.label1.cget("text")]["Counties"][geo]
        elif self.levelID == 2:
            if self.label1.cget("text") not in self.selectedGeos:
                self.selectedGeos[self.label1.cget("text")] = {}
                self.selectedGeos[self.label1.cget("text")]["ID"] = self.geos[
                    self.label1.cget("text")
                ]["ID"]
                self.selectedGeos[self.label1.cget("text")]["selected"] = False
            if "Places" not in self.selectedGeos[self.label1.cget("text")]:
                self.selectedGeos[self.label1.cget("text")]["Places"] = {}
            if geo not in self.selectedGeos[self.label1.cget("text")]["Places"]:
                self.listbox3.insert(END, geo)
                self.selectedGeos[self.label1.cget("text")]["Places"][geo] = self.geos[
                    self.label1.cget("text")
                ]["Places"][geo]

    """Adds the selected state, county, or place to the selected list of geos"""

    def addButton(self):
        if self.levelID == 0:
            selection = self.listbox1.curselection()
        else:
            selection = self.listbox2.curselection()
        if len(selection) > 0:
            if self.levelID == 0:
                geo = self.listbox1.get(selection[0])
            else:
                geo = self.listbox2.get(selection[0])
            self.addGeo(geo)

    def removeButton(self):
        selection = self.listbox3.curselection()
        if len(selection) > 0:
            geo = self.listbox3.get(selection[0])
            for i in range(self.listbox3.size()):
                if self.listbox3.get(i) == geo:
                    self.listbox3.delete(i)
            # self.listbox3.delete()

    def getGeoCount(self):
        return self.listbox3.size()

    def getGeos(self):
        return self.selectedGeos


class TablePage(Page):
    desc = {}

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.loadTableDesc(args[0])

        # Init all widgets
        self.dtsFrame = Frame(self)
        self.canvas = Canvas(self.dtsFrame)
        self.scrollbar = Scrollbar(
            self.dtsFrame, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Init all dtCheckboxes
        self.checkVars = []
        self.checkBoxes = []
        self.checkVars.append(IntVar())
        checkBox = Checkbutton(
            self.scrollable_frame,
            text="Select all tables",
            variable=self.checkVars[len(self.checkVars) - 1],
            command=self.selectAll,
        )
        self.checkBoxes.append(checkBox)
        for key in self.desc.keys():
            self.checkVars.append(IntVar())
            checkBox = Checkbutton(
                self.scrollable_frame,
                text=key,
                variable=self.checkVars[len(self.checkVars) - 1],
            )
            self.checkBoxes.append(checkBox)

        # Pack all widgets
        self.dtsFrame.pack(side="bottom", fill="both", expand=True)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Pack all dtCheckboxes
        for checkBox in self.checkBoxes:
            checkBox.pack(side="top", fill="both", expand=True)

    def loadTableDesc(self, parent):
        # logger.info("Loading dataTableDescriptions.json")
        with open(parent.getDir(0) + "/dataTableDescriptions.json", "r") as loadfile:
            self.desc = json.load(loadfile)
        # logger.info("dataTableDescriptions.json loaded")

    def selectAll(self):
        state = 0
        if self.checkVars[0].get() == 1:
            state = 1
        for i in range(1, len(self.checkVars)):
            self.checkVars[i].set(state)

    def getTableCount(self):
        count = 0
        for i in range(1, len(self.checkVars)):
            if self.checkVars[i].get() == 1:
                count += 1
        return count


class ConfPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Init all widgets
        self.confFrame = Frame(self)
        self.geoCountLabel = Label(
            self.confFrame, text="0 locations in Report Area", anchor="center"
        )
        self.tableCountLabel = Label(
            self.confFrame, text="0 Data Tables included in Report", anchor="center"
        )
        self.fileNameFrame = Frame(self.confFrame)
        self.fileNameLabel = Label(
            self.fileNameFrame, text="Enter a file name:", anchor="e"
        )
        self.fileNameEntry = Entry(self.fileNameFrame, justify="right")
        self.fileNameEntry.insert(0, "Databook")
        self.fileNameExtensionLabel = Label(
            self.fileNameFrame, text=".xlsx", anchor="w"
        )

        # Pack all widgets
        self.confFrame.pack(side="left", fill="both", expand=True)
        self.geoCountLabel.pack(side="top", fill="x", expand=False)
        self.tableCountLabel.pack(side="top", fill="x", expand=False)
        self.fileNameFrame.pack(side="top", fill="x", expand=False)
        self.fileNameLabel.pack(side="left", fill="x", expand=True)
        self.fileNameEntry.pack(side="left", fill="x", expand=False)
        self.fileNameExtensionLabel.pack(side="left", fill="x", expand=True)

    def updateSelection(self, gCount, tCount):
        self.geoCountLabel.config(text=str(gCount) + " locations in Report Area")
        self.tableCountLabel.config(
            text=str(tCount) + " Data Tables included in Report"
        )

    def getFileName(self):
        return self.fileNameEntry.get()


class GenPage(Page):
    exit_flag = False
    monitor_lock = None
    monitor_queue = None

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.parent = args[0]
        self.logger = args[1]

        # Init all widgets
        self.genFrame = Frame(self)
        self.centerFrame = Frame(self.genFrame)

        self.pageNum = Label(
            self.centerFrame, text="Generating your file...", anchor="center"
        )
        self.progress = Progressbar(
            self.centerFrame, orient=HORIZONTAL, length=500, mode="determinate"
        )

        # Pack all widgets
        self.genFrame.pack(side="left", fill="both", expand=True)
        self.centerFrame.pack(side="left", fill="x", expand=True, anchor="center")
        self.pageNum.pack(side="top", fill="both", expand=True)
        self.progress.pack(side="top", expand=False, anchor="s")

    def generate(self, dirs, geos, indicators, filename):
        self.exit_flag = False
        self.monitor_lock = threading.Lock()
        self.monitor_queue = queue.Queue(5)
        if self.logger:
            self.logger.info(str(time.time()) + " Main starting thread")
        Generator(
            self.monitor_lock,
            self.monitor_queue,
            self.logger,
            dirs,
            geos,
            indicators,
            filename,
        ).start()

    def check(self):
        if self.logger:
            self.logger.info(str(time.time()) + " Main loop")
        self.monitor_lock.acquire()
        if not self.monitor_queue.empty():
            if self.logger:
                self.logger.info(str(time.time()) + " Main got message")
            self.progress["value"] += self.monitor_queue.get()
            if self.progress["value"] >= 100:
                self.exit_flag = True
        self.monitor_lock.release()

        if not self.exit_flag:
            self.after(100, self.check)
        else:
            if self.logger:
                self.logger.info(str(time.time()) + " Main done")
            self.parent.nextPage()


class FinalPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Init all widgets
        self.finalFrame = Frame(self)
        self.pageNum = Label(
            self.finalFrame,
            text="Your report was generated successfully!",
            anchor="center",
        )

        # Pack all widgets
        self.finalFrame.pack(side="left", fill="both", expand=True)
        self.pageNum.pack(fill="both", expand=True)


class MainView(Frame):
    pageID = 0
    steps = [
        "Step 1 of 3: Create your Report Area",
        "Step 2 of 3: Add Data Tables to your Databook",
        "Step 3 of 3: Confirm your selection",
    ]

    def __init__(self, logger, data_dir, log_dir, out_dir):
        super(MainView, self).__init__()
        self.logger = logger
        self.dirs = (data_dir, log_dir, out_dir)

        header_font = tkfont.Font(family="Lucida Grande", size=14)
        label_font = tkfont.Font(family="Lucida Grande", size=10)

        # INIT ALL WIDGETS

        # Header Frame - Contains app name and settings button
        headerFrame = Frame(self)
        label1 = Label(headerFrame, text="Census2Xlsx", font=header_font)
        # TODO: Change this to picture of gear
        label2 = Label(headerFrame, text="Settings", font=header_font)

        # Progress Frame - Contains images showing progression of user
        self.progressFrame = Frame(self)
        self.label3 = Label(self.progressFrame, text=self.steps[0], font=label_font)

        # Pages Frame - Contains each page of the application
        self.pagesFrame = Frame(self)
        self.p1 = GeoPage(self)
        self.p2 = TablePage(self)
        self.p3 = ConfPage(self)
        self.p4 = GenPage(self, logger, ())
        self.p5 = FinalPage(self)

        # Navigation Frame - Contains the next, back, and generate buttons
        self.navigationFrame = Frame(self)
        self.next = Button(self.navigationFrame, text="Next", command=self.nextPage)
        self.prev = Button(self.navigationFrame, text="Back", command=self.lastPage)

        # PACK ALL WIDGETS

        # Header Frame (All other frames get packed in show())
        headerFrame.pack(
            side="top", fill="x", expand=False, padx=(10, 10), pady=(10, 0)
        )
        label1.pack(side="left")
        label2.pack(side="right")

        # Progress Frame
        self.label3.pack(side="top", anchor="center")

        # Pages Frame
        self.p1.place(in_=self.pagesFrame, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=self.pagesFrame, x=0, y=0, relwidth=1, relheight=1)
        self.p3.place(in_=self.pagesFrame, x=0, y=0, relwidth=1, relheight=1)
        self.p4.place(in_=self.pagesFrame, x=0, y=0, relwidth=1, relheight=1)
        self.p5.place(in_=self.pagesFrame, x=0, y=0, relwidth=1, relheight=1)

        # display the GUI to the user
        self.show()

    def nextPage(self):
        if self.pageID < 4:
            self.pageID += 1
            self.show()
        else:
            self.pageID = 0
            self.show()

    def lastPage(self):
        if self.pageID > 0:
            self.pageID -= 1
            self.show()

    def show(self):
        """
        show updates the apps UI when the user goes to a new page
        """

        # unpack all frames under header
        self.progressFrame.pack_forget()
        self.pagesFrame.pack_forget()
        self.navigationFrame.pack_forget()

        # only pack progressFrame if on first 3 pages
        if self.pageID <= 2:
            self.progressFrame.pack(
                side="top", fill="x", expand=False, padx=(10, 10), pady=(0, 5)
            )
            self.label3.config(text=self.steps[self.pageID])
            self.pagesFrame.pack(
                side="top", fill="both", expand=True, padx=(10, 10), pady=(5, 5)
            )
            self.navigationFrame.pack(
                side="bottom", fill="x", expand=False, padx=(10, 10), pady=(5, 10)
            )
        else:
            self.pagesFrame.pack(
                side="top", fill="both", expand=True, padx=(10, 10), pady=(5, 5)
            )
            self.navigationFrame.pack(
                side="bottom", fill="x", expand=False, padx=(10, 10), pady=(5, 10)
            )

        # unpack buttons in navigationFrame
        self.next.pack_forget()
        self.prev.pack_forget()

        # add navigationFrame buttons depending on pageID
        if self.pageID == 0:
            self.next.config(text="Next")
            self.next.pack(side="right")
            self.p1.show()
        elif self.pageID == 1:
            self.next.config(text="Next")
            self.prev.pack(side="left")
            self.next.pack(side="right")
            self.p2.show()
        elif self.pageID == 2:
            self.p3.updateSelection(self.p1.getGeoCount(), self.p2.getTableCount())
            self.next.config(text="Generate")
            self.prev.pack(side="left")
            self.next.pack(side="right")
            self.p3.show()
        elif self.pageID == 3:
            self.p4.show()
            self.p4.generate(self.dirs, self.p1.getGeos(), None, self.p3.getFileName())
            if self.logger:
                self.logger.info(str(time.time()) + " Main looping...")
            self.p4.check()
        elif self.pageID == 4:
            self.next.config(text="New Report")
            self.next.pack(side="right")
            self.p5.show()

    def getDir(self, dirType):
        return self.dirs[dirType]

    def getDirs(self):
        return self.dirs


def main(data_dir, log_dir="", out_dir="."):
    logger = None
    # if a log_dir was given, log to that dir. Otherwise, no logging
    if log_dir != "":
        logging.basicConfig(
            filename=log_dir + "/c2x.log", filemode="w", level=logging.INFO
        )
        logger = logging.getLogger("view")

    if logger and data_dir == "data":
        logger.info("Running bundled pyinstaller application")
        print("omg")

    # setup window
    if logger:
        logger.info("Initializing view.py...")

    root = Tk()
    root.title("C2X")
    root.iconbitmap("./src/assets/icon2.ico")
    mainFrame = MainView(logger, data_dir, log_dir, out_dir)
    mainFrame.pack(side="top", fill="both", expand=True)
    root.wm_geometry(windowSize)

    if logger:
        logger.info("view.py initialized successfully")

    # run the Tkinter GUI
    root.mainloop()


if __name__ == "__main__":
    DAT_DIR = ""
    LOG_DIR = ""
    OUT_DIR = ""

    # check how this program was executed
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # executed as a PyInstaller bundle
        DAT_DIR = "../assets/data"
        LOG_DIR = "."
        OUT_DIR = "."
    else:
        # execute as a normal python process
        try:
            opts, args = getopt.getopt(
                sys.argv[1:], "hd:l:o:", ["ddir=", "ldir=", "odir="]
            )
        except getopt.GetoptError:
            print("view.py -d <data_dir> -l <logDir> -o <outputDir>")
            sys.exit(2)
        for opt, arg in opts:
            if opt == "-h":
                print("view.py -d <data_dir> -l <logDir> -o <outputDir>")
                sys.exit()
            elif opt in "-d":
                DAT_DIR = arg
            elif opt in "-l":
                LOG_DIR = arg
            elif opt in "-o":
                OUT_DIR = arg

    main(DAT_DIR, LOG_DIR, OUT_DIR)
