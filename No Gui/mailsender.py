import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import oku_ayarlar

def mail_gonder():
    # Ayarları oku
    ayarlar = oku_ayarlar()
    if not ayarlar:
        return
    
    print("\n=== Mail Gönderme Formu ===")
    
    # Mail bilgilerini al
    gonderen = input("Gönderen mail adresi: ")
    alici = input("Alıcı mail adresi: ")
    konu = input("Mail konusu: ")
    icerik = input("Mail içeriği: ")
    
    # Mail oluştur
    mesaj = MIMEMultipart()
    mesaj["From"] = gonderen
    mesaj["To"] = alici
    mesaj["Subject"] = konu
    
    mesaj.attach(MIMEText(icerik, "plain", "utf-8"))
    
    try:
        # SMTP sunucusuna bağlan
        with smtplib.SMTP(ayarlar['smtp_sunucu'], ayarlar['smtp_port']) as server:
            # Eğer kullanıcı adı ve parola varsa login ol
            if ayarlar['kullanici_adi'] and ayarlar['parola']:
                server.login(ayarlar['kullanici_adi'], ayarlar['parola'])
            
            # Maili gönder
            server.send_message(mesaj)
            print("\nMail başarıyla gönderildi!")
            
    except Exception as e:
        print(f"\nHata oluştu: {str(e)}")

if __name__ == "__main__":
    mail_gonder() 