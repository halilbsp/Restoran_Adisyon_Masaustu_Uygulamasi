from forms.frmOdemeUi import Ui_frmOdeme
from PyQt5 import QtWidgets
from database.connect_to_database import connect_to_database
import mysql.connector
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDateTime


class frmOdeme(QtWidgets.QWidget):
    def __init__(self, masa_no=None):
        super(frmOdeme, self).__init__()
        self.ui = Ui_frmOdeme()
        self.ui.setupUi(self)
        self.showFullScreen()

        self.ui.lblOdemeMasaNo.setText(masa_no)
        self.masa_no = masa_no

        # Varsayılanlar
        self.servis_turu = "normal"
        self.durum = "açık"

        # Buton bağlantıları
        self.ui.btnGeri.clicked.connect(self.back_application)
        self.ui.btnUrunGetir.clicked.connect(self.populate_table)
        self.ui.btnHesapKapat.clicked.connect(self.close_account)

        # Veritabanı bağlantısı
        self.connection = connect_to_database()


    def back_application(self):
        from views.frmMasalar import frmMasalar
        self.masalar = frmMasalar()
        self.masalar.show()
        self.close()


    def populate_table(self):
        self.masa_no = self.ui.lblOdemeMasaNo.text()

        if self.connection is not None:
            try:
                cursor = self.connection.cursor()

                query = (
                    "SELECT s.id, s.urunId, s.adisyonId, s.masaId, s.adet, s.urunNot, "
                    "u.urunAd, u.fiyat "
                    "FROM satislar AS s "
                    "INNER JOIN urunleer AS u ON s.urunId = u.id "
                    "WHERE s.masaId = %s AND s.servisTuru = %s AND s.durum = %s"
                )

                cursor.execute(query, (self.masa_no, self.servis_turu, self.durum))

                self.ui.twSiparisOdeme.setRowCount(0)
                total_price = 0

                for row_num, (satis_id, urun_id, adisyon_id, masa_id, adet, urun_not, urun_adi, fiyat) in enumerate(cursor.fetchall()):
                    self.ui.twSiparisOdeme.insertRow(row_num)
                    self.ui.twSiparisOdeme.setItem(row_num, 0, QTableWidgetItem(urun_adi))
                    self.ui.twSiparisOdeme.setItem(row_num, 1, QTableWidgetItem(str(adet)))
                    self.ui.twSiparisOdeme.setItem(row_num, 2, QTableWidgetItem(str(fiyat)))
                    self.ui.twSiparisOdeme.setItem(row_num, 3, QTableWidgetItem(str(urun_not)))
                    self.ui.twSiparisOdeme.setItem(row_num, 4, QTableWidgetItem(str(satis_id)))
                    self.ui.twSiparisOdeme.setItem(row_num, 5, QTableWidgetItem(str(urun_id)))
                    self.ui.twSiparisOdeme.setItem(row_num, 6, QTableWidgetItem(str(adisyon_id)))
                    self.ui.twSiparisOdeme.setItem(row_num, 7, QTableWidgetItem(str(masa_id)))

                    total_price += adet * fiyat

                self.ui.lblToplamTutar.setText(str(total_price))

                cursor.close()

            except mysql.connector.Error as err:
                print("Hata populate_table:", err)
        else:
            print("Veritabanı bağlantısı başarısız")


    def close_account(self):
        self.masa_no = self.ui.lblOdemeMasaNo.text()

        # Ödeme türü seçimi
        if self.ui.rbNakit.isChecked():
            payment_type = "Nakit"
        elif self.ui.rbKart.isChecked():
            payment_type = "Kart"
        else:
            QMessageBox.critical(self, "Ödeme Türü Hatası", "Lütfen ödeme türünü seçin...")
            return

        confirmation = QMessageBox.question(self, "Onay", "Masa kapatılsın mı?",
                                            QMessageBox.Ok | QMessageBox.Cancel)

        if confirmation != QMessageBox.Ok:
            return

        if self.connection is None:
            print("Veritabanı bağlantısı yok.")
            return

        try:
            cursor = self.connection.cursor()

            adisyon_totals = {}

            for row_num in range(self.ui.twSiparisOdeme.rowCount()):
                adisyon_id = int(self.ui.twSiparisOdeme.item(row_num, 6).text())

                adet = int(self.ui.twSiparisOdeme.item(row_num, 1).text())
                fiyat = float(self.ui.twSiparisOdeme.item(row_num, 2).text())
                item_total = adet * fiyat

                if adisyon_id in adisyon_totals:
                    adisyon_totals[adisyon_id] += item_total
                else:
                    adisyon_totals[adisyon_id] = item_total

            odeme_tarihi = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")

            for adisyon_id, toplam_tutar in adisyon_totals.items():

                # Ödeme kayıt ekleme
                cursor.execute(
                    "INSERT INTO hesapodemeleri (adisyonId, odemeTuru, toplamTutar, tarih, servisTuru) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (adisyon_id, payment_type, toplam_tutar, odeme_tarihi, self.servis_turu)
                )

            # Adisyon güncelle
            cursor.execute(
                "UPDATE adisyonlar SET durum = %s WHERE masaId = %s AND servisTuru = %s",
                ("kapalı", self.masa_no, self.servis_turu)
            )

            # Masa güncelle
            cursor.execute(
                "UPDATE masalar SET durum = %s, masaDurum = %s WHERE id = %s",
                (1, "kapalı", self.masa_no)
            )

            # Sipariş güncelle
            cursor.execute(
                "UPDATE satislar SET durum = %s WHERE masaId = %s AND servisTuru = %s",
                ("kapalı", self.masa_no, self.servis_turu)
            )

            self.connection.commit()

            # UI Temizle
            self.ui.twSiparisOdeme.setRowCount(0)
            self.ui.lblToplamTutar.setText("0.00")

            # Masalara dön
            from views.frmMasalar import frmMasalar
            self.frm_masalar = frmMasalar()
            self.frm_masalar.show()
            self.close()

        except Exception as ex:
            print("Hata:", ex)
