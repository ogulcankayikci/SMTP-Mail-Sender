import json
import os

def kaydet_ayarlar():
    print("\n=== SMTP Sunucu Ayarları ===")
    
    config = {
        'smtp_sunucu': input('SMTP Sunucu adresi: '),
        'smtp_port': int(input('SMTP Port numarası: ')),
        'kullanici_adi': input('SMTP Kullanıcı adı (boş bırakılabilir): '),
        'parola': input('SMTP Parola (boş bırakılabilir): ')
    }
    
    # Ayarları JSON dosyasına kaydet
    with open('mail_ayarlar.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    print("\nAyarlar başarıyla kaydedildi!")

def oku_ayarlar():
    try:
        with open('mail_ayarlar.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Ayarlar dosyası bulunamadı! Lütfen önce ayarları kaydedin.")
        return None

if __name__ == "__main__":
    kaydet_ayarlar() 