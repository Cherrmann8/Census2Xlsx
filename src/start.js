const { app, BrowserWindow } = require('electron')
const path = require('path')
const url = require('url')
const { PythonShell } = require('python-shell');
const { ipcMain } = require('electron')

let mainWindow

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
  })

  mainWindow.loadURL(
    process.env.ELECTRON_START_URL ||
      url.format({
        pathname: path.join(__dirname, '/../public/index.html'),
        protocol: 'file:',
        slashes: true,
      })
  )

  mainWindow.on('closed', () => {
    mainWindow = null
  })

  mainWindow.menuBarVisible = false
  mainWindow.webContents.openDevTools();
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

// ------------------- event listeners --------------------

// temporary variable to store data while background
// process is ready to start processing
let cache = {
	data: undefined,
}

// a window object outside the function scope prevents
// the object from being garbage collected
let hiddenWindow

// This event listener will listen for request
// from visible renderer process
ipcMain.on('START_BACKGROUND_VIA_MAIN', (event, args) => {
	hiddenWindow = new BrowserWindow({
		show: false,
		webPreferences: {
			nodeIntegration: true,
		},
	})

	hiddenWindow.loadURL(
      url.format({
        pathname: path.join(__dirname, '/../public/hidden.html'),
        protocol: 'file:',
        slashes: true,
      }))

	hiddenWindow.webContents.openDevTools()

	hiddenWindow.on('closed', () => {
		hiddenWindow = null
	})

	cache.data = args.number

  event.reply('report', 'finished setting up hidden.html')
})

// This event listener will listen for data being sent back
// from the background renderer process
ipcMain.on('MESSAGE_FROM_BACKGROUND', (event, args) => {
	mainWindow.webContents.send('MESSAGE_FROM_BACKGROUND_VIA_MAIN', args.message)
})

ipcMain.on('BACKGROUND_READY', (event, args) => {

	event.reply('START_PROCESSING', {
		data: cache.data,
	})

  mainWindow.webContents.send('report', 'hidden.html is ready to start processing data')
})

// console.log('hi from start.js')
// let pyshell = new PythonShell(path.join(__dirname, '/scripts/testing.py'), {
//   pythonPath: 'python3',
// })

// pyshell.on('message', function(results) {
//   console.log(`MESSAGE_FROM_BACKGROUND ${results}`)
// })

// ipcMain.on('asynchronous-message', (event, arg) => {
//   if (arg === '0') {
//     event.reply('asynchronous-reply', 'got 0')
//   } else if (arg === '1') {
//     event.reply('asynchronous-reply', 'got 1')
//   }
// })