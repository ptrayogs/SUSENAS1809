# rules_kp.py

def cek_kp_pendidikan_kesehatan(sekolah_bos, r293, anak_paud, biaya_paud, bpjs_pbi, r338, bayi_0th, biaya_lahir, imunisasi, biaya_imun):
    results = []
    
    # W-KP-01: BOS [cite: 15]
    if sekolah_bos and r293 < 10000:
        results.append({"type": "warning", "msg": "W-KP-01: Sekolah penerima BOS tapi SPP (R293) Kecil/Nol. Wajib IMPUTASI nilai BOS."})
    
    # W-KP-03: PAUD [cite: 15]
    if anak_paud and biaya_paud == 0:
        results.append({"type": "warning", "msg": "W-KP-03: Anak PAUD tapi Biaya (Alat tulis/seragam) NOL."})

    # W-KP-02: BPJS PBI [cite: 15]
    if bpjs_pbi and r338 == 0:
        results.append({"type": "error", "msg": "W-KP-02: Peserta BPJS PBI (Gratis) tapi R338 (Premi) NOL. Wajib IMPUTASI."})

    # W-KP-04: Biaya Lahir [cite: 15]
    if bayi_0th and biaya_lahir == 0:
        results.append({"type": "error", "msg": "W-KP-04: Bayi 0 Tahun tapi Biaya Melahirkan NOL. Jika Jampersal, wajib IMPUTASI."})
    
    return results

def cek_kp_teknologi(pakai_hp, biaya_hp, punya_rek, adm_bank, terima_pip, blok_ve):
    results = []
    # W-KP-07: Pulsa [cite: 17]
    if pakai_hp and biaya_hp == 0:
        results.append({"type": "error", "msg": "W-KP-07: Pakai HP/Internet tapi Biaya Pulsa/Data NOL."})
    
    # W-KP-08: Admin Bank [cite: 17]
    if punya_rek and adm_bank == 0:
        results.append({"type": "warning", "msg": "W-KP-08: Punya Rekening tapi Admin Bank NOL. Cek jenis tabungan."})

    # W-KP-09: PIP [cite: 17]
    if terima_pip and blok_ve == 0:
        results.append({"type": "error", "msg": "W-KP-09: Terima PIP tapi Blok V.E (Bantuan Pemerintah) KOSONG."})
        
    return results

def cek_kp_konsumsi(balita_no_asi, biaya_susu, rokok, kayu_bakar, korek, wanita_subur, pembalut, pam, listrik):
    results = []
    
    # W-KP-10: Susu [cite: 19]
    if balita_no_asi and biaya_susu == 0:
        results.append({"type": "warning", "msg": "W-KP-10: Balita tidak ASI tapi Biaya Susu NOL."})

    # W-KP-11 & 12: Rokok/Kayu vs Korek [cite: 19]
    if (rokok > 0 or kayu_bakar > 0) and korek == 0:
        results.append({"type": "error", "msg": "W-KP-11/12: Ada Pengeluaran Rokok/Kayu Bakar tapi Biaya Korek Api NOL."})

    # W-KP-13: Pembalut [cite: 19]
    if wanita_subur and pembalut == 0:
        results.append({"type": "error", "msg": "W-KP-13: Ada Wanita Usia Subur tapi Biaya Pembalut (R275) NOL."})

    # Outliers [cite: 44, 45, 46]
    if 0 < pam < 3000:
        results.append({"type": "warning", "msg": "Outlier: Biaya PAM < 3.000 (Sangat Kecil)."})
    if listrik > 1000000:
        results.append({"type": "warning", "msg": "Outlier: Listrik > 1 Juta. Pastikan bukan listrik usaha."})
    if kayu_bakar > 400000:
        results.append({"type": "warning", "msg": "Outlier: Kayu Bakar > 400.000."})
        
    return results