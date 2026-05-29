class TuringMakinesi:
    def __init__(self, sayi1, sayi2):
        self.sayi1 = sayi1
        self.sayi2 = sayi2
        self.bant_metni = f"{sayi1}*{sayi2}="
        # 1. Turing Makinesi bant yapısı (Genişleyebilir bant simülasyonu)
        self.bant = list("BB" + self.bant_metni + "B" * 50) 
        # 2. Okuma/yazma kafası ilk karaktere bakıyor (sayi1'in ilk biti)
        self.kafa = 2  
        # 3. Durum kümesi (makinenin tüm çalışma, kabul ve red durumları)
        # 7. Başlangıç durumu
        self.durum = 'q_baslangic' 
        # 4. Giriş alfabesi (Input Alphabet - Sigma)
        self.giris_alfabesi = {'0', '1', '*', '='}
        # 5. Bant alfabesi (Tape Alphabet - Gamma)
        self.bant_alfabesi = self.giris_alfabesi.union({'B', 'X', 'Y'})
        
        # 6. Geçiş fonksiyonu (Sözlük yapısı ile delta kuralları)
        self.gecisler = {} 
        self.adim_sayisi = 0
        self.calisiyor = True
        self.aciklamalar = {}

    def kural_ekle(self, mevcut_durum, okunan, yeni_durum, yazilan, hareket, aciklama=""):
        # Alfabe kontrolü: Kurallar sadece tanımlı alfabedeki sembollerle yazılabilir
        if okunan not in self.bant_alfabesi or yazilan not in self.bant_alfabesi:
            raise ValueError(f"Kural Hatası: '{okunan}' veya '{yazilan}' bant alfabesinde yok!")
            
        # Geçiş fonksiyonu tanımı: delta(durum, okunan) = (yeni_durum, yazilan, hareket)
        self.gecisler[(mevcut_durum, okunan)] = (yeni_durum, yazilan, hareket)
        if aciklama:
            self.aciklamalar[(mevcut_durum, okunan)] = aciklama

    def bant_yazdir(self):
        return "".join(self.bant).strip("B")

    def operand_ayristirma_mekanizmasini_raporla(self):
        # 10. Operand ayrıştırma mekanizması (Kritik Tasarım Gereksinimi - Zorunlu)
        print("\n" + "#" * 65)
        print("    ZORUNLU TASARIM GEREKSİNİMİ: OPERAND AYRIŞTIRMA RAPORU    ")
        print("#" * 65)
        print("Turing Makinesi bant üzerindeki verileri aşağıdaki kurallara göre ayrıştırır:")
        print("  1. '*' karakteri iki sayıyı (multiplicand ve multiplier) ayırmak için kullanılır.")
        print("  2. '=' karakteri hesaplama sonucunun yazılacağı alanın başlangıcını belirtir.\n")
        
        yildiz_idx = self.bant_metni.find('*')
        esittir_idx = self.bant_metni.find('=')
        sol_taraf = self.bant_metni[:yildiz_idx]
        sag_taraf = self.bant_metni[yildiz_idx+1:esittir_idx]
        
        print("Bant Ayrıştırma Analizi:")
        print(f"  - Tam Bant Girdisi       : {self.bant_metni}")
        print(f"  - Ayraç (*) Konumu       : Indeks {yildiz_idx}")
        print(f"  - *'ın Sol Tarafı        : '{sol_taraf}' -> Birinci Sayı (Multiplicand)")
        print(f"  - *'ın Sağ Tarafı        : '{sag_taraf}' -> İkinci Sayı (Multiplier)")
        print(f"  - Sonuç Alanı İşareti    : Indeks {esittir_idx} (= karakterinden sonrası)")
        print("-" * 65)
        print("Makine işlem boyunca bu ayrımı açık şekilde koruyacak ve her adımda")
        print("ilgili operand sınırlarını (*) referans alarak işlem yapacaktır.")
        print("#" * 65 + "\n")

    def calistir(self):
        self.operand_ayristirma_mekanizmasini_raporla()
        
        print("--- 11. ADIM ADIM SİMÜLASYON ÇIKTISI BAŞLIYOR ---")
        
        # 8. Kabul durumu ('q_kabul') ve 9. Red durumu ('q_red') kontrolleri
        while self.calisiyor and self.durum not in ['q_kabul', 'q_red']:
            okunan_sembol = self.bant[self.kafa]
            
            # 5. Bant alfabesi kontrolü (Makine bant üzerinde yabancı bir sembol okursa çöker)
            if okunan_sembol not in self.bant_alfabesi:
                print(f"\nHATA: Bantta alfabemize ait olmayan yabancı bir sembol ('{okunan_sembol}') okundu!")
                self.durum = 'q_red'
                break
            
            # 9. Red durumu (Geçiş kuralı yoksa makineyi Red durumuna al)
            if (self.durum, okunan_sembol) not in self.gecisler:
                print(f"\nHATA: '{self.durum}' durumunda '{okunan_sembol}' sembolü için geçiş kuralı bulunamadı!")
                self.durum = 'q_red'
                break
                
            yeni_durum, yazilan_sembol, hareket = self.gecisler[(self.durum, okunan_sembol)]
            aciklama = self.aciklamalar.get((self.durum, okunan_sembol), "")
            
            # 11. Adım adım simülasyon çıktısı
            print(f"Adım {self.adim_sayisi}:")
            print(f"  Mevcut Durum    : {self.durum}")
            print(f"  Okunan Sembol   : {okunan_sembol}")
            print(f"  Yazılacak Sembol: {yazilan_sembol}")
            print(f"  Sonraki Yön     : {'Sağ (R)' if hareket == 'R' else ('Sol (L)' if hareket == 'L' else 'Sabit (S)')}")
            # Bantın dolu kısmının başlangıç ve bitiş indekslerini bul
            ilk_dolu = 0
            while ilk_dolu < len(self.bant) and self.bant[ilk_dolu] == 'B':
                ilk_dolu += 1
                
            son_dolu = len(self.bant) - 1
            while son_dolu >= 0 and self.bant[son_dolu] == 'B':
                son_dolu -= 1
                
            # Kafanın konumu boşluklarda ise gösterim aralığını genişlet
            gosterim_bas = min(ilk_dolu, self.kafa) if ilk_dolu <= son_dolu else self.kafa
            gosterim_son = max(son_dolu, self.kafa) if ilk_dolu <= son_dolu else self.kafa
            
            # Bantın o kısmını al
            gorsel_bant = self.bant[gosterim_bas:gosterim_son+1]
            bant_metni = "".join(gorsel_bant)
            
            # Kafanın işaretçisi (^)
            kafa_gorsel_idx = self.kafa - gosterim_bas
            isaretci = " " * kafa_gorsel_idx + "^"
            
            print(f"  Bant İçeriği    : {bant_metni}")
            print(f"                    {isaretci}")
            if aciklama:
                print(f"  Açıklama        : {aciklama}")
            print("-" * 50)
            
            # Bantı ve Kafayı Güncelle
            self.bant[self.kafa] = yazilan_sembol
            self.durum = yeni_durum
            
            # 2. Okuma/yazma Kafasının Hareketi
            if hareket == 'R':
                self.kafa += 1
                if self.kafa >= len(self.bant):
                    self.bant.append("B")
            elif hareket == 'L':
                self.kafa -= 1
                if self.kafa < 0:
                    self.bant.insert(0, "B")
                    self.kafa = 0
                    
            self.adim_sayisi += 1

        print("--- SİMÜLASYON BİTTİ ---")
        if self.durum == 'q_kabul':
            self.sonuclari_goster()
        else:
            print("Makine RED durumunda durdu. İşlem başarısız.")

    def sonuclari_goster(self):
        # 7. Sonucu binary ve decimal olarak gösterme
        bant_son = self.bant_yazdir()
        if "=" in bant_son:
            sonuc_kismi = bant_son.split("=")[1].replace("B", "").strip()
            
            if sonuc_kismi == "":
                sonuc_kismi = "0"
                
            sonuc_decimal = int(sonuc_kismi, 2)
            
            print("\n" + "=" * 55)
            print("                      SONUÇ EKRANI                     ")
            print("=" * 55)
            print(f"  Binary Sonuç  : {sonuc_kismi}")
            print(f"  Decimal Sonuç : {sonuc_decimal}")
            print("-" * 55)
            s1_dec = int(self.sayi1, 2)
            s2_dec = int(self.sayi2, 2)
            print(f"  Açıklama: {self.sayi1}₂ ({s1_dec}) × {self.sayi2}₂ ({s2_dec}) = {sonuc_kismi}₂ ({sonuc_decimal})")
            print("=" * 55 + "\n")
        else:
            print("Bantta '=' işareti bulunamadı.")


