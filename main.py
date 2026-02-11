# main.py
import streamlit as st
import rules_kor
import rules_kp

# Fungsi Helper untuk menampilkan hasil warning
def display_validation(results):
    if not results:
        st.success("✅ Tidak ditemukan warning/anomali pada data yang diinput.")
    else:
        for res in results:
            if res['type'] == 'error':
                st.error(res['msg'])
            elif res['type'] == 'warning':
                st.warning(res['msg'])
            else:
                st.info(res['msg'])

# Setup Halaman
st.set_page_config(page_title="Validasi SUSENAS 2026", layout="wide")
st.title("🕵️ Validator Digital SUSENAS 2026")

# Sidebar
menu = st.sidebar.radio("Pilih Blok Pemeriksaan:", 
    ["1. Kependudukan (KOR)", "2. Pendidikan (KOR)", "3. Ketenagakerjaan (KOR)",
     "4. KP: Pendidikan & Kesehatan", "5. KP: Teknologi & Keuangan", "6. KP: Konsumsi"])

st.header(f"Validasi: {menu}")
st.divider()

# --- LOGIC INPUT & CALL RULES ---

if menu == "1. Kependudukan (KOR)":
    col1, col2 = st.columns(2)
    with col1:
        r403 = st.selectbox("R403 - Hubungan KRT", [1, 2, 3, 4, 5], format_func=lambda x: "1. KRT" if x==1 else str(x))
        r407 = st.number_input("R407 - Umur", 0, 120, 30)
        jml_keluarga = st.number_input("Jml Keluarga", 1, 10, 1)
        r508 = st.selectbox("R508 - Punya KTP?", [1, 2], format_func=lambda x: "2. Ya" if x==2 else "1. Tidak")
        r404 = st.selectbox("R404 - Status Kawin", [1, 2, 3, 4], format_func=lambda x: {1:"Belum", 2:"Kawin", 3:"C.Hidup", 4:"C.Mati"}[x])
        r409 = st.number_input("R409 - Umur Kawin Pertama", 0, 99, 0)
    
    with col2:
        # Panggil Fungsi dari rules_kor.py
        hasil = rules_kor.cek_kependudukan(r403, r407, r508, r404, r409, jml_keluarga)
        display_validation(hasil)

elif menu == "2. Pendidikan (KOR)":
    col1, col2 = st.columns(2)
    with col1:
        r407 = st.number_input("R407 - Umur", 0, 100, 10)
        r610 = st.selectbox("R610 - Status Sekolah", [1, 2, 3])
        r612 = st.selectbox("R612 - Jenjang", ["SD/Paket A", "SMP/Paket B", "SMA/Paket C", "SLB", "Lainnya"])
        kelas_ini = st.number_input("Kelas Saat Ini", 0, 12, 1)
        kelas_lalu = st.number_input("Kelas Tahun Lalu", 0, 12, 0)
        r608 = st.selectbox("R608 - Baca Tulis (5=Buta Huruf)", [1, 5])
        disabilitas = st.checkbox("Ada Disabilitas di Blok X?")
        
    with col2:
        hasil = rules_kor.cek_pendidikan(r407, r610, r612, kelas_ini, kelas_lalu, r608, disabilitas)
        display_validation(hasil)

elif menu == "3. Ketenagakerjaan (KOR)":
    col1, col2 = st.columns(2)
    with col1:
        r407 = st.number_input("R407 - Umur", 0, 100, 20)
        r706 = st.selectbox("R706 - Status Kerja", [1, 2, 3, 4], format_func=lambda x: "3. Berusaha + Buruh Tetap" if x==3 else "Lainnya")
        r1901a = st.radio("Sumber Biaya Utama", ["1. Pekerjaan", "Lainnya"])
        art_bekerja = st.number_input("Jml ART Bekerja", 0, 10, 1)
        
    with col2:
        hasil = rules_kor.cek_ketenagakerjaan(r407, r706, r1901a, art_bekerja, "A")
        display_validation(hasil)

elif menu == "4. KP: Pendidikan & Kesehatan":
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Pendidikan")
        sekolah_bos = st.checkbox("Ada Sekolah Penerima BOS?")
        r293 = st.number_input("Biaya SPP (R293)", 0)
        anak_paud = st.checkbox("Ada Anak PAUD?")
        biaya_paud = st.number_input("Biaya PAUD", 0)
        st.caption("Kesehatan")
        bpjs_pbi = st.checkbox("Ada BPJS PBI (Gratis)?")
        r338 = st.number_input("Biaya Premi (R338)", 0)
        bayi_0th = st.checkbox("Ada Bayi 0 Th?")
        biaya_lahir = st.number_input("Biaya Melahirkan", 0)
        
    with col2:
        hasil = rules_kp.cek_kp_pendidikan_kesehatan(sekolah_bos, r293, anak_paud, biaya_paud, bpjs_pbi, r338, bayi_0th, biaya_lahir, False, 0)
        display_validation(hasil)

elif menu == "5. KP: Teknologi & Keuangan":
    col1, col2 = st.columns(2)
    with col1:
        pakai_hp = st.checkbox("Pakai HP/Internet?")
        biaya_hp = st.number_input("Biaya Pulsa/Data", 0)
        punya_rek = st.checkbox("Punya Rekening?")
        adm_bank = st.number_input("Biaya Admin Bank", 0)
        terima_pip = st.checkbox("Terima PIP Tunai?")
        blok_ve = st.number_input("Nilai Bantuan Pemerintah (Blok V.E)", 0)
        
    with col2:
        hasil = rules_kp.cek_kp_teknologi(pakai_hp, biaya_hp, punya_rek, adm_bank, terima_pip, blok_ve)
        display_validation(hasil)

elif menu == "6. KP: Konsumsi":
    col1, col2 = st.columns(2)
    with col1:
        balita_no_asi = st.checkbox("Balita Tidak ASI?")
        biaya_susu = st.number_input("Biaya Susu Balita", 0)
        rokok = st.number_input("Biaya Rokok", 0)
        kayu_bakar = st.number_input("Biaya Kayu Bakar", 0)
        korek = st.number_input("Biaya Korek Api", 0)
        wanita_subur = st.checkbox("Ada Wanita 10-54th?")
        pembalut = st.number_input("Biaya Pembalut", 0)
        pam = st.number_input("Biaya PAM", 0)
        listrik = st.number_input("Biaya Listrik", 0)
        
    with col2:
        hasil = rules_kp.cek_kp_konsumsi(balita_no_asi, biaya_susu, rokok, kayu_bakar, korek, wanita_subur, pembalut, pam, listrik)
        display_validation(hasil)