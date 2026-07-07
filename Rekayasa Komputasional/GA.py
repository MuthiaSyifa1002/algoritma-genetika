import random

KAMUS = {
    "inaaa": "Ibu",
    "ambe": "Bapak",
    "moico": "Bagus",
    "miano": "Orang",
    "anaa": "Anak",
    "moko": "Mau",
    "osie": "Sana",
    "wuta": "Tanah",
    "urai": "Adik",
    "die": "Sini"
}

ALFABET = "abcdefghijklmnopqrstuvwxyz"
UKURAN_POPULASI = 8
PROB_MUTASI = 0.8

target = ""
generasi = 0
populasi = []
fitness = []
probabilitas = []
kumulatif = []
detail_seleksi = []
mating_pool = []
detail_crossover = []
anak_crossover = []
detail_mutasi = []
anak_mutasi = []


def buat_populasi_awal():
    global populasi, generasi
    populasi = ["".join(random.choice(ALFABET) for _ in range(len(target)))
                for _ in range(UKURAN_POPULASI)]
    generasi = 1


def hitung_fitness_individu(individu):
    cocok = sum(1 for i in range(len(target)) if individu[i] == target[i])
    return cocok, cocok / len(target)


def tabel_cocok(individu):
    print("  Posisi | Target | Individu | Cocok?")
    for j in range(len(target)):
        cocok = "Ya" if individu[j] == target[j] else "Tidak"
        print(f"  {j+1:<6} | {target[j]:<6} | {individu[j]:<8} | {cocok}")


def evaluasi_fitness(cetak=False):
    global fitness
    fitness = []
    if cetak:
        print(f"\nPERHITUNGAN FITNESS (GENERASI {generasi})")
        print(f"Target : {target}")
        print("Rumus  : Fitness = Jumlah huruf benar / Panjang kata")
        print(f"Karena panjang kata = {len(target)}, maka: Fitness = Jumlah huruf benar / {len(target)}")
        print("-" * 60)
    for i, ind in enumerate(populasi, 1):
        cocok, nilai = hitung_fitness_individu(ind)
        fitness.append(nilai)
        if cetak:
            print(f"Individu {i} (I{i}): {ind}")
            tabel_cocok(ind)
            print(f"  Jumlah huruf benar : {cocok}")
            print(f"  Fitness(I{i}) = {cocok}/{len(target)} = {nilai:.2f}")
            print()
    if cetak:
        print("Tabel Rekap Fitness:")
        print("Individu | Kromosom | Huruf Benar | Fitness")
        for i, ind in enumerate(populasi, 1):
            cocok, nilai = hitung_fitness_individu(ind)
            print(f"I{i:<7} | {ind:<8} | {cocok:<11} | {nilai:.2f}")
        rincian = " + ".join(f"{f:.2f}" for f in fitness)
        print(f"Total fitness:")
        print(f"Sigma Fitness = {rincian} = {sum(fitness):.2f}")


