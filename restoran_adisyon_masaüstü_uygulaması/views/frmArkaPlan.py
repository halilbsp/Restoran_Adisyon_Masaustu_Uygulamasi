from PyQt5 import QtWidgets
from forms.frmArkaPlanUi import Ui_frmArkaPlan


class frmArkaPlan(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_frmArkaPlan()
        self.ui.setupUi(self)
