import sqlite3



conn = sqlite3.connect("ogrenci_sistemi.db")
cursor = conn.cursor()


cursor.execute("""
               CREATE TABLE IF NOT EXISTS ogrenciler
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
               isim TEXT, 
               bolum TEXT,
               vize_notu INTEGER,
               final_notu INTEGER     
              ) 
""")

conn.commit()
print("---TABLO BAŞARIYLA HAZIRLANDI---")

def ogrenci_ekle(isim, bolum, vize_notu, final_notu):
    cursor.execute("""
                   INSERT INTO ogrenciler ( isim, bolum, vize_notu,final_notu)
                   VALUES ( ?, ?, ?, ?)""", (isim, bolum, vize_notu, final_notu))
    conn.commit()

ogrenci_ekle("Ahmet Yılmaz" , "Bilgisayar Müh.", 60,80)
ogrenci_ekle("Ayşe Kaya" , "Endüstri Müh", 85,95)
ogrenci_ekle("Mehmet Demir", "Yazılım Müh." , 40,50)
ogrenci_ekle("Zeynep Çelik" , "Bilgisayar Müh." , 70,65)


def ogrencileri_listele():
    cursor.execute("SELECT * FROM ogrenciler")
    ogrenciler = cursor.fetchall()
    for ogrenci in ogrenciler:
        ort = ogrenci[3] * 0.4 + ogrenci[4] * 0.6
        if ort >= 60:
            print(f"[GEÇTİ] {ogrenci[1]} ({ogrenci[2]}),- Ort: {ort}")
        else:
            print(f"[KALDI] {ogrenci[1]} ({ogrenci[2]}),- Ort: {ort}")

ogrencileri_listele()

def not_guncelle(ogrenci_id,yeni_vize,yeni_final):
    cursor.execute("UPDATE  ogrenciler SET vize_notu = ? , final_notu = ? WHERE id = ?", (yeni_vize,yeni_final ,ogrenci_id))
    conn.commit()
    print(f"ID: {ogrenci_id}  olan öğrencinin notları güncellendi")
not_guncelle(1,90,100)
ogrencileri_listele()

def ogrenci_sil(ogrenci_id):
    cursor.execute("DELETE FROM ogrenciler  WHERE id = ?", (ogrenci_id,))
    conn.commit()
    print(f"ID: {ogrenci_id} olan öğrenci silindi")

ogrenci_sil(3)
ogrencileri_listele()

def okul_istatistikleri():
    cursor.execute("SELECT COUNT(*) FROM ogrenciler")
    toplam = cursor.fetchone()[0]
    print(f"Toplam Öğrenci Sayısı: {toplam} ")
    cursor.execute("SELECT AVG(vize_notu) , AVG(final_notu) FROM ogrenciler")
    ortalamalar = cursor.fetchone()
    print(f"Vize Ortalaması: {ortalamalar[0]} , Final Ortalaması: {ortalamalar[1]}")
    cursor.execute("SELECT MAX(final_notu) FROM ogrenciler")
    en_yuksek = cursor.fetchone()[0]
    cursor.execute("SELECT MIN(vize_notu) FROM ogrenciler")
    en_dusuk = cursor.fetchone()[0]
    print(f"En Yüksek Final: {en_yuksek} | En Düşük Vize: {en_dusuk}")






okul_istatistikleri()






conn.close()