def seleksi_roulette(cetak=False):
    global probabilitas, kumulatif, detail_seleksi, mating_pool
    total = sum(fitness)
    if total == 0:
        probabilitas = [1 / len(populasi)] * len(populasi)
    else:
        probabilitas = [f / total for f in fitness]
    kumulatif = []
    jumlah = 0
    for p in probabilitas:
        jumlah += p
        kumulatif.append(jumlah)
    if cetak:
        print(f"\nSELEKSI ROULETTE WHEEL (GENERASI {generasi})")
        print("Keterangan simbol:")
        print("  Pi                = probabilitas individu ke-i terpilih")
        print("  Fitness(hi)       = fitness individu ke-i")
        print("  Sigma Fitness(hj) = jumlah seluruh fitness populasi")
        print("  n                 = jumlah individu dalam populasi")
        print()
        print("Langkah 1: Jumlah fitness")
        rincian = " + ".join(f"{f:.2f}" for f in fitness)
        print(f"  Sigma Fitness(hj) = {rincian} = {total:.2f}")
        print(f"  n = {len(populasi)}")
        print()
        print("Langkah 2: Hitung peluang masing-masing individu")
        print("  Rumus: Pi = Fitness(hi) / Sigma Fitness(hj)")
        for i in range(len(populasi)):
            print(f"  P{i+1} = {fitness[i]:.2f}/{total:.2f} = {probabilitas[i]:.2f}")
        print()
        print("Langkah 3: Probabilitas kumulatif (Ci = C(i-1) + Pi) dan interval")
        print("Individu | Fitness | Probabilitas | Prob. Kumulatif | Interval")
        batas_bawah = 0.0
        for i in range(len(populasi)):
            print(f"{i+1:<8} | {fitness[i]:.2f}    | {probabilitas[i]:.2f}         | {kumulatif[i]:.2f}            | {batas_bawah:.2f} - {kumulatif[i]:.2f}")
            batas_bawah = kumulatif[i]
        print()
        print("Langkah 4: Bangkitkan bilangan acak r (0-1)")
        print("Jika C(i-1) <= r < Ci maka individu ke-i terpilih")
    detail_seleksi = []
    mating_pool = []
    for putaran in range(UKURAN_POPULASI):
        r = random.random()
        idx = 0
        for i, c in enumerate(kumulatif):
            if r <= c:
                idx = i
                break
        detail_seleksi.append((r, idx))
        mating_pool.append(populasi[idx])
        if cetak:
            batas_bawah = kumulatif[idx - 1] if idx > 0 else 0.0
            print(f"  r{putaran+1} = {r:.2f}")
            print(f"  Karena {batas_bawah:.2f} <= {r:.2f} < {kumulatif[idx]:.2f} maka yang dipilih adalah Individu {idx+1} ({populasi[idx]})")
    if cetak:
        print()
        print("Urutan Individu Terpilih:")
        print("Putaran ke- | Bilangan Acak (r) | Interval    | Individu Terpilih")
        for putaran, (r, idx) in enumerate(detail_seleksi, 1):
            batas_bawah = kumulatif[idx - 1] if idx > 0 else 0.0
            print(f"{putaran:<11} | {r:.2f}              | {batas_bawah:.2f} - {kumulatif[idx]:.2f} | Individu {idx+1}")
        print(f"Hasil Seleksi (mating pool): {mating_pool}")


def crossover(cetak=False):
    global detail_crossover, anak_crossover
    detail_crossover = []
    anak_crossover = []
    if cetak:
        print(f"\nPROSES CROSS OVER / PINDAH SILANG (GENERASI {generasi})")
        print("Metode: One-Point Crossover (pertukaran gen secara langsung)")
        print("Child 1 = bagian awal Parent 1 + bagian akhir Parent 2")
        print("Child 2 = bagian awal Parent 2 + bagian akhir Parent 1")
        print("-" * 60)
    for i in range(0, len(mating_pool) - 1, 2):
        p1 = mating_pool[i]
        p2 = mating_pool[i + 1]
        titik = random.randint(1, len(target) - 1)
        c1 = p1[:titik] + p2[titik:]
        c2 = p2[:titik] + p1[titik:]
        detail_crossover.append((p1, p2, titik, c1, c2))
        anak_crossover.extend([c1, c2])
        if cetak:
            print(f"Pasangan {i//2 + 1}:")
            print(f"  Misalkan titik potong setelah gen ke-{titik}.")
            print(f"  Parent 1 : {p1[:titik]} | {p1[titik:]}")
            print(f"  Parent 2 : {p2[:titik]} | {p2[titik:]}")
            print("  Bagian setelah titik potong ditukar.")
            print(f"  Child 1  : {p1[:titik]} | {p2[titik:]} = {c1}")
            print(f"  Child 2  : {p2[:titik]} | {p1[titik:]} = {c2}")
            print()
    if len(mating_pool) % 2 == 1:
        anak_crossover.append(mating_pool[-1])


