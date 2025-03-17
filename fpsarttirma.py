import os
import shutil
import subprocess
import winreg
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from tkinter import PhotoImage
import webbrowser


# Webhook URL'yi buraya ekle
WEBHOOK_URL = "https://discord.com/api/webhooks/1350884472974872637/gYli7yoU9SciFpYc8m0EQUrNh8tCkZljcDk2NLBipbzHQ6LypbQSrKwRKn2d_kellkUJ"

def send_discord_webhook():
    data = {
        "content": "**XAMPP Optimizasyon Programı Çalıştırıldı!** 🚀\nOptimizasyon işlemi başarıyla tamamlandı."
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"Webhook gönderilirken hata oluştu: {e}")

def move_files_to_desktop_folder():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    new_folder_path = os.path.join(desktop_path, "Masaüstü")
    
    # "Masaüstü" klasörü yoksa oluşturuluyor
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    
    # Masaüstündeki her öğe için işlem yapılır
    for item in os.listdir(desktop_path):
        item_path = os.path.join(desktop_path, item)
        
        # Eğer öğe "Recycle Bin" değilse ve bir dosya veya klasör ise
        if item.lower() != "recycle bin":
            try:
                if os.path.isfile(item_path):  # Dosya taşıma
                    shutil.move(item_path, os.path.join(new_folder_path, item))
                    print(f"{item} dosyası başarıyla taşındı.")
                elif os.path.isdir(item_path):  # Klasör taşıma
                    shutil.move(item_path, os.path.join(new_folder_path, item))
                    print(f"{item} klasörü başarıyla taşındı.")
            except Exception as e:
                print(f"{item} dosyası veya klasörü taşınamadı: {e}")


def open_url(url):
    webbrowser.open(url)

def disable_unnecessary_services():
    commands = [
        'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Search" /v "BingSearchEnabled" /t REG_DWORD /d 0 /f',
        'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Search" /v "CortanaConsent" /t REG_DWORD /d 0 /f',
        'reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\System" /v "EnableActivityFeed" /t REG_DWORD /d 0 /f',
        'reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\System" /v "PublishUserActivities" /t REG_DWORD /d 0 /f',
        'reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\System" /v "UploadUserActivities" /t REG_DWORD /d 0 /f',
        'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "EnableLUA" /t REG_DWORD /d 0 /f',
        'reg add "HKCU\\Software\\Microsoft\\InputPersonalization" /v "RestrictImplicitTextCollection" /t REG_DWORD /d 1 /f',
        'reg add "HKCU\\Software\\Microsoft\\InputPersonalization" /v "RestrictImplicitInkCollection" /t REG_DWORD /d 1 /f'
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True)

def clear_temp_folders():
    temp_folders = [
        os.getenv('TEMP'),
        os.getenv('TMP'),
        "C:\\Windows\\Temp",
        "C:\\Windows\\Prefetch"
    ]
    for folder in temp_folders:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Dosya silinemedi: {file_path}, Hata: {e}")

def set_high_performance():
    subprocess.run('powercfg /s SCHEME_MIN', shell=True)

def change_visual_settings():
    commands = [
        'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v "AppsUseLightTheme" /t REG_DWORD /d 0 /f',
        'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v "SystemUsesLightTheme" /t REG_DWORD /d 0 /f',
        'reg add "HKCU\\Software\\Microsoft\\Windows\\DWM" /v "EnableBlurBehind" /t REG_DWORD /d 0 /f',
        'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "TaskbarSmallIcons" /t REG_DWORD /d 1 /f'
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True)

def set_black_wallpaper():
    key = winreg.HKEY_CURRENT_USER
    path = r"Control Panel\Desktop"
    with winreg.OpenKey(key, path, 0, winreg.KEY_SET_VALUE) as reg_key:
        winreg.SetValueEx(reg_key, "WallPaper", 0, winreg.REG_SZ, "")
    subprocess.run("RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters", shell=True)

