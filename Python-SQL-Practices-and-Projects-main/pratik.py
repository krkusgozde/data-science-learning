import sqlite3
from tkinter.constants import INSERT

conn = sqlite3.connect('kutuphane.db')
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS kitaplar
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kitap_adi TEXT,
                yazar TEXT   
                )
""")

conn.commit()
print("1. Tablo başarıyla hazırlandı")

def kitaplari_listele():
    print("\n --- MEVCUT KİTAP LİSTESİ --- ")
    cursor.execute("SELECT * FROM kitaplar")
    kayitlar = cursor.fetchall()

    if not kayitlar:
        print("Kütüphanede henüz kitap yok!")

    else:
        for kitap in kayitlar:
            print(f"ID: {kitap[0]} | Kitap adı : {kitap[1]} | Yazar: {kitap[2]}")
    print("-" * 30)

kitaplari_listele()


print("\n >>> Veriler ekleniyor...")

cursor.execute("INSERT INTO kitaplar(kitap_adi,yazar) VALUES ('Suç ve Ceza', 'Dostoyevski')")

yeni_kitaplar = [
    ('Sefiller' , 'Victor Hugo'),
    ('Simyacı' , 'Paulo Coelho')

]

cursor.executemany("INSERT INTO kitaplar (kitap_adi,yazar) VALUES (?,?)", yeni_kitaplar)

conn.commit()
kitaplari_listele()

print("\n >>> Suç ve Ceza'nın bilgileri güncelleniyor...")

cursor.execute("""
UPDATE kitaplar
SET kitap_adi = 'Suç ve Ceza(Tam Metin)' , yazar = 'Dostoyevski'
WHERE id = 1    
""")

conn.commit()
kitaplari_listele()

print("\n >>> Simyacı kitabı siliniyor...")
cursor.execute("DELETE FROM kitaplar WHERE id = 3")
conn.commit()
kitaplari_listele()




conn.close()


