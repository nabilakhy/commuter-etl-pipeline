import os
import pandas as pd
from sqlalchemy import create_engine
import time

# Konfigurasi koneksi Database
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "commuter_db")

CSV_PATH = os.getenv("CSV_PATH", "data/data_commuter.csv")

def get_db_engine():
    """Membuat koneksi ke database PostgreSQL."""
    db_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(db_url)

def extract(file_path: str) -> pd.DataFrame:
    """EXTRACT: Membaca data mentah dari file CSV."""
    print(f"[EXTRACT] Membaca file dari: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} tidak ditemukan!")
    
    df = pd.read_csv(file_path)
    print(f"[EXTRACT] Berhasil mengekstrak {len(df)} baris data mentah.")
    return df

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """TRANSFORM: Membersihkan dan mengubah kode angka menjadi label deskriptif."""
    print("[TRANSFORM] Memulai proses transformasi...")
    df_clean = df.copy()
    # 1. Standarisasi nama kolom awal (huruf kecil & tanpa spasi)
    df_clean.columns = (
        df_clean.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w\s]", "", regex=True)
    )
    # 2. Hapus baris duplikat jika ada
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    print(f"[TRANSFORM] Menghapus {initial_rows - len(df_clean)} baris duplikat.")
    # 3. Ganti nama kolom kode kuesioner ke nama yang jelas (Semantic Renaming)
    column_mapping = {
        'a1': 'kode_gender',
        'a2': 'usia',
        'a3': 'kode_status',
        'a4': 'kode_asal_kota',
        'a5': 'kode_tujuan_kota',
        'a6': 'kode_pengeluaran',
        'b1': 'kode_transportasi',
        'b2': 'kode_durasi'
    }
    df_clean = df_clean.rename(columns=column_mapping)
    # 4. MAPPING DATA: Ubah kode angka menjadi teks yang mudah dipahami
    # a. Jenis Kelamin (1 = Laki-laki, 2 = Perempuan)
    gender_map = {1: 'Laki-laki', 2: 'Perempuan'}
    df_clean['jenis_kelamin'] = df_clean['kode_gender'].map(gender_map).fillna('Lainnya')
    # b. Moda Transportasi Utama (Berdasarkan kode transportasi Jabodetabek)
    transport_map = {
        4: 'KRL Commuter Line',
        3: 'TransJakarta / Bus',
        5: 'Ojek Online / Angkutan Lain',
        2: 'Kendaraan Pribadi'
    }
    df_clean['nama_transportasi'] = df_clean['kode_transportasi'].map(transport_map).fillna('Lainnya')
    # c. Pengelompokan Usia (Age Binning)
    bins = [0, 25, 40, 60, 100]
    labels = ['<25 tahun', '25-40 tahun', '41-60 tahun', '>60 tahun']
    df_clean['kelompok_usia'] = pd.cut(df_clean['usia'], bins=bins, labels=labels)
    print(f"[TRANSFORM] Transformasi selesai. Data siap: {len(df_clean)} baris, {len(df_clean.columns)} kolom.")
    return df_clean

def load(df: pd.DataFrame, table_name: str = "dim_kepuasan_komuter"):
    """LOAD: Menyimpan data yang sudah bersih ke PostgreSQL."""
    print(f"[LOAD] Menghubungkan ke PostgreSQL di {DB_HOST}:{DB_PORT}/{DB_NAME}...")
    engine = get_db_engine()

    # Retry connection jika container postgres baru menyala
    max_retries = 10
    for attempt in range(max_retries):
        try:
            with engine.connect():
                print("[LOAD] Koneksi database berhasil.")
                break
        except Exception as e:
            print(f"[LOAD] Menunggu database siap... (percobaan {attempt+1}/{max_retries})")
            time.sleep(3)
    else:
        raise ConnectionError("Gagal terhubung ke database setelah beberapa percobaan.")

    print(f"[LOAD] Memasukkan data ke tabel '{table_name}'...")
    df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
    print(f"[LOAD] Sukses! Data berhasil dimuat ke tabel '{table_name}'.")

def run_pipeline():
    print("=" * 50)
    print("MEMULAI ETL PIPELINE: KEPUASAN HIDUP KOMUTER")
    print("=" * 50)
    
    raw_data = extract(CSV_PATH)
    clean_data = transform(raw_data)
    load(clean_data)
    
    print("=" * 50)
    print("PIPELINE SELESAI DENGAN SUKSES!")
    print("=" * 50)

if __name__ == "__main__":
    run_pipeline()