def mutasi(cetak=False):
    global detail_mutasi, anak_mutasi
    detail_mutasi = []
    anak_mutasi = []
    if cetak:
        print(f"\nPROSES MUTASI GEN (GENERASI {generasi})")
        print(f"probMut (probabilitas mutasi yang ditetapkan) = {PROB_MUTASI}")
        print("Jika p < probMut maka mutasi dilakukan, jika tidak maka individu tetap.")
        print("-" * 60)
    for i, anak in enumerate(anak_crossover, 1):
        p = random.random()
        if p < PROB_MUTASI:
            posisi = random.randrange(len(anak))
            gen_lama = anak[posisi]
            gen_baru = random.choice(ALFABET)
            hasil = anak[:posisi] + gen_baru + anak[posisi + 1:]
            detail_mutasi.append((anak, posisi, gen_lama, gen_baru, hasil))
            anak_mutasi.append(hasil)
            if cetak:
                print(f"Child {i}: p = {p:.2f}")
                print(f"  Karena p = {p:.2f} < probMut = {PROB_MUTASI} -> mutasi dilakukan")
                print(f"  R = {posisi + 1} (posisi gen yang dipilih secara acak)")
                print(f"  Individu sebelum mutasi : {anak}")
                print(f"  Gen ke-{posisi + 1} ('{gen_lama}') diganti huruf acak baru '{gen_baru}'")
                print(f"  Individu setelah mutasi : {hasil}")
                print()
        else:
            detail_mutasi.append((anak, -1, "-", "-", anak))
            anak_mutasi.append(anak)
            if cetak:
                print(f"Child {i}: p = {p:.2f}")
                print(f"  Karena p = {p:.2f} >= probMut = {PROB_MUTASI} -> individu tetap tanpa mutasi ({anak})")
                print()


def bentuk_generasi_baru(cetak=False):
    global populasi, generasi
    terbaik = populasi[fitness.index(max(fitness))]
    fitness_anak = [hitung_fitness_individu(a)[1] for a in anak_mutasi]
    idx_terburuk = fitness_anak.index(min(fitness_anak))
    populasi_baru = anak_mutasi[:]
    populasi_baru[idx_terburuk] = terbaik
    populasi = populasi_baru
    generasi += 1
    if cetak:
        print(f"\nEVALUASI POPULASI BARU (GENERASI {generasi})")
        print(f"(Elitisme: individu terbaik '{terbaik}' dipertahankan menggantikan anak terburuk)")
        print(f"Target: {target}")
        print("-" * 60)
        for i, ind in enumerate(populasi, 1):
            cocok, nilai = hitung_fitness_individu(ind)
            print(f"Child/Individu {i}: {ind}")
            tabel_cocok(ind)
            print(f"  Fitness({ind}) = {cocok}/{len(target)} = {nilai:.2f}")
            print()
        print("Tabel Rekap Populasi Baru:")
        print("Individu | Kromosom | Huruf Benar | Fitness")
        for i, ind in enumerate(populasi, 1):
            cocok, nilai = hitung_fitness_individu(ind)
            print(f"I{i:<7} | {ind:<8} | {cocok:<11} | {nilai:.2f}")
        nilai_terbaik = max(hitung_fitness_individu(ind)[1] for ind in populasi)
        if nilai_terbaik == 1.0:
            print("Karena fitness = 1, maka kata target sudah ditemukan.")
        else:
            print(f"Fitness terbaik = {nilai_terbaik:.2f} (belum 1.00), evolusi dapat dilanjutkan.")
    evaluasi_fitness(cetak=False)


def menu_1():
    print("\nDAFTAR KAMUS BAHASA MORONENE - INDONESIA")
    print("-" * 40)
    print("No | Moronene | Indonesia")
    print("-" * 40)
    for i, (moro, indo) in enumerate(KAMUS.items(), 1):
        print(f"{i:<2} | {moro:<8} | {indo}")
    print("-" * 40)


