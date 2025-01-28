import tkinter as tk
from tkinter import ttk, messagebox
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Ayarları JSON dosyasına kaydetme ve yükleme
AYARLAR_DOSYASI = "ayarlar.json"

def ayarlari_yukle():
    try:
        with open(AYARLAR_DOSYASI, "r", encoding="utf-8") as dosya:
            return json.load(dosya)
    except FileNotFoundError:
        return {}

def ayarlari_kaydet(ayarlar):
    with open(AYARLAR_DOSYASI, "w", encoding="utf-8") as dosya:
        json.dump(ayarlar, dosya, ensure_ascii=False, indent=4)

def mail_gonder(smtp_sunucu, smtp_port, kullanici_adi, parola, gonderen, alici, konu, icerik):
    mesaj = MIMEMultipart()
    mesaj["From"] = gonderen
    mesaj["To"] = alici
    mesaj["Subject"] = konu
    mesaj.attach(MIMEText(icerik, "plain", "utf-8"))

    try:
        with smtplib.SMTP(smtp_sunucu, smtp_port) as server:
            if kullanici_adi and parola:
                server.login(kullanici_adi, parola)
            server.send_message(mesaj)
            messagebox.showinfo("Başarılı", "Mail başarıyla gönderildi!")
    except Exception as e:
        messagebox.showerror("Hata", f"Mail gönderilirken bir hata oluştu: {str(e)}")

def arayuz_olustur():
    ayarlar = ayarlari_yukle()

    def ayarlari_hatirla():
        yeni_ayarlar = {
            "smtp_sunucu": smtp_sunucu_giris.get(),
            "smtp_port": smtp_port_giris.get(),
            "kullanici_adi": kullanici_adi_giris.get(),
            "parola": parola_giris.get()
        }
        ayarlari_kaydet(yeni_ayarlar)
        messagebox.showinfo("Başarılı", "Ayarlar kaydedildi!")

    def maili_gonder():
        smtp_sunucu = smtp_sunucu_giris.get()
        smtp_port = smtp_port_giris.get()
        kullanici_adi = kullanici_adi_giris.get()
        parola = parola_giris.get()
        gonderen = gonderen_giris.get()
        alici = alici_giris.get()
        konu = konu_giris.get()
        icerik = icerik_giris.get("1.0", tk.END)

        if not (smtp_sunucu and smtp_port and gonderen and alici and konu and icerik):
            messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return

        mail_gonder(smtp_sunucu, smtp_port, kullanici_adi, parola, gonderen, alici, konu, icerik)

    # Ana pencere
    pencere = tk.Tk()
    pencere.title("Mail Gönderme Uygulaması")
    pencere.geometry("500x400")

    # Sekme kontrolü
    sekme_kontrol = ttk.Notebook(pencere)
    sekme_kontrol.pack(expand=True, fill="both")

    # Mail sekmesi
    mail_sekmesi = ttk.Frame(sekme_kontrol)
    sekme_kontrol.add(mail_sekmesi, text="Mail")

    ttk.Label(mail_sekmesi, text="Gönderen:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    gonderen_giris = ttk.Entry(mail_sekmesi, width=30)
    gonderen_giris.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(mail_sekmesi, text="Alıcı:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    alici_giris = ttk.Entry(mail_sekmesi, width=30)
    alici_giris.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(mail_sekmesi, text="Konu:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    konu_giris = ttk.Entry(mail_sekmesi, width=30)
    konu_giris.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(mail_sekmesi, text="İçerik:").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
    icerik_giris = tk.Text(mail_sekmesi, width=40, height=10)
    icerik_giris.grid(row=3, column=1, padx=10, pady=5)

    ttk.Button(mail_sekmesi, text="Gönder", command=maili_gonder).grid(row=4, column=0, columnspan=2, pady=10)

    # Ayarlar sekmesi
    ayarlar_sekmesi = ttk.Frame(sekme_kontrol)
    sekme_kontrol.add(ayarlar_sekmesi, text="Ayarlar")

    ttk.Label(ayarlar_sekmesi, text="SMTP Sunucu:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    smtp_sunucu_giris = ttk.Entry(ayarlar_sekmesi, width=30)
    smtp_sunucu_giris.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(ayarlar_sekmesi, text="SMTP Port:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    smtp_port_giris = ttk.Entry(ayarlar_sekmesi, width=30)
    smtp_port_giris.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(ayarlar_sekmesi, text="Kullanıcı Adı:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    kullanici_adi_giris = ttk.Entry(ayarlar_sekmesi, width=30)
    kullanici_adi_giris.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(ayarlar_sekmesi, text="Parola:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    parola_giris = ttk.Entry(ayarlar_sekmesi, width=30, show="*")
    parola_giris.grid(row=3, column=1, padx=10, pady=5)

    ttk.Button(ayarlar_sekmesi, text="Ayarları Hatırla", command=ayarlari_hatirla).grid(row=4, column=0, columnspan=2, pady=10)

    # Kaydedilen ayarları yükle
    if ayarlar:
        smtp_sunucu_giris.insert(0, ayarlar.get("smtp_sunucu", ""))
        smtp_port_giris.insert(0, ayarlar.get("smtp_port", ""))
        kullanici_adi_giris.insert(0, ayarlar.get("kullanici_adi", ""))
        parola_giris.insert(0, ayarlar.get("parola", ""))

    pencere.mainloop()

if __name__ == "__main__":
    arayuz_olustur()
