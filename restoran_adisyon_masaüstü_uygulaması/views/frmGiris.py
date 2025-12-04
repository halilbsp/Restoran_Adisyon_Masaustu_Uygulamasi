from datetime import datetime
import mysql.connector
from forms.frmGirisUi import Ui_frmGiris
from PyQt5 import QtWidgets
from database.connect_to_database import connect_to_database
from views.frmMenu import frmMenu
from PyQt5.QtWidgets import QMessageBox


class frmGiris(QtWidgets.QWidget):
    def __init__(self):
        super(frmGiris, self).__init__()
        self.ui = Ui_frmGiris()
        self.ui.setupUi(self)
        self.showFullScreen()

        # --- BUTON BAĞLANTILARI ---
        self.ui.btnGiris.clicked.connect(self.login_button_clicked)
        self.ui.btnCikis.clicked.connect(self.exit_application)

        # --- DATABASE BAĞLANTISI ---
        self.connection = connect_to_database()

    def login_button_clicked(self):
        username = self.ui.cbKullanici.text()
        password = self.ui.lnSifre.text()

        if self.check_user_login(username, password):
            print(f"{username} başarılı, Giriş Yapıldı")

            self.user_login_record()

            self.open_menu_window()
            self.hide()  # IMPORTANT: close değil hide

        else:
            self.show_error_message("Kullanıcı adı veya şifre yanlış")

    def check_user_login(self, username, password):
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                query = "SELECT * FROM personeller WHERE ad = %s AND sifre = %s"
                cursor.execute(query, (username, password))
                user = cursor.fetchone()
                cursor.close()
                return user is not None

            except mysql.connector.Error as err:
                print("Database hatası:", err)
                return False

        print("Veritabı bağlantısı başlatılamadı")
        return False

    def user_login_record(self):
        try:
            cursor = self.connection.cursor()
            login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            selected_user = self.ui.cbKullanici.text()

            query = "INSERT INTO personelhareketleri (pesonelAd, durum, tarih) VALUES (%s, %s, %s)"
            cursor.execute(query, (selected_user, "Giriş Yapıldı", login_time))
            self.connection.commit()
            cursor.close()

        except mysql.connector.Error as err:
            print("Hata user_login_record:", err)

    def open_menu_window(self):
        print("Menü ekranı açılıyor...")
        self.frmMenu = frmMenu()
        self.frmMenu.show()

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Kullanıcı Girişi Hatası")
        msg.exec_()

    def exit_application(self):
        QtWidgets.QApplication.quit()
