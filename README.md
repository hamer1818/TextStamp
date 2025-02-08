# TextStamp

TextStamp, resimleriniz üzerine özelleştirilmiş metin damgaları eklemenizi sağlayan kullanıcı dostu bir masaüstü uygulamasıdır.

## Özellikler

- Sürükle-bırak ile kolay alan seçimi
- Otomatik font boyutlandırma
- Birden fazla metin desteği
- Özelleştirilebilir font desteği
- Çoklu çıktı oluşturma
- Kullanıcı dostu arayüz
- Dahili öğretici sistem
- Scroll desteği ile büyük resimler için uygun görüntüleme

## Kurulum

1. Python 3.x'in kurulu olduğundan emin olun

```bash
python --version
```

2. Bu depoyu klonlayın:

```bash
git clone https://github.com/hamer1818/TextStamp.git
```
3. virtual environment oluşturun:

```bash
python -m venv venv
```

4. Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

## Kullanım

1. Uygulamayı çalıştırın:

```bash
python main.py
```


## Kullanım

1. "Resim Yükle" butonu ile bir resim seçin
2. Fare ile sürükleyerek metin eklemek istediğiniz alanı belirleyin
3. "Bölgeyi Onayla" butonuna tıklayın
4. Metin kutusuna eklemek istediğiniz metni yazın
5. "Metin Ekle" butonuna tıklayın
6. İsterseniz birden fazla metin ekleyebilirsiniz
7. "Metinleri Uygula ve Çıktı Al" butonu ile sonuçları kaydedin

## Özelleştirme

### Font Değiştirme
- `fonts` klasörü içine `main.ttf` adında bir TrueType font dosyası ekleyerek varsayılan fontu değiştirebilirsiniz
- Font bulunamazsa sistem varsayılan fontu kullanılacaktır

## Gereksinimler

- Python 3.x
- Pillow (PIL)
- tkinter (Python ile birlikte gelir)

## Klasör Yapısı
```plaintext
textStamp/
├── main.py
├── README.md
├── requirements.txt
└── fonts/
└── main.ttf (isteğe bağlı)
```

## Özellikler ve Sınırlamalar

- Desteklenen resim formatları: PNG, JPG, JPEG, GIF, BMP, PPM, PGM
- Maksimum font boyutu: 100pt
- Metin rengi: Siyah
- Çıktı formatı: PNG

## Sorun Giderme

1. Font Bulunamadı Hatası
   - `fonts` klasörünün varlığını kontrol edin
   - `main.ttf` dosyasının doğru konumda olduğunu kontrol edin

2. Resim Yüklenmiyor
   - Desteklenen formatta olduğundan emin olun
   - Dosya boyutunun çok büyük olmadığından emin olun

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

## İletişim

Sorularınız ve önerileriniz için bir Issue oluşturabilirsiniz.

## Sürüm Geçmişi

- v1.0 (2024)
  - İlk sürüm
  - Temel metin ekleme özellikleri
  - Öğretici sistem
  - Çoklu metin desteği