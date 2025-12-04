from forms.frmSiparisUi import Ui_frmSiparis
from PyQt5 import QtWidgets
from database.connect_to_database import connect_to_database
import mysql.connector # DÜZELTME: import mysql yerine mysql.connector
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox

class frmSiparis(QtWidgets.QWidget):
    def __init__(self, masa_no=None):
        super(frmSiparis, self).__init__()
        self.ui = Ui_frmSiparis()
        self.ui.setupUi(self)
        self.showFullScreen()

        # Tıklanan masanın numarasını alma
        self.ui.lblMasaNo.setText(masa_no)

        # Katagori ID'lerini butonlara eşleştiren bir sözlük oluşturun
        category_buttons = {
            self.ui.btnAnaYemek: 1,
            self.ui.btnMakarna: 2,
            self.ui.btnSalata: 3,
            self.ui.btnCorba: 4,
            self.ui.btnFastfood: 5,
            self.ui.btnIcecekler: 6,
            self.ui.btnArasicak: 7,
            self.ui.btnTatli: 8,
            self.ui.btnDurum: 9,
        }

        # Butonlara tıklama işlemleri
        for button, category_id in category_buttons.items():
            button.clicked.connect(lambda _, category_id=category_id: self.get_items_by_category(category_id))
        
        # Butonlara tıklandığında yapılacak işlemler
        self.ui.btnGeri.clicked.connect(self.back_application)
        self.ui.twIcindekiler.itemClicked.connect(self.contents_table)
        self.ui.btnOdeme.clicked.connect(self.payment_application)
        self.ui.btnUrunSil.clicked.connect(self.order_table_delete)
        self.ui.btnSiparis.clicked.connect(self.order_application)

        # Database bağlantısını başlatma
        self.connection = connect_to_database()

    def get_items_by_category(self, category_id):   # Kategori id'sine göre ürünleri getirme
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                query = "SELECT id, urunAd, fiyat FROM urunler WHERE kategori_İd = %s"
                cursor.execute(query, (category_id,))
                items = cursor.fetchall()

                # Tabloviewdeki verileri temizleme
                self.ui.twIcindekiler.setRowCount(0)

                # Verileri tabloya ekleme
                for row_num, (id, urunAd, fiyat) in enumerate(items): # SQL sırasına dikkat: id, urunAd, fiyat
                    # Veritabanından gelen sıraya göre enumerate içindeki değişkenleri ayarladım, ancak items tuple'ı (id, urunAd, fiyat) dönüyor.
                    # SQL: SELECT id, urunAd, fiyat
                    # items[0] -> id, items[1] -> urunAd, items[2] -> fiyat
                    # Kodunuzda (urunAd, fiyat, id) olarak açmıştınız, burayı düzelttim.
                    
                    # Ancak sizin twIcindekiler tablonuzun sütun yapısını bilmediğim için
                    # eski koddaki atamalara sadık kalıyorum:
                    # Col 0: Fiyat, Col 1: ID, Col 2: Ad
                    
                    # items içinden doğru veriyi çekmek için:
                    db_id = row_num
                    val_id = items[db_id][0]
                    val_ad = items[db_id][1]
                    val_fiyat = items[db_id][2]

                    self.ui.twIcindekiler.insertRow(row_num)
                    self.ui.twIcindekiler.setItem(row_num, 0, QtWidgets.QTableWidgetItem(str(val_fiyat)))
                    self.ui.twIcindekiler.setItem(row_num, 1, QtWidgets.QTableWidgetItem(str(val_id)))
                    self.ui.twIcindekiler.setItem(row_num, 2, QtWidgets.QTableWidgetItem(str(val_ad)))

                cursor.close()

            except mysql.connector.Error as err:
                print("Hata get_items_by_category:", err)
        else:
            print("Veritabanı bağlantısı başlatılamadı")

    def contents_table(self, item):   # Ürünleri içerik tablosuna aktarma
        # Seçilen ürünlerin bilgilerini alma
        selected_row = item.row()
        urun_fiyati = self.ui.twIcindekiler.item(selected_row, 0).text()
        urun_id = self.ui.twIcindekiler.item(selected_row, 1).text()
        urun_notu = ""
        urun_adi = self.ui.twIcindekiler.item(selected_row, 2).text()

        # twSipariş tablosundaki mevcut satırları kontrol etme
        for row in range(self.ui.twSiparis.rowCount()):
            existing_item = self.ui.twSiparis.item(row, 4) # Ürün adı 4. sütunda
            if existing_item and existing_item.text() == urun_adi:
                # Ürün zaten mevcut ise adetini arttırma
                # DÜZELTME: self.ui_twSiparis -> self.ui.twSiparis
                adet_item = self.ui.twSiparis.item(row, 1) 
                current_adet = int(adet_item.text()) if adet_item else 0
                new_adet = current_adet + 1
                adet_item = QtWidgets.QTableWidgetItem(str(new_adet))
                self.ui.twSiparis.setItem(row, 1, adet_item)
                return
            
        # twSipariş yeni bir satır ekleme işlemlerini
        row_position = self.ui.twSiparis.rowCount()
        self.ui.twSiparis.insertRow(row_position)

        # Ürün bilgilerini twSiparişler tablosuna yerleştir
        self.ui.twSiparis.setItem(row_position, 0, QtWidgets.QTableWidgetItem(urun_fiyati))
        self.ui.twSiparis.setItem(row_position, 1, QtWidgets.QTableWidgetItem("1")) # DÜZELTME: İlk eklemede Adet 1 olmalı
        self.ui.twSiparis.setItem(row_position, 2, QtWidgets.QTableWidgetItem(urun_notu))
        self.ui.twSiparis.setItem(row_position, 3, QtWidgets.QTableWidgetItem(urun_id))
        self.ui.twSiparis.setItem(row_position, 4, QtWidgets.QTableWidgetItem(urun_adi))

    def back_application(self):  # Masalar sayfasına dönme
        from views.frmMasalar import frmMasalar
        self.masalar = frmMasalar()
        self.masalar.show()
        self.close()

    def order_table_delete(self):  # Siparişi silme
        # Seçilen ürünü alma
        selected_items = self.ui.twSiparis.selectedItems()
        if not selected_items:
            return
        
        # Seçilen ürünün bulunduğu satırı alma
        selected_row = selected_items[0].row()
        self.ui.twSiparis.removeRow(selected_row)

    def payment_application(self):  # Ödeme sayfasına geçme
        masa_no = self.ui.lblMasaNo.text()
        from views.frmOdeme import frmOdeme
        self.odeme = frmOdeme(masa_no)
        self.odeme.show()
        self.close()

    def order_application(self):  # Sipariş sayfasına geçme
        # twSiparişler tablosundaki verilerin kontrolü
        if self.ui.twSiparis.rowCount() == 0:
             QMessageBox.critical(self, "Hata", "Sepette ürün yok.")
             return

        for col in range(self.ui.twSiparis.columnCount()):
            item = self.ui.twSiparis.item(0, 0)
            if item is None or item.text() == "":
                QMessageBox.critical(self, "Hata", "Sipariş verileri eksik.")
                return
            
        # twSiparişlerdeki ürünlerin adetini kontrol et
        # DÜZELTME: twSİparis -> twSiparis (Büyük İ sorunu)
        for row in range(self.ui.twSiparis.rowCount()):
            adet_item = self.ui.twSiparis.item(row, 1)
            if adet_item is None or adet_item.text() == "":
                QMessageBox.critical(self, "Hata", "Adet bilgisi boş olamaz")
                return
            
        # Sipariş verme işlemlerini
        table_number = self.ui.lblMasaNo.text()  # MASA 1
        print(f"Masa {table_number} numarasıdır...")

        # Masa durumunu kontrol eden işlem masa dolu mu boş mu?
        adisyon_id = self.chech_table_status(table_number)

        print(f"\n ----- MASANIN AÇMA DURUMU {adisyon_id} ----- \n")
        # Siparişlerin varlığını ve yokluğunu kontrol etme
        if adisyon_id is not None:
            # Mevcut bir adisyon var siparişler bunun üzerine eklesin
            self.add_order_to_existing_adisyon(adisyon_id)
        else:
            # Mevcut adisyon yok ise yeni bir adisyon oluştur ve siparişleri ekle
            adisyon_id = self.create_new_adisyon(table_number)
            self.add_order_to_existing_adisyon(adisyon_id)

        self.update_table_status(table_number)

        print(f"\n ----- MASANIN AÇMA DURUMU TAMAMLANDI ----- \n")

        self.close()
        from views.frmMasalar import frmMasalar
        self.masalar = frmMasalar()
        self.masalar.show()

    def chech_table_status(self, table_number):   # Masa durumunu kontrol eden işlem
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()

                # Masalar tablosundan belirli bir masa numarasına göre adisyon durumunu kontrol etme
                query = "SELECT id FROM adisyonlar WHERE masaİd = %s AND durum = 'açık' AND servisTuru = 'normal'"
                cursor.execute(query, (table_number,))
                result = cursor.fetchone()
                cursor.close()

                if result:
                    return result[0]
                else:
                    return None
                
            except mysql.connector.Error as err:
                print("Hata chech_table_status:", err)
        else:
            print("Veritabanı bağlantısı başlatılamadı")

    def add_order_to_existing_adisyon(self, adisyon_id):   # Mevcut adisyona sipariş ekleme
        table_number = self.ui.lblMasaNo.text()    # MASA 1

        if self.connection is not None:
            try:
                cursor = self.connection.cursor()

                for satir in range(self.ui.twSiparis.rowCount()):
                    # Sipariş detaylarını tablodan alma işlemleri
                    # DÜZELTME: Ürün ID 3. sütunda tutuluyor, 4. sütunda İsim var.
                    urun_id = self.ui.twSiparis.item(satir, 3).text() 
                    adet = self.ui.twSiparis.item(satir, 1).text()
                    urun_not = self.ui.twSiparis.item(satir, 2).text()

                    # Satış zamanını alma
                    tarih_ve_saat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    servis_turu = "normal"
                    durum = "açık"

                    # Siparişi satışlar tablosundaki verilerle uyuşturarak ekle
                    # DÜZELTME: 8 kolon var, 8 tane %s olmalı (7 taneydi)
                    query = "INSERT INTO satislar (adisyonİd, urunİd, masaİd, adet, servisTuru, durum, satisZamani, urunNot) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(query, (adisyon_id, urun_id, table_number, adet, servis_turu, durum, tarih_ve_saat, urun_not))
                    self.connection.commit()

                cursor.close()
                print(f"Masa {table_number} için siparişler eklendi.")

            except mysql.connector.Error as err:
                print("Hata add_order_to_existing_adisyon:", err)
        else:
            print("Veritabanı bağlantısı başlatılamadı")

    def create_new_adisyon(self, table_number):   # Yeni adisyon oluşturma
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()

                # Yeni bir adisyon oluşturma
                query = "INSERT INTO adisyonlar (masaİd, tarih, durum, servisTuru) VALUES (%s, %s, %s, %s)"
                # DÜZELTME: Syntax hatası datetime.now().strftime(...) 
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(query, (table_number, current_datetime, "açık", "normal"))
                self.connection.commit()

                # Oluşturulan adisyonun id numarasını al
                query  = "SELECT LAST_INSERT_ID()"
                cursor.execute(query)
                adisyon_id = cursor.fetchone()[0]

                cursor.close()
                print(f"Masa {table_number} adisyon oluşturuldu... Adisyon ID: {adisyon_id}")

                return adisyon_id
            
            except mysql.connector.Error as err:
                print("Hata create_new_adisyon:", err)
        else:
            print("Veritabanı bağlantısı başlatılamadı")
    
    def update_table_status(self, table_number):   # Masa durmu güncelleme
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                query = "UPDATE masalar SET durum = 2, masaDurum = 'açık' WHERE id = %s"
                cursor.execute(query, (table_number,))

                self.connection.commit()
                cursor.close()
                print(f"Masa {table_number} durumu güncellenmiştir...")

            except mysql.connector.Error as err:
                print("Hata update_table_status", err)
        else:
            print("Database bağlantısı hatalı")