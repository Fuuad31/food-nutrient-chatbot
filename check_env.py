# check_env.py
import os
from dotenv import load_dotenv

print("--- Memulai Tes Akses .env ---")

# Memanggil fungsi untuk memuat file .env
# Jika file .env ada di folder yang sama, ini seharusnya berhasil.
success = load_dotenv()

if success:
    print("✅ Pustaka python-dotenv berhasil menemukan dan memuat file .env.")
else:
    print("❌ GAGAL: Pustaka python-dotenv TIDAK dapat menemukan file .env.")
    print("--- Tes Selesai (GAGAL) ---")
    exit() # Hentikan skrip di sini jika file tidak ditemukan

# Sekarang, coba baca variabelnya dari environment
api_key = os.getenv("GOOGLE_API_KEY")

print("\n--- Membaca Variabel ---")
if api_key:
    print(f"✅ BERHASIL: Variabel GOOGLE_API_KEY ditemukan.")
    print(f"   Isinya dimulai dengan: '{api_key[:5]}...'")
else:
    print("❌ GAGAL: Variabel GOOGLE_API_KEY TIDAK ditemukan di environment.")
    print("   Ini berarti file .env Anda mungkin kosong atau nama variabelnya salah.")

print("--- Tes Selesai ---")