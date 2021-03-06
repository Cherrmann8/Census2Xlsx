const { app, BrowserWindow } = require("electron");
const path = require("path");
const url = require("url");
const { ipcMain } = require("electron");
const { dialog } = require("electron");

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      webSecurity: false,
      contextIsolation: false
    },
  });
  
  if (process.env.IS_DEV === "1") {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.loadURL(
    process.env.ELECTRON_START_URL ||
    url.format({
      pathname: path.join(__dirname, '../build/index.html'),
      protocol: "file:",
      slashes: true,
    })
  );

  mainWindow.on("closed", () => {
    mainWindow = null;
  });

  mainWindow.menuBarVisible = false;
}

app.on("ready", createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// ------------------- event listeners --------------------

// temporary variable to store data while background
// process is ready to start processing
let cache = {
  reportArea: undefined,
  selectedIndicators: undefined,
  options: undefined,
};

// a window object outside the function scope prevents
// the object from being garbage collected
let hiddenWindow;

// This event listener will listen for request
// from visible renderer process
ipcMain.on("START_BACKGROUND_VIA_MAIN", (event, args) => {
  hiddenWindow = new BrowserWindow({
    // Show needs to be false for production
    show: true,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  if (process.env.IS_DEV === "1") {
    hiddenWindow.loadURL(
      url.format({
        pathname: path.join(__dirname, "/../public/hidden.html"),
        protocol: "file:",
        slashes: true,
      })
    );
  } else {
    hiddenWindow.loadURL(
      url.format({
        pathname: path.join(__dirname, "/../build/hidden.html"),
        protocol: "file:",
        slashes: true,
      })
    );
  }


  hiddenWindow.webContents.openDevTools();

  hiddenWindow.on("closed", () => {
    hiddenWindow = null;
  });

  cache.reportArea = args.reportArea;
  cache.selectedIndicators = args.selectedIndicators;
  cache.options = args.options;
  if (process.env.IS_DEV === "1") {
    cache.options["dataDir"] = path.join(__dirname, '../src/assets/data/')
  } else {
    cache.options["dataDir"] = path.join(__dirname, '../../extraResources/data/')
  }
});

ipcMain.on("BACKGROUND_READY", (event, args) => {
  event.reply("START_PROCESSING", {
    reportArea: cache.reportArea,
    selectedIndicators: cache.selectedIndicators,
    options: cache.options,
  });
});

ipcMain.on("FAKE_BACKGROUND_VIA_MAIN", (event, args) => {
  hiddenWindow = new BrowserWindow({
    show: false,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  hiddenWindow.loadURL(
    url.format({
      pathname: path.join(__dirname, "/../public/fakeHidden.html"),
      protocol: "file:",
      slashes: true,
    })
  );

  hiddenWindow.webContents.openDevTools();

  hiddenWindow.on("closed", () => {
    hiddenWindow = null;
  });
});

ipcMain.on("BACKGROUND_FAKED", (event, args) => {
  event.reply("FAKE_PROCESSING");
});

// This event listener will listen for data being sent back
// from the background renderer process
ipcMain.on("MESSAGE_FROM_BACKGROUND", (event, args) => {
  mainWindow.webContents.send("MESSAGE_FROM_BACKGROUND_VIA_MAIN", args);
});

ipcMain.on("RETRY_SAVE", (event, args) => {
  hiddenWindow.webContents.send("RETRY_SAVE", args);
});

ipcMain.on("GET_WINDOW_COUNT", (event, args) => {
  const c = BrowserWindow.getAllWindows();
  event.reply("RETURN_WINDOW_COUNT", {
    count: c,
  });
});

ipcMain.on("START_DIALOG", (event, args) => {
  let options = {
    title: "Choose a directory to save to",
    defaultPath : app.getPath("downloads"),
    buttonLabel : "Open directory",
    properties :[
      "openDirectory",
      "createDirectory",
    ]
  }
  const filePath = dialog.showOpenDialogSync(options);
  event.reply("RETURN_DIALOG", {
    filePath: filePath,
  });
});

ipcMain.on("GET_DOWNLOADS_PATH", (event, args) => {
  const downloadsPath = app.getPath("downloads");
  event.reply("RETURN_DOWNLOADS_PATH", {
    downloadsPath: downloadsPath,
  });
});
