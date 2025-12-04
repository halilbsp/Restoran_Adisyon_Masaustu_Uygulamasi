import subprocess
import os

pyuic_path = r"C:\Users\Halil Başpınar\AppData\Local\Programs\Python\Python313\Scripts\pyuic5.exe"

ui_files = [
    "ui/frmGiris.ui",
    "ui/frmArkaPlan.ui",
    "ui/frmMenu.ui",
    "ui/frmMasalar.ui",
    "ui/frmSiparis.ui",
    "ui/frmOdeme.ui",
]

for ui_file in ui_files:
    py_file = "forms/{}.py".format(ui_file.split("/")[-1].replace(".ui", "Ui"))
    command = [pyuic_path, ui_file, "-o", py_file]
    
    try:
        subprocess.run(command, check=True)
        print(f"{ui_file} başarıyla dönüştürüldü.")
    except subprocess.CalledProcessError:
        print(f"{ui_file} dönüştürülürken bir hata oluştu.")