def menu_2():
    global target
    kata = input("Masukkan kata yang dicari: ").lower().strip()
    if kata in KAMUS:
        target = kata
        buat_populasi_awal()
        evaluasi_fitness(cetak=False)
        print(f"Kata '{kata}' ditemukan di kamus. Artinya: {KAMUS[kata]}")
        print(f"Target GA diset: '{target}' (panjang kromosom = {len(target)})")
        print("Populasi awal generasi 1 telah dibangkitkan.")
        return
    for moro, indo in KAMUS.items():
        if kata == indo.lower():
            target = moro
            buat_populasi_awal()
            evaluasi_fitness(cetak=False)
            print(f"Arti '{indo}' ditemukan. Kata Moronene: '{moro}'")
            print(f"Target GA diset: '{target}' (panjang kromosom = {len(target)})")
            print("Populasi awal generasi 1 telah dibangkitkan.")
            return
    print("Kata tidak ditemukan di dalam kamus.")


def menu_3():
    if not target:
        print("Peringatan: tentukan kata target dulu di menu 2!")
        return
    buat_populasi_awal()
    evaluasi_fitness(cetak=False)
    print(f"\nMENJALANKAN ALGORITMA GENETIKA | Target: {target}")
    print("Populasi awal:")
    for i, ind in enumerate(populasi, 1):
        print(f"  I{i} : {ind}")
    print("\nProses evolusi (dicetak saat fitness terbaik meningkat):")
    fitness_terbaik = -1
    while True:
        nilai_max = max(fitness)
        individu_terbaik = populasi[fitness.index(nilai_max)]
        if nilai_max > fitness_terbaik:
            fitness_terbaik = nilai_max
            print(f"Generasi {generasi:<4} | Terbaik: {individu_terbaik} | Fitness: {nilai_max:.4f}")
        if nilai_max == 1.0:
            print(f"\nSOLUSI DITEMUKAN pada generasi {generasi}!")
            print(f"Kata Moronene : {individu_terbaik}")
            print(f"Arti          : {KAMUS[individu_terbaik]}")
            break
        seleksi_roulette(cetak=False)
        crossover(cetak=False)
        mutasi(cetak=False)
        bentuk_generasi_baru(cetak=False)


def menu_4():
    if not populasi:
        print("Peringatan: populasi kosong, cari kata dulu di menu 2!")
        return
    print(f"\nPOPULASI GENERASI {generasi} (Target: {target})")
    print("-" * 40)
    for i, ind in enumerate(populasi, 1):
        print(f"I{i} : {ind}")


def menu_5():
    if not populasi:
        print("Peringatan: populasi kosong, cari kata dulu di menu 2!")
        return
    evaluasi_fitness(cetak=True)


def menu_6():
    if not fitness:
        print("Peringatan: hitung fitness dulu di menu 5!")
        return
    seleksi_roulette(cetak=True)


def menu_7():
    if not mating_pool:
        print("Peringatan: lakukan seleksi dulu di menu 6!")
        return
    crossover(cetak=True)


def menu_8():
    if not anak_crossover:
        print("Peringatan: lakukan crossover dulu di menu 7!")
        return
    mutasi(cetak=True)


def menu_9():
    if not anak_mutasi:
        print("Peringatan: lakukan mutasi dulu di menu 8!")
        return
    bentuk_generasi_baru(cetak=True)


def main():
    while True:
        print("\n==============================================")
        print("ALGORITMA GENETIKA - KAMUS BAHASA MORONENE")
        print("==============================================")
        print("1.  Tampilkan Kamus")
        print("2.  Cari Kata")
        print("3.  Jalankan Algoritma Genetika")
        print("4.  Tampilkan Populasi")
        print("5.  Hasil Fitness")
        print("6.  Seleksi Roulette")
        print("7.  Cross Over")
        print("8.  Mutasi")
        print("9.  Generasi Baru")
        print("10. Keluar")
        pilih = input("Pilih menu (1-10): ").strip()
        if pilih == "1":
            menu_1()
        elif pilih == "2":
            menu_2()
        elif pilih == "3":
            menu_3()
        elif pilih == "4":
            menu_4()
        elif pilih == "5":
            menu_5()
        elif pilih == "6":
            menu_6()
        elif pilih == "7":
            menu_7()
        elif pilih == "8":
            menu_8()
        elif pilih == "9":
            menu_9()
        elif pilih == "10":
            print("Program selesai. Terima kasih.")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()