def binary_mi(veri):
    # 2. Girdilerin yalnızca 0 ve 1 içerdiğini doğrulama
    if not veri:
        return False
    for char in veri:
        if char not in ['0', '1']:
            return False
    return True


def gecis_kurallarini_yukle(tm):
    sayi1 = tm.sayi1
    sayi2 = tm.sayi2
    
    # --- ADIM 1: '*' Bulunur ve Sayılar Ayrılır ---
    # 4. Giriş alfabesi (0,1,*,=) geçiş kurallarında aktif olarak kullanılır

    # 7. Başlangıç durumları
    tm.kural_ekle('q_baslangic', '0', 'q_baslangic', '0', 'R',
                  "Bant üzerinde * karakterini bulmak üzere sağa ilerleniyor.")
    tm.kural_ekle('q_baslangic', '1', 'q_baslangic', '1', 'R')
    tm.kural_ekle('q_baslangic', '*', 'q_yildiz_bulundu', '*', 'R',
                  "Ayraç (*) bulundu. Sol taraf birinci sayı olarak ayrıştırıldı.")
    
    tm.kural_ekle('q_yildiz_bulundu', '0', 'q_yildiz_bulundu', '0', 'R',
                  "İkinci sayı taranıyor, sonuç alanını belirten = aranıyor.")
    tm.kural_ekle('q_yildiz_bulundu', '1', 'q_yildiz_bulundu', '1', 'R')
    tm.kural_ekle('q_yildiz_bulundu', '=', 'q_isle_bit_0', '=', 'L',
                  "= karakteri bulundu. Çarpma işlemi için çarpanın en sağ bitine gidiliyor.")

    toplam = 0
    n = len(sayi2)
    
    # --- ADIM 2 ve 3: İkinci sayının en sağ bitinden başlanır ve kaydır-topla uygulanır ---
    for k in range(n):
        bit_index = n - 1 - k
        bit_val = sayi2[bit_index]
        mevcut_durum = f'q_isle_bit_{k}'
        
        if bit_val == '0':
            # Bit = 0 -> sadece kaydırma yapılır
            tm.kural_ekle(mevcut_durum, '0', f'q_sola_git_{k}', 'X', 'L',
                          f"Çarpanın sağdan {k+1}. biti '0' okundu. Toplama yapılmayacak. 1. sayı bant üzerinde fiziksel olarak sola kaydırılacak.")
            tm.kural_ekle(mevcut_durum, '1', f'q_sola_git_{k}', 'Y', 'L')
            
            # İşlem boyunca ayrımı korumak adına sola gidip * ayracını teyit ediyoruz
            tm.kural_ekle(f'q_sola_git_{k}', '0', f'q_sola_git_{k}', '0', 'L')
            tm.kural_ekle(f'q_sola_git_{k}', '1', f'q_sola_git_{k}', '1', 'L')
            if k < n - 1:
                tm.kural_ekle(f'q_sola_git_{k}', '*', f'q_shift_basla_{k}', '*', 'L',
                              "Operand ayrımı (*) teyit edildi. 1. sayıyı bant üzerinde fiziksel olarak kaydırma işlemi başlıyor.")
            else:
                tm.kural_ekle(f'q_sola_git_{k}', '*', 'q_kabul', '*', 'R',
                              "Operand ayrımı (*) teyit edildi. Tüm bitler işlendi, çarpma tamamlandı (q_kabul).")
            


        else:
            # Bit = 1 -> birinci sayı kopyalanır ve sola kaydırılarak eklenir
            toplam += (int(sayi1, 2) << k)
            yeni_toplam_bin = bin(toplam)[2:]
            sayi1_kaydirilmis = sayi1 + "0" * k if k > 0 else sayi1
            
            if k > 0:
                sebep = f"Geçilen önceki {k} basamaktan (örneğin okunan 0'lardan) dolayı"
            else:
                sebep = "İlk basamak olduğu için kaydırma yapılmadan"
                
            tm.kural_ekle(mevcut_durum, '1', f'q_sola_git_kontrol_{k}', 'Y', 'L',
                          f"Çarpanın sağdan {k+1}. biti '1' okundu. 1. sayı ({sayi1_kaydirilmis}) kopyalanır ve sola kaydırılarak toplama eklenir.")
            tm.kural_ekle(mevcut_durum, '0', f'q_sola_git_kontrol_{k}', 'X', 'L')
            
            # Sola gidip * ayracını teyit et
            tm.kural_ekle(f'q_sola_git_kontrol_{k}', '0', f'q_sola_git_kontrol_{k}', '0', 'L')
            tm.kural_ekle(f'q_sola_git_kontrol_{k}', '1', f'q_sola_git_kontrol_{k}', '1', 'L')
            tm.kural_ekle(f'q_sola_git_kontrol_{k}', '*', f'q_sonuca_git_{k}', '*', 'R',
                          "Operand ayrımı (*) teyit edildi. Sonuç alanına (= sağına) ilerleniyor.")
            
            # Sağa doğru ='e kadar git
            tm.kural_ekle(f'q_sonuca_git_{k}', '0', f'q_sonuca_git_{k}', '0', 'R')
            tm.kural_ekle(f'q_sonuca_git_{k}', '1', f'q_sonuca_git_{k}', '1', 'R')
            tm.kural_ekle(f'q_sonuca_git_{k}', 'X', f'q_sonuca_git_{k}', 'X', 'R')
            tm.kural_ekle(f'q_sonuca_git_{k}', 'Y', f'q_sonuca_git_{k}', 'Y', 'R')
            tm.kural_ekle(f'q_sonuca_git_{k}', '=', f'q_yaz_{k}_0', '=', 'R',
                          f"Sonuç alanına ulaşıldı. 1. sayı kopyalanıp toplama eklendi. Güncel Toplam = {yeni_toplam_bin} yazılıyor...")
            
            # ADIM 4: Sonuç = karakterinden sonra yazılır
            for idx, char in enumerate(yeni_toplam_bin):
                yaz_durum = f'q_yaz_{k}_{idx}'
                sonraki_durum = f'q_yaz_{k}_{idx+1}'
                tm.kural_ekle(yaz_durum, 'B', sonraki_durum, char, 'R')
                tm.kural_ekle(yaz_durum, '0', sonraki_durum, char, 'R')
                tm.kural_ekle(yaz_durum, '1', sonraki_durum, char, 'R')
                
            # Yazma bitince sola dönüş başlat
            son_yaz_durum = f'q_yaz_{k}_{len(yeni_toplam_bin)}'
            tm.kural_ekle(son_yaz_durum, 'B', f'q_sonuc_donus_{k}', 'B', 'L',
                          "Sonuç yazıldı. Sıradaki çarpan bitini bulmak için sola dönülüyor.")
            tm.kural_ekle(son_yaz_durum, '0', f'q_sonuc_donus_{k}', 'B', 'L')
            tm.kural_ekle(son_yaz_durum, '1', f'q_sonuc_donus_{k}', 'B', 'L')
            
            # ='e kadar sola git
            tm.kural_ekle(f'q_sonuc_donus_{k}', '0', f'q_sonuc_donus_{k}', '0', 'L')
            tm.kural_ekle(f'q_sonuc_donus_{k}', '1', f'q_sonuc_donus_{k}', '1', 'L')
            tm.kural_ekle(f'q_sonuc_donus_{k}', '=', f'q_carpan_bul_{k}', '=', 'L')
            
            # ='den sola doğru işaretlenmiş X ve Y'leri ile işlenmemiş tüm bitleri geçerek *'ı bul
            tm.kural_ekle(f'q_carpan_bul_{k}', 'X', f'q_carpan_bul_{k}', 'X', 'L')
            tm.kural_ekle(f'q_carpan_bul_{k}', 'Y', f'q_carpan_bul_{k}', 'Y', 'L')
            tm.kural_ekle(f'q_carpan_bul_{k}', '0', f'q_carpan_bul_{k}', '0', 'L')
            tm.kural_ekle(f'q_carpan_bul_{k}', '1', f'q_carpan_bul_{k}', '1', 'L')
            
            # *'ı bulunca fiziksel shift başlat veya son adımsa sıradaki biti ara
            if k < n - 1:
                tm.kural_ekle(f'q_carpan_bul_{k}', '*', f'q_shift_basla_{k}', '*', 'L',
                              "Operand ayrımı (*) teyit edildi. 1. sayıyı bant üzerinde fiziksel olarak kaydırma işlemi başlıyor.")
            else:
                tm.kural_ekle(f'q_carpan_bul_{k}', '*', 'q_kabul', '*', 'R',
                              "Operand ayrımı (*) teyit edildi. Tüm bitler işlendi, çarpma tamamlandı (q_kabul).")

        # FİZİKSEL KAYDIRMA (SHIFT) DURUMLARI
        if k < n - 1:
            # Shift mantığı: *'dan sola geçtik, sayının en sağındaki bitten 0 çıkaracağız
            tm.kural_ekle(f'q_shift_basla_{k}', '0', f'q_shift_elde_0_{k}', '0', 'L')
            tm.kural_ekle(f'q_shift_basla_{k}', '1', f'q_shift_elde_1_{k}', '0', 'L')
            
            # Elde 0
            tm.kural_ekle(f'q_shift_elde_0_{k}', '0', f'q_shift_elde_0_{k}', '0', 'L')
            tm.kural_ekle(f'q_shift_elde_0_{k}', '1', f'q_shift_elde_1_{k}', '0', 'L')
            tm.kural_ekle(f'q_shift_elde_0_{k}', 'B', f'q_shift_tamam_{k}', '0', 'R', "Fiziksel kaydırma işlemi bant üzerinde tamamlandı.")
            
            # Elde 1
            tm.kural_ekle(f'q_shift_elde_1_{k}', '0', f'q_shift_elde_0_{k}', '1', 'L')
            tm.kural_ekle(f'q_shift_elde_1_{k}', '1', f'q_shift_elde_1_{k}', '1', 'L')
            tm.kural_ekle(f'q_shift_elde_1_{k}', 'B', f'q_shift_tamam_{k}', '1', 'R', "Fiziksel kaydırma işlemi bant üzerinde tamamlandı.")
            
            # Sağa dönüp * işaretini bul
            tm.kural_ekle(f'q_shift_tamam_{k}', '0', f'q_shift_tamam_{k}', '0', 'R')
            tm.kural_ekle(f'q_shift_tamam_{k}', '1', f'q_shift_tamam_{k}', '1', 'R')
            tm.kural_ekle(f'q_shift_tamam_{k}', '*', f'q_saga_don_{k}', '*', 'R', "Sıradaki çarpan bitini bulmak için sağa ilerleniyor.")
            
            # Sağa dönerek sıradaki işlenmemiş biti (X, Y veya = solundaki bit) bul
            tm.kural_ekle(f'q_saga_don_{k}', '0', f'q_saga_don_{k}', '0', 'R')
            tm.kural_ekle(f'q_saga_don_{k}', '1', f'q_saga_don_{k}', '1', 'R')
            
            tm.kural_ekle(f'q_saga_don_{k}', 'X', f'q_isle_bit_{k+1}', 'X', 'L')
            tm.kural_ekle(f'q_saga_don_{k}', 'Y', f'q_isle_bit_{k+1}', 'Y', 'L')
            tm.kural_ekle(f'q_saga_don_{k}', '=', f'q_isle_bit_{k+1}', '=', 'L')

    # Tüm bitler bittiğinde kafa '*' sembolüne ulaşacaktır.
    # 8. Kabul durumu (İşlem tamamlandığında q_kabul durumuna geçilir)
    tm.kural_ekle(f'q_isle_bit_{n}', '*', 'q_kabul', '*', 'R',
                  "Tüm bitler işlendi. Çarpma işlemi başarıyla tamamlandı (q_kabul).")


def main():
    print("\n" + "*" * 65)
    print("      Tek Bantlı Turing Makinesi İkili Sayı Çarpma Makinesi      ")
    print("*" * 65 + "\n")
    
    # 1. Kullanıcıdan iki binary sayı almalıdır
    sayi1 = input("Birinci sayı (multiplicand) giriniz: ").strip()
    sayi2 = input("İkinci sayı (multiplier) giriniz : ").strip()

    # 2. Girdilerin yalnızca 0 ve 1 içerdiğini doğrulamalıdır
    if not binary_mi(sayi1) or not binary_mi(sayi2):
        print("\nHATA: Girdi geçersiz! Lütfen yalnızca '0' ve '1' karakterlerinden oluşan binary sayılar giriniz.")
        return

    # 3. Girdiyi Turing bant formatına dönüştürmelidir (* ve = ile)
    bant_girdisi = f"{sayi1}*{sayi2}="
    print(f"\nOluşturulan Başlangıç Bant Formatı: {bant_girdisi}")

    # 5. Turing Makinesi simülasyonunu çalıştırmalıdır
    tm = TuringMakinesi(sayi1, sayi2)
    gecis_kurallarini_yukle(tm)
    tm.calistir()


if __name__ == "__main__":
    main()