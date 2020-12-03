import model
import logging
import json
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

"""
Author: Charles Herrmann
Date: 12/2/2020
Description: GUI for Census2xlsx application
"""

logging.basicConfig(filename='c2x.log', filemode='w', level=logging.INFO)
logger = logging.getLogger('view')


"""
class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

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
        "Place Level"
    ]

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        # Load all the geographic data (all states, counties, and places)
        self.loadGeos()

        # Init and add the geographies box to the page
        self.geoFrame = Frame(self, borderwidth=2, relief=GROOVE)
        self.levelVar = StringVar(self.geoFrame)
        self.levelVar.set(self.geoLevels[0])
        self.levelMenu = OptionMenu(self.geoFrame, self.levelVar, *self.geoLevels)
        self.levelVar.trace("w", self.levelMenuEvent)
        self.label1 = Label(self.geoFrame, text="Select a State")
        self.label2 = Label(self.geoFrame, text="Select a County")
        self.label3 = Label(self.geoFrame, text="Select a Place")
        self.listbox1 = Listbox(self.geoFrame, borderwidth=2, relief=GROOVE)
        self.listbox2 = Listbox(self.geoFrame, borderwidth=2, relief=GROOVE)
        # self.listbox1.bind('<Button-1>', self.stateMenuEvent)
        # self.listbox1.bind('<Double-1>', self.stateMenuEvent)
        self.geoFrame.pack(side='left', fill='both', expand=True)
        self.levelMenu.pack(side="top", fill="x", expand=False)

        for state in self.geos.keys():
            self.listbox1.insert(END, state)

        buttonFrame = Frame(self)
        add = Button(buttonFrame, text="Add", command=self.addButton)
        remove = Button(buttonFrame, text="Remove", command=self.removeButton)
        buttonFrame.pack(side='left', fill='x', expand=False)
        add.pack(side="top", fill="x", expand=False)
        remove.pack(side="bottom", fill="x", expand=False)

        # Init and add the selection box to the page
        selectionFrame = Frame(self, borderwidth=2, relief=GROOVE)
        label4 = Label(selectionFrame, text="Report Area", anchor='center')
        self.listbox3 = Listbox(selectionFrame, borderwidth=1, relief=GROOVE)
        selectionFrame.pack(side='left', fill='both', expand=True)
        label4.pack(side="top", fill="x", expand=False)
        self.listbox3.pack(side='bottom', fill='both', expand=True)

    def loadGeos(self):
        logger.info("Loading geographies.json")
        with open('geographies.json', 'r') as loadfile:
            self.geos = json.load(loadfile)
        logger.info("geographies.json loaded")

    def stateSelected(self, *args):
        self.label1.config(text=self.listbox1.get(self.listbox1.curselection()[0]))
        self.listbox1.pack_forget()
        self.listbox2.pack(side='top', fill='both', expand=True)
        self.fillListBox2()

    def levelMenuEvent(self, *args):
        newLevelID = -1

        if self.levelVar.get() == self.geoLevels[1]:
            newLevelID = 0
        elif self.levelVar.get() == self.geoLevels[2]:
            newLevelID = 1
        elif self.levelVar.get() == self.geoLevels[3]:
            newLevelID = 2
        else:
            logger.error("GeoPage optMenu has invalid state")

        if newLevelID != -1:
            if newLevelID != self.levelID:
                self.levelID = newLevelID
                self.label1.pack_forget()
                self.label2.pack_forget()
                self.label3.pack_forget()
                self.listbox1.pack_forget()
                self.listbox2.pack_forget()
                if self.levelID == 0:
                    self.resetState()
                    self.listbox1.unbind('<Double-1>')
                elif self.levelID == 1:
                    self.resetState()
                    self.listbox1.bind('<Double-1>', self.stateSelected)
                    self.label2.pack(side="top", fill="x", expand=False)
                elif self.levelID == 2:
                    self.resetState()
                    self.listbox1.bind('<Double-1>', self.stateSelected)
                    self.label3.pack(side="top", fill="x", expand=False)
        else:
            print("ERROR: GeoPage has invalid levelID")

    # Fills either the counties or places list boxes
    def fillListBox2(self):
        # Empty listbox2 of any elements
        self.listbox2.delete(0, END)
        # Fill in the counties for the chosen state
        if self.levelID == 1:
            for county in self.geos[self.label1.cget('text')]['Counties']:
                self.listbox2.insert(END, county)
        # Fill in the places for the chosen state
        elif self.levelID == 2:
            for county in self.geos[self.label1.cget('text')]['Places']:
                self.listbox2.insert(END, county)

    # Reset the State Label and show listbox1
    def resetState(self):
        self.label1.config(text='Select a State')
        self.label1.pack(side="top", fill="x", expand=False)
        self.listbox1.pack(side='top', fill='both', expand=True)

    # Adds the selected state, county, or place to the
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
            self.listbox3.insert(END, geo)
            if self.levelID == 0:
                if geo not in self.selectedGeos:
                    self.selectedGeos[geo] = {}
                self.selectedGeos[geo]['ID'] = self.geos[geo]['ID']
                self.selectedGeos[geo]['selected'] = True
            elif self.levelID == 1:
                if self.label1.cget('text') not in self.selectedGeos:
                    self.selectedGeos[self.label1.cget('text')] = {}
                    self.selectedGeos[self.label1.cget('text')]['ID'] = self.geos[self.label1.cget('text')]['ID']
                    self.selectedGeos[self.label1.cget('text')]['selected'] = False
                if 'Counties' not in self.selectedGeos[self.label1.cget('text')]:
                    self.selectedGeos[self.label1.cget('text')]['Counties'] = {}
                self.selectedGeos[self.label1.cget('text')]['Counties'][geo] = self.geos[self.label1.cget('text')]['Counties'][geo]
            elif self.levelID == 2:
                if self.label1.cget('text') not in self.selectedGeos:
                    self.selectedGeos[self.label1.cget('text')] = {}
                    self.selectedGeos[self.label1.cget('text')]['ID'] = self.geos[self.label1.cget('text')]['ID']
                    self.selectedGeos[self.label1.cget('text')]['selected'] = False
                if 'Places' not in self.selectedGeos[self.label1.cget('text')]:
                    self.selectedGeos[self.label1.cget('text')]['Places'] = {}
                self.selectedGeos[self.label1.cget('text')]['Places'][geo] = self.geos[self.label1.cget('text')]['Places'][geo]

    def removeButton(self):
        print(self.selectedGeos)

    def getGeoCount(self):
        return self.listbox3.size()

    def getGeos(self):
        return self.selectedGeos


class TablePage(Page):
    desc = {}

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.loadTableDesc()

        # Init all widgets
        self.dtsFrame = Frame(self)
        self.canvas = Canvas(self.dtsFrame)
        self.scrollbar = Scrollbar(self.dtsFrame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Init all dtCheckboxes
        self.checkVars = []
        self.checkBoxes = []
        self.checkVars.append(IntVar())
        checkBox = Checkbutton(self.scrollable_frame, text='Select all tables', variable=self.checkVars[len(self.checkVars)-1], command=self.selectAll)
        self.checkBoxes.append(checkBox)
        for key in self.desc.keys():
            self.checkVars.append(IntVar())
            checkBox = Checkbutton(self.scrollable_frame, text=key, variable=self.checkVars[len(self.checkVars)-1])
            self.checkBoxes.append(checkBox)

        # Pack all widgets
        self.dtsFrame.pack(side='bottom', fill='both', expand=True)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Pack all dtCheckboxes
        for checkBox in self.checkBoxes:
            checkBox.pack(side='top', fill='both', expand=True)

    def loadTableDesc(self):
        logger.info("Loading dataTableDescriptions.json")
        with open('dataTableDescriptions.json', 'r') as loadfile:
            self.desc = json.load(loadfile)
        logger.info("dataTableDescriptions.json loaded")

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
        self.geoCountLabel = Label(self.confFrame, text='0 locations in Report Area', anchor='center')
        self.tableCountLabel = Label(self.confFrame, text='0 Data Tables included in Report', anchor='center')
        self.fileNameFrame = Frame(self.confFrame)
        self.fileNameLabel = Label(self.fileNameFrame, text='Enter a file name:', anchor='e')
        self.fileNameEntry = Entry(self.fileNameFrame, justify='right')
        self.fileNameEntry.insert(0, 'Generated_Databook')
        self.fileNameExtensionLabel = Label(self.fileNameFrame, text='.xlsx', anchor='w')

        # Pack all widgets
        self.confFrame.pack(side='left', fill='both', expand=True)
        self.geoCountLabel.pack(side='top', fill='x', expand=False)
        self.tableCountLabel.pack(side='top', fill='x', expand=False)
        self.fileNameFrame.pack(side='top', fill='x', expand=False)
        self.fileNameLabel.pack(side='left', fill='x', expand=True)
        self.fileNameEntry.pack(side='left', fill='x', expand=False)
        self.fileNameExtensionLabel.pack(side='left', fill='x', expand=True)

    def updateSelection(self, gCount, tCount):
        self.geoCountLabel.config(text=str(gCount)+' locations in Report Area')
        self.tableCountLabel.config(text=str(tCount)+' Data Tables included in Report')


class MainView(Frame):
    pageID = 0
    steps = ["Step 1 of 3: Create your Report Area",
             "Step 2 of 3: Add Data Tables to your Databook",
             "Step 3 of 3: Confirm your selection"]
    cmodel = model.CensusModel()

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
        self.label3 = Label(progressFrame, text=self.steps[0])

        progressFrame.pack(side="top", fill="x", expand=False)
        self.label3.pack(side="top", anchor='center')

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
        self.gen = Button(buttonFrame, text="Generate", command=self.generate)

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
        self.next.pack_forget()
        self.prev.pack_forget()
        self.gen.pack_forget()

        if self.pageID == 0:
            self.next.pack(side="right")
            self.p1.show()
        elif self.pageID == 1:
            self.prev.pack(side="left")
            self.next.pack(side="right")
            self.p2.show()
        elif self.pageID == 2:
            self.p3.updateSelection(self.p1.getGeoCount(), self.p2.getTableCount())
            self.prev.pack(side="left")
            self.gen.pack(side="right")
            self.p3.show()
        self.label3.config(text=self.steps[self.pageID])

    def generate(self):
        self.cmodel.genData(self.p1.getGeos(), None, 'Databook.xlsx')
        
def setupUI(root):
    # setup window
    logger.info("Initializing view.py...")
    root.title("Cen2Xlsx")
    mainFrame = MainView(root)
    mainFrame.pack(side="top", fill="both", expand=True)
    root.wm_geometry("500x300")
    logger.info("view.py initialized successfully")
"""

class TestApp(App):
    def build(self):
        sm = ScreenManager()

        # Add few screens
        for i in range(4):
            screen = Screen(name='Title %d' % i)
            sm.add_widget(screen)
        layout = BoxLayout(orientation='vertical')
        btn1 = Button(text='Hello')
        btn2 = Button(text='World')
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        return sm


def main():
    logger.info("Started from view.py")
    TestApp().run()


if __name__ == "__main__":
    main()

