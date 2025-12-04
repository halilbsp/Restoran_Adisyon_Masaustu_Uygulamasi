from forms.frmMasalarUi import Ui_frmMasalar
from PyQt5 import QtWidgets
from database.connect_to_database import connect_to_database
import mysql.connector  # DÜZELTME 1: Eksik import tamamlandı
from PyQt5.QtGui import QPixmap, QIcon

class frmMasalar(QtWidgets.QWidget):
    def __init__(self):
        super(frmMasalar, self).__init__()
        self.ui = Ui_frmMasalar()
        self.ui.setupUi(self)
        self.showFullScreen()

        self.ui.btnCikis.clicked.connect(self.back_application)
        # Butonların tanımlanması
        self.masa_buttons = [
            self.ui.btnMasa1, self.ui.btnMasa2, self.ui.btnMasa3, self.ui.btnMasa4, self.ui.btnMasa5,
            self.ui.btnMasa6, self.ui.btnMasa7, self.ui.btnMasa8, self.ui.btnMasa9, self.ui.btnMasa10,
            self.ui.btnMasa11, self.ui.btnMasa12, self.ui.btnMasa13, self.ui.btnMasa14, self.ui.btnMasa15,
            self.ui.btnMasa16, self.ui.btnMasa17, self.ui.btnMasa18, self.ui.btnMasa19, self.ui.btnMasa20,
            self.ui.btnMasa21, self.ui.btnMasa22, self.ui.btnMasa23, self.ui.btnMasa24, self.ui.btnMasa25,
            self.ui.btnMasa26, self.ui.btnMasa27, self.ui.btnMasa28, 
        ]

        # Masa butonlarına tıklandığında yapılacak işlemler
        # DÜZELTME 2: 'satrt' yerine 'start' yazıldı
        for i, masa_buton in enumerate(self.masa_buttons, start=1):
            masa_buton.clicked.connect(lambda _, masa_no=i: self.masa_button_clicked(masa_no))

        # Database bağlantısı başlatma
        self.connection = connect_to_database()

        # Masalardaki masa butonları üzerindeki elementleri düzenleme
        self.tables_control()   # Masa elementleri kontrol edilmesi
        self.update_table_status()  # Masalardaki durumları güncelleme

    def back_application(self):
        QtWidgets.QApplication.quit()

    
    def masa_button_clicked(self, masa_no):      # Sipariş sayfasına geçme
        print(f"Masa {masa_no} tıklandı.")
        from views.frmSiparis import frmSiparis
        self.siparis = frmSiparis(str(masa_no))
        self.siparis.show()
        self.close()

    def tables_control(self):          # Masalardaki masa butonları üzerindeki elementleri güncelleme
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                # Adisyonlar tablosundan masa numarasına göre masa butronları üzerindeki elementleri güncelleme
                query = "SELECT masaİd, durum, tarih FROM adisyonlar WHERE durum = 'açık' AND servisTuru = 'normal'"

                cursor.execute(query)
                adisyonlar = cursor.fetchall()

                for adisyon in adisyonlar:
                    masa_id = adisyon[0]
                    masa_durum = adisyon[1]
                    tarih = adisyon[2]

                    if masa_durum == "açık":
                        # Masa durum labelini dolduracağız
                        # Not: Burada masa_id integer ise string'e çevrilmesi gerekebilir veya f-string otomatik halleder.
                        # Eğer UI dosyasında isimler lblBtnDurum_1 şeklindeyse sorun yok.
                        label_durum = getattr(self.ui, f"lblBtnDurum_{masa_id}")
                        label_durum.setText("Dolu")

                        # Masa satış saatini dolduracağız
                        label_tarih = getattr(self.ui, f"lblBtnSaat_{masa_id}")
                        label_tarih.setText(tarih.strftime("%H:%M"))

                        # Masa toplam tutarını dolduracağız
                        toplam_tutar = self.calculate_total_sales(masa_id)
                        label_tutar = getattr(self.ui, f"lblBtnFiyat_{masa_id}")
                        label_tutar.setText(f"$ {str(toplam_tutar)}")

                    else:
                        # Masa durumunu boş göndereceğiz
                        label_durum = getattr(self.ui, f"lblBtnDurum_{masa_id}")
                        label_durum.setText("Dolu") # Mantıken burası "Boş" olmalı olabilir mi? Kontrol etmenizde fayda var.

                cursor.close()
            except mysql.connector.Error as err:
                print("Hata tables_control:", err)
        else:
            print("Veritabanı bağlantısı başlatılamadı")

    def calculate_total_sales(self, masa_id):   # Masa toplam tutarını hesaplama
        if self.connection is not None:
            try:
                # DÜZELTME 3: self.colorCount yerine self.connection kullanıldı
                cursor = self.connection.cursor()

                # masaİd göre satışlarının toplamını hesapla
                query = (f"SELECT SUM(u.fiyat * s.adet) FROM satislar s JOIN urunler u ON s.urunId = u.id WHERE s.adisyonId = (SELECT id FROM adisyonlar WHERE masaId = '{masa_id}' AND durum = 'açık' and servisTuru = 'normal') and s.durum = 'açık'")
                cursor.execute(query)
                total_sales = cursor.fetchone()[0]
                cursor.close()

                return total_sales if total_sales else "0" # Boş ise 0 döndürmek daha güvenli olabilir
            
            except mysql.connector.Error as err:
                print("Hata calculate_total_sales:", err)
                return "hata"
        else:
            print("Veritabanı bağlantısı başarısız")

    def update_table_status(self):    # Masalardaki resim durumlarını güncelleme
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                query = "SELECT id, durum FROM masalar"
                cursor.execute(query)
                masa_durumlari = cursor.fetchall()

                # Adisyonlar tablosundan masa numarasına göre masa butonları üzerindeki resimleri güncelleme
                for masa_id, masa_durumu in masa_durumlari:
                    # masa_id veritabanından integer geliyorsa -1 işlemi doğrudur.
                    if masa_id <= len(self.masa_buttons):
                        masa_button = self.masa_buttons[masa_id - 1]

                        if masa_durumu == "1":
                            # Masa boşken resim dolduracağız
                            image_path = ":/nmasalar/resimler/MASA/bos_masa.png"
                            pixmap = QPixmap(image_path)
                            masa_button.setIcon(QIcon(pixmap))
                        elif masa_durumu == "2":
                             # Masa doluyken resim dolduracağız
                            image_path = ":/nmasalar/resimler/MASA/dolu_masa.png"
                            pixmap = QPixmap(image_path)
                            masa_button.setIcon(QIcon(pixmap))

            except mysql.connector.Error as err:
                print("Hata update_table_status:", err)
        else:
            print("Veritabanı bağlantısı başlatılamadı")