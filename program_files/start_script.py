import sys
import os

# setting new system path to be able to refer to parent directories
parent = os.path.abspath('..')
sys.path.insert(1, parent)

import subprocess as sp
import matplotlib.pyplot as plt
import streamlit
import atexit
import matplotlib
from program_files.GUI_st import GUI_st_global_functions
from streamlit.web import cli as stcli
from pathlib import Path
from PySide6 import QtCore, QtWebEngineWidgets, QtWidgets


# Set environment variables for frozen macOS applications using Qt WebEngine
if getattr(sys, 'frozen', False) and sys.platform == 'darwin':
    # Set the path for Qt WebEngine resources
    os.environ["QTWEBENGINE_RESOURCES_PATH"] = str(Path(sys._MEIPASS))
    # Set the path for Qt WebEngine locales
    os.environ["QTWEBENGINE_LOCALES_PATH"] = \
        str(Path(sys._MEIPASS)) + "/qtwebengine_locales"


def kill_server(p):
    """
    Terminate a subprocess depending on the operating system.

    This function is responsible for terminating a subprocess based on the
    operating system. It uses different methods for Windows and POSIX systems.

    :param p: process which will be killed
    :type p: subprocess.Popen
    """
    if os.name == 'nt':
        # Terminate the subprocess using taskkill for Windows
        sp.call(['taskkill', '/F', '/T', '/PID', str(p.pid)])
    elif os.name == 'posix':
        # Terminate the subprocess using the kill method for POSIX systems
        p.kill()
    else:
        # For other operating systems, do nothing
        pass


if __name__ == '__main__':
    # Set environment variable to enable Qt WebEngine debugging
    os.environ["QT_LOGGING_TO_CONSOLE"] = "1"

    # Configure Matplotlib to use Qt backend for rendering
    matplotlib.use("QtAgg")
    plt.rcParams['figure.hooks'].append('mplcvd:setup')

    # Determine the bundle directory based on frozen or non-frozen state
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = Path(sys._MEIPASS)
    else:
        bundle_dir = Path(__file__).parent.parent

    # Define the command to run the Streamlit application
    cmd = [
        "streamlit",
        "run",
        str(bundle_dir) + "/program_files/GUI_st/1_Main_Application.py",
        "--server.headless=True",
        "--global.developmentMode=False"
    ]

    # Start the Streamlit subprocess and register termination function
    p = sp.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    atexit.register(kill_server, p)

    # Set the hostname and port for the Qt WebEngineView
    hostname = 'localhost'
    port = 8501

    # Initialize a Qt application and WebEngineView
    app = QtWidgets.QApplication()
    view = QtWebEngineWidgets.QWebEngineView()

    # Load and show the Streamlit app in the WebEngineView
    view.load(QtCore.QUrl(f'http://{hostname}:{port}'))
    view.show()

    # Start the Qt application event loop
    app.exec()