def disable_lock_screen_background():
    subprocess.run('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Personalization" /v "NoLockScreen" /t REG_DWORD /d 1 /f', shell=True)

def set_theme_color():
    subprocess.run('reg add "HKCU\\Software\\Microsoft\\Windows\\DWM" /v "AccentColor" /t REG_DWORD /d 0xFF0078D7 /f', shell=True)

def run_fps_reg():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    reg_file_path = os.path.join(current_dir, "FPS.reg") 

    if os.path.exists(reg_file_path):
        subprocess.run(['regedit', '/s', reg_file_path], shell=True)
    else:
        print("FPS.reg dosyası bulunamadı!")

def optimize_fps():
    disable_unnecessary_services()
    clear_temp_folders()
    set_high_performance()
    change_visual_settings()
    set_black_wallpaper()
    disable_lock_screen_background()
    set_theme_color()
    run_fps_reg()  # FPS.reg dosyasını çalıştır
    move_files_to_desktop_folder()  # Dosyaları masaüstü klasörüne taşı
    send_discord_webhook()
    messagebox.showinfo("XAMPP Optimizasyon", "Optimizasyon işlemi başarıyla tamamlandı!")

def create_gui():
    # Ana pencere
    root = tk.Tk()
    root.title("XAMPP Optimizasyon Programı")
    root.geometry("500x500")  # Pencereyi büyüttük
    root.config(bg="#FF6F00")  # Arka planı koyu turuncu yaptık
    root.iconbitmap("app_icon.ico")  # Pencere başlığına icon ekledik
    root.resizable(False, False)  # Pencereyi küçültüp büyütmeyi engelledik

    # Başlık
    title_label = tk.Label(root, text="XAMPP Optimizasyon Programı", font=("Arial", 18, "bold"), fg="white", bg="#FF6F00")
    title_label.pack(pady=20)

    # Açıklama
    description_label = tk.Label(root, text="Bilgisayarınızı optimize etmek ve FPS arttırmak için tıklayın", font=("Arial", 12), fg="white", bg="#FF6F00")
    description_label.pack(pady=10)

    # Buton
    optimize_btn = tk.Button(root, text="FPS Arttır", command=optimize_fps, font=("Arial", 14), fg="white", bg="#0078D7", relief="raised", width=15)
    optimize_btn.pack(pady=15)

    # Durum çubuğu
    status_label = tk.Label(root, text="Üstteki düğmeye basarak \nBilgisayarınızın daha düzgün çalışmasını sağlayabilirsiniz.", font=("Arial", 11), fg="white", bg="#FF6F00")
    status_label.pack(pady=10)

    instagram_img = tk.PhotoImage(file="instagram_icon.png")  # Dosya yolunu kontrol edin
    github_img = tk.PhotoImage(file="github_icon.png")
    discord_img = tk.PhotoImage(file="discord_icon.png")

    # Koyu turuncu arka planlı butonlar (activebackground ile tıklama sırasında da aynı kalır)
    instagram_btn = tk.Button(root, image=instagram_img,
                              command=lambda: open_url("https://www.instagram.com/bugrasd"),
                              bd=0, highlightthickness=0, bg="#FF6F00", activebackground="#FF6F00")
    github_btn = tk.Button(root, image=github_img,
                           command=lambda: open_url("https://www.github.com/bugrasd"),
                           bd=0, highlightthickness=0, bg="#FF6F00", activebackground="#FF6F00")
    discord_btn = tk.Button(root, image=discord_img,
                            command=lambda: open_url("https://discord.gg/mXbN3gVzPS"),
                            bd=0, highlightthickness=0, bg="#FF6F00", activebackground="#FF6F00")

    # Butonları yerleştirme
    instagram_btn.place(x=80, y=300, width=128, height=128)
    github_btn.place(x=210, y=300, width=128, height=128)
    discord_btn.place(x=340, y=300, width=128, height=128)




    root.mainloop()

if __name__ == "__main__":
    create_gui()
