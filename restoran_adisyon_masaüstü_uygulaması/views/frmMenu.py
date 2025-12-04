from database.connect_to_database import connect_to_database
from forms.frmMenuUi import Ui_frmMenu
from PyQt5 import QtWidgets
from datetime import datetime



class frmMenu(QtWidgets.QWidget):
    def __init__(self):
        super(frmMenu, self).__init__()
        self.ui = Ui_frmMenu()
        self.ui.setupUi(self)
        self.showFullScreen()

        # Butonlara tıklandığında yapılacak işlemler
        self.ui.btnMasalar.clicked.connect(self.tables_application)
        self.ui.btnCikis.clicked.connect(self.exit_application)
        self.ui.btnKilit.clicked.connect(self.back_application)

        # Database bağlantısını başlatma
        self.connection = connect_to_database()

        # Arayüzdeki saati güncelle
        self.update_time_date()

def update_time_date(self):           # Arayüzdeki saati güncelle
    simdiki_zaman = datetime.now()
    saat = simdiki_zaman.strftime("%H:%M")
    tarih = self.create_history_text()
    self.ui.lblSaat.setText(saat)
    self.ui.lblTarih.setText(tarih)

def create_history_text(self):    # Arayüzdeki tarih formatını güncelle
    simdiki_zaman = datetime.now()
    gunler = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]
    aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

    gun = gunler[simdiki_zaman.weekday()]
    ay = aylar[simdiki_zaman.month - 1]

    tarih_metni = f"{simdiki_zaman.day} {ay} {gun}"
    return tarih_metni

def tables_application(self):
    print("Masalar sayfasına gidiyor...")
    from views.frmMasalar import frmMasalar
    self.masalar = frmMasalar()
    self.masalar.show()
    self.close()

def back_application(self):
    print("Giriş sayfasına dönüldü...")
    from views.frmGiris import frmGiris
    self.giris = frmGiris()
    self.giris.show()
    self.close()

def exit_application(self):
    QtWidgets.QApplication.quit()
