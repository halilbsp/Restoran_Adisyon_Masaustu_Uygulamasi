# 🍽️ Restoran Adisyon Masaüstü Uygulaması

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Qt Designer](https://img.shields.io/badge/Qt-Designer-green.svg)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange.svg)

Bu proje, Python ve Qt Designer kullanılarak geliştirilmiş, MySQL veritabanı altyapısına sahip kapsamlı bir **restoran adisyon ve masa yönetim sistemidir**. İşletmelerin sipariş, stok, masa ve müşteri yönetimini tek bir masaüstü uygulamasından kolayca yapabilmesini sağlar.

---

## 🌟 Özellikler

Uygulama aşağıdaki temel modülleri içermektedir:

* **🔐 Kullanıcı Girişi:** Yetkili girişi için güvenli login ekranı.
* **🪑 Masa Yönetimi:** Masaların boş/dolu durumlarını renk kodları ile görsel takip etme.
* **📝 Sipariş Sistemi (Adisyon):** Masalara hızlı ürün ekleme, adet belirleme ve toplam tutar hesaplama.
* **💳 Ödeme & Kasa:** Nakit veya kredi kartı ile ödeme alma, masayı kapatma.
* **📦 Stok ve Menü Yönetimi:** Ürün ekleme, silme, fiyat güncelleme ve kategori yönetimi.
* **👥 Müşteri Takibi:** Müşteri veritabanı oluşturma, yeni kayıt ve düzenleme işlemleri.
* **📊 Raporlama:** Günlük, haftalık ve aylık ciro raporları. Satış istatistiklerinin görselleştirilmesi.

---

## 🛠️ Kullanılan Teknolojiler

* **Programlama Dili:** Python
* **Arayüz (GUI):** PyQt5 / Qt Designer
* **Veritabanı:** MySQL
* **Diğer Kütüphaneler:** `mysql-connector`, `matplotlib` (grafikler için), `PyQt5-tools`.

---

## 🚀 Kurulum ve Çalıştırma

Projeyi bilgisayarınızda çalıştırmak için:

1.  **Projeyi Klonlayın:**
    ```bash
    git clone [https://github.com/KULLANICI_ADINIZ/restoran-adisyon-uygulamasi.git](https://github.com/KULLANICI_ADINIZ/restoran-adisyon-uygulamasi.git)
    cd restoran-adisyon-uygulamasi
    ```

2.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Veritabanı Bağlantısı:**
    * Bilgisayarınızda MySQL sunucusunun kurulu olduğundan emin olun.
    * Proje içindeki `.sql` dosyasını veritabanınıza import edin.
    * `main.py` (veya veritabanı bağlantı dosyanız) içerisindeki kullanıcı adı ve şifre alanlarını kendi yerel sunucunuza göre düzenleyin.

4.  **Uygulamayı Başlatın:**
    ```bash
    python main.py
    ```
---

## 📢 Teşekkür ve Atıf (Credits)

Bu proje geliştirilirken **Rehber Yazılım** YouTube kanalındaki eğitim serisinden yararlanılmıştır. Eğitim içeriği ve rehberliği için kendilerine teşekkür ederim.

🔗 [Rehber Yazılım YouTube Kanalı](https://www.youtube.com/@RehberYazilim)

---

## 👤 İletişim

**Geliştirici:** [Halil BAŞPINAR]  
**GitHub:** [github.com/halilbsp](https://github.com/halilbsp)  
**LinkedIn:** [linkedin.com/in/halilbaşpınar](www.linkedin.com/in/halil-başpınar-0a7478384)
