import os
import PyQt5
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = (
    os.path.join(os.path.dirname(PyQt5.__file__), "Qt5", "plugins", "platforms")
)

import sys
from PyQt5 import QtWidgets
from views.frmGiris import frmGiris

def run():
    print("Program Çalıştırıldı...")
    qt_app = QtWidgets.QApplication(sys.argv)
    window = frmGiris()
    window.show()
    sys.exit(qt_app.exec_())

if __name__ == "__main__":
    run()

input("programdan çıkmak için ENTER'a")