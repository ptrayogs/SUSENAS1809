# rules_kor.py

def cek_kependudukan(r403, r407, r508, r404, r409, jml_keluarga):
    results = []
    
    # W-KOR-01: KRT Umur < 15 atau > 70 [cite: 2]
    if r403 == 1 and (r407 < 15 or r407 > 70):
        results.append({"type": "error", "msg": f"W-KOR-01: KRT Umur {r407} tahun (<15 atau >70). Pastikan ART ini penanggung jawab utama."})
    
    # W-KOR-02: Jumlah Keluarga > 2 [cite: 2]
    if jml_keluarga > 2:
        results.append({"type": "warning", "msg": f"W-KOR-02: Ada {jml_keluarga} keluarga dalam 1 Ruta. Cek konsep 'Satu Dapur'."})
        
    # W-KOR-03: Umur < 17 punya KTP [cite: 2]
    if r407 < 17 and r508 == 2 and r404 == 1:
        results.append({"type": "error", "msg": "W-KOR-03: Umur < 17 dan Belum Kawin tapi punya KTP. Seharusnya KIA/KK."})
        
    # W-KOR-04: UKP tidak wajar [cite: 2]
    if r409 == 98 or (0 < r409 < 12):
        results.append({"type": "warning", "msg": f"W-KOR-04: UKP bernilai {r409}. Jika 98 (Tidak Tahu) lakukan probing, jika < 12 pastikan kebenarannya."})

    # W-KOR-05: Cerai Mati Umur Muda [cite: 2]
    if r404 == 4 and r407 < 17:
        results.append({"type": "warning", "msg": f"W-KOR-05: Status 'Cerai Mati' tapi umur {r407} tahun. Sangat jarang."})
        
    return results

def cek_pendidikan(r407, r610, r612, kelas_ini, kelas_lalu, r608, disabilitas_blok_x):
    results = []
    
    # W-EDU-01: Umur vs Jenjang [cite: 4]
    msg = ""
    if r612 == "SD/Paket A" and (r407 < 6 or r407 > 13): msg = "W-EDU-01: Umur tidak wajar untuk SD (<6 atau >13)."
    elif r612 == "SMP/Paket B" and (r407 < 12 or r407 > 16): msg = "W-EDU-01: Umur tidak wajar untuk SMP (<12 atau >16)."
    elif r612 == "SMA/Paket C" and (r407 < 16 or r407 > 19): msg = "W-EDU-01: Umur tidak wajar untuk SMA (<16 atau >19)."
    if msg: results.append({"type": "warning", "msg": msg})

    # W-EDU-02: Lansia Sekolah [cite: 4]
    if r407 > 50 and r610 == 2:
        results.append({"type": "warning", "msg": "W-EDU-02: Umur > 50 tahun 'Masih Bersekolah'. Pastikan bukan kursus kilat/pengajian."})

    # W-EDU-03: SLB tanpa Disabilitas [cite: 4]
    if r612 == "SLB" and not disabilitas_blok_x:
        results.append({"type": "error", "msg": "W-EDU-03: Sekolah di SLB tapi Blok X tidak mencatat disabilitas."})

    # W-EDU-04: Tinggal Kelas [cite: 4]
    if (kelas_ini == kelas_lalu) and kelas_ini > 0:
        results.append({"type": "info", "msg": "W-EDU-04: Kelas tahun ini SAMA dengan tahun lalu. Konfirmasi tinggal kelas."})

    # W-EDU-05: Buta Huruf Kelas 5+ [cite: 4]
    if r612 == "SD/Paket A" and kelas_ini >= 5 and r608 == 5:
        results.append({"type": "error", "msg": "W-EDU-05: Anak SD Kelas 5 ke atas tapi Buta Huruf."})
        
    return results

def cek_ketenagakerjaan(r407, r706, r1901a, art_bekerja, kegiatan):
    results = []
    # W-LAB-01: Pekerja Anak Bos [cite: 6]
    if r407 < 18 and r706 == 3:
        results.append({"type": "error", "msg": "W-LAB-01: Pekerja Anak (<18 th) status Berusaha dgn Buruh Tetap. Cek kewajaran."})
    
    # W-LAB-02: Sumber Biaya vs Status Kerja [cite: 6]
    if r1901a == "1. Pekerjaan" and art_bekerja == 0:
        results.append({"type": "error", "msg": "W-LAB-02: Sumber biaya utama 'Pekerjaan', tapi TIDAK ADA ART yang bekerja."})
    
    return results