const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 1000,
        height: 700,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true
        },
        // Make the window look more modern
        frame: false,
        transparent: false,
        resizable: false,
        fullscreenable: false
    });

    win.loadFile('index.html');
    
    // Uncomment to open DevTools during development
    // win.webContents.openDevTools();
}

app.whenReady().then(createWindow);

ipcMain.on('app-quit', () => {
    app.quit();
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
