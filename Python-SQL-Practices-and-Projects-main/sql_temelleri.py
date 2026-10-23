import sqlite3

# 1. ADIM: Veritabanına bağlan (Dosya yoksa PyCharm klasöründe otomatik oluşturulur)
conn = sqlite3.connect("okul_rehberi.db")
cursor = conn.cursor()

# 2. ADIM: Tablo Oluşturma
# Tablomuz yoksa oluşturuyoruz: ID, Isim, Bolum ve Not
cursor.execute("""
               CREATE TABLE IF NOT EXISTS ogrenciler
               (
                   id
                   INTEGER
                   PRIMARY
                   KEY
                   AUTOINCREMENT,
                   isim
                   TEXT
                   NOT
                   NULL,
                   bolum
                   TEXT,
                   not_ortalamasi
                   REAL
               )
               """)
conn.commit()  # Tablo oluşturmayı kaydet
print("1. Tablo başarıyla hazırlandı.")


# 3. ADIM: Yardımcı Ekran Yazdırma Fonksiyonu
# Her işlemden sonra veritabanının son halini görmek için kullanacağız
def verileri_listele():
    print("\n--- MEVCUT ÖĞRENCİ LİSTESİ ---")
    cursor.execute("SELECT * FROM ogrenciler")
    kayitlar = cursor.fetchall()

    if not kayitlar:
        print("Tabloda henüz hiç veri yok!")
    else:
        for satir in kayitlar:
            print(f"ID: {satir[0]} | İsim: {satir[1]} | Bölüm: {satir[2]} | Not: {satir[3]}")
    print("-" * 30)


# 4. ADIM: İlk Durumu Görelim
verileri_listele()

# --- VERİ EKLEME (INSERT INTO) ---
print("\n>>> Veriler ekleniyor...")

# Tekli veri ekleme
cursor.execute("INSERT INTO ogrenciler (isim, bolum, not_ortalamasi) VALUES ('Gözde', 'Veri Bilimi', 3.90)")

# Toplu veri ekleme
yeni_ogrenciler = [
    ('Ahmet', 'Yazılım', 3.20),
    ('Mehmet', 'Matematik', 2.80),
    ('Ayşe', 'Veri Bilimi', 3.75)
]

cursor.executemany("INSERT INTO ogrenciler (isim, bolum, not_ortalamasi) VALUES (?, ?, ?)", yeni_ogrenciler)

conn.commit()  # Değişiklikleri kaydet
verileri_listele()  # Güncel listeyi göster

# --- VERİ GÜNCELLEEME (UPDATE) ---
print("\n >>> Mehmet'in bilgileri güncelleniyor...")

#Mehmet'in not ortalamasını 3.50 yapıo bölümünü 'Yazılım' olarak güncelliyoruz

cursor.execute("""
UPDATE ogrenciler
SET not_ortalamasi = 3.50, bolum = 'Yazılım'
WHERE isim = 'Mehmet'    
""")

conn.commit()      #Değişikliği veritabanına kaydet
verileri_listele() #Mehmet'in güncellenmiş halini ekranda kontrol et

# --- VERİ SİLME (DELETE)
print("\n>>> Not ortalaması 3.30 altında olanlar silniyor...")

#Şarta uyan öğrencileri sil

cursor.execute("DELETE FROM ogrenciler WHERE not_ortalamasi < 3.30")
conn.commit()
verileri_listele()

# --- ADIM 4: GELİŞMİŞ SORGULAR VE FİLTRELEME ---

# 1. Sıralama (ORDER BY): Not ortalamasına göre yüksekten düşüğe sırala (DESC)
print("\n>>> Not Ortalamasına Göre Sıralı Liste (Yüksekten Düşüğe):")
cursor.execute("SELECT * FROM ogrenciler ORDER BY not_ortalamasi DESC")
for satir in cursor.fetchall():
    print(f"İsim: {satir[1]} | Bölüm: {satir[2]} | Not: {satir[3]}")

# 2. Gruplama (GROUP BY): Bölümlere göre kaç öğrenci var?
print("\n>>> Bölümlere Göre Öğrenci Sayıları:")
cursor.execute("SELECT bolum, COUNT(*) FROM ogrenciler GROUP BY bolum")
for satir in cursor.fetchall():
    print(f"Bölüm: {satir[0]} -> Öğrenci Sayısı: {satir[1]}")

# 3. İstatistik (AVG): Veri Bilimi bölümünün not ortalaması nedir?
cursor.execute("SELECT AVG(not_ortalamasi) FROM ogrenciler WHERE bolum = 'Veri Bilimi'")
ort_not = cursor.fetchone()[0]
print(f"\n>>> Veri Bilimi Bölümü Not Ortalaması: {round(ort_not, 2)}")






# 5. ADIM: Bağlantıyı Kapatma (Kodun en altında durmalı)
conn.close()


