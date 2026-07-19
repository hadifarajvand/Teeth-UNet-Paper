# بازپیاده‌سازی مقاله IEEE AIIoT 2024 — سگمنتیشن دندان با U-Net

**زبان:** **فارسی** | [English](README.en.md)

این پروژه برای بازپیاده‌سازی مقاله‌ی زیر آماده شده است:

**Rohini Joshi, “Segmentation of Teeth in Panoramic X-ray Image Using U-net Algorithm,” IEEE AIIoT 2024.**

هدف پروژه این است که روند مقاله تا حد ممکن به‌صورت قابل‌اجرا و قابل‌بررسی در اختیار خواننده باشد؛ از آماده‌سازی دیتاست و آموزش مدل گرفته تا محاسبه‌ی معیارها و تولید خروجی‌های تصویری.

دو حالت اجرا در نظر گرفته شده است:

- **Smoke Mode** برای یک تست سریع و کامل از سالم بودن کل کد و پایپ‌لاین.
- **Paper Mode** برای اجرای اصلی روی دیتاست Tufts Dental Database و تولید خروجی‌های مربوط به مقاله.

---

## شروع سریع

ابتدا مخزن را دریافت کرده و محیط پایتون را آماده کنید:

```bash
git clone https://github.com/hadifarajvand/Teeth-UNet-Paper.git
cd Teeth-UNet-Paper

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

برای اجرای یک تست سریع:

```bash
make smoke
```

برای دانلود و آماده‌سازی دیتاست اصلی مقاله:

```bash
make datasets-tdd
```

و برای اجرای کامل Paper Mode:

```bash
make paper
```

---

## دانلود دیتاست‌ها

اسکریپت اصلی دیتاست‌ها را مستقیماً داخل همین repository آماده می‌کند:

```bash
python scripts/download_datasets.py --dataset all
```

یا با wrapper ساده‌تر:

```bash
bash download_datasets.sh --dataset all
```

ساختار داده‌ها بعد از آماده‌سازی به این شکل خواهد بود:

```text
data/
├── bootstrap_synthetic/          # دیتاست Smoke
├── tdd_download/                 # فایل‌های خام دانلودشده
├── tdd/                          # دیتاست آماده برای Paper Mode
│   ├── images/
│   └── masks/
└── open_reference_download/      # داده‌ی مرجع اختیاری
```

### فقط دیتاست اصلی مقاله

```bash
python scripts/download_datasets.py --dataset tdd
```

این فرمان دانلود، استخراج، پیدا کردن جفت‌های تصویر و Mask، آماده‌سازی ساختار نهایی و اعتبارسنجی دیتاست را انجام می‌دهد.

فایل‌های نهایی مورد استفاده‌ی آموزش در این مسیر قرار می‌گیرند:

```text
data/tdd/images/
data/tdd/masks/
```

برای اطمینان از اینکه دیتاست کامل و مناسب اجرای اصلی است، اسکریپت حداقل 900 جفت معتبر تصویر و Mask را بررسی می‌کند.

### دانلود مجدد از ابتدا

```bash
python scripts/download_datasets.py --dataset tdd --force
```

### استفاده از آرشیوی که از قبل دارید

اگر نسخه‌ی رسمی یا مجاز TDD را از قبل در اختیار دارید:

```bash
python scripts/download_datasets.py \
  --dataset tdd \
  --archive /absolute/path/to/tufts-dental-database.zip
```

---

## مسیرهای دریافت TDD

چون دسترسی به Tufts Dental Database ممکن است بسته به منبع یا نیاز به احراز هویت متفاوت باشد، downloader چند مسیر را به‌ترتیب امتحان می‌کند:

1. mirror کامل TDD روی Kaggle: `iftakharh/tufts-dental-datasetcustomized`
2. KaggleHub، Kaggle CLI یا API دانلود Kaggle
3. آرشیو رسمی Radiographهای Tufts
4. mirror فعال Radiographها: `manarmaged/tufts-radiographs`
5. Tooth Maskهای TDD از منبع عمومی مبتنی بر Tufts
6. تطبیق فایل‌ها با شناسه‌ی عددی اصلی تصاویر

اگر Kaggle نیاز به ورود داشته باشد، کافی است credential معمول Kaggle را روی سیستم تنظیم کرده و همان فرمان را دوباره اجرا کنید.

---

## Smoke Mode

Smoke Mode برای این است که بدون نیاز به دیتاست اصلی، مطمئن شویم کل پروژه از ابتدا تا انتها درست اجرا می‌شود.

```bash
make smoke
```

یا:

```bash
python scripts/run_pipeline.py smoke
```

در این اجرا مراحل اصلی شامل آموزش U-Net، محاسبه‌ی Dice و IoU، ذخیره‌ی checkpoint، prediction، post-processing و تولید Figureهای 1 تا 11 انجام می‌شود.

یک اجرای کامل Smoke قبلاً با همین کد انجام شده و نتیجه‌ی آن به شکل زیر بوده است:

- Dice: `0.9171192049980164`
- IoU: `0.846945196390152`
- Loss: `0.43136271834373474`

این نتایج فقط برای بررسی سالم بودن کد هستند و جایگزین نتیجه‌ی اجرای اصلی روی TDD محسوب نمی‌شوند.

---

## Paper Mode

برای اجرای اصلی مقاله:

```bash
make paper
```

یا:

```bash
python scripts/run_pipeline.py paper --download
```

این دستور به‌ترتیب کارهای زیر را انجام می‌دهد:

```text
دریافت و آماده‌سازی TDD
→ بررسی جفت‌های Image/Mask
→ ساخت Train/Validation/Test Manifest
→ آموزش U-Net با ورودی 512×512
→ محاسبه Loss، Dice و IoU
→ ذخیره Best Checkpoint
→ تولید Figureهای 1 تا 11
→ مقایسه نتایج با مقادیر گزارش‌شده در مقاله
```

---

## تنظیمات اصلی مدل

بر اساس اطلاعات منتشرشده در مقاله، تنظیمات اصلی Paper Mode به این شکل در نظر گرفته شده‌اند:

- مدل: `U-Net`
- Loss: `Binary Cross Entropy`
- Optimizer: `Adam`
- Learning Rate: `0.001`
- Epochs: `50`
- Input Size: `512×512`

مقادیر گزارش‌شده در مقاله تقریباً عبارت‌اند از:

- Dice ≈ `0.88`
- IoU ≈ `0.79`

بعضی جزئیات اجرایی مانند split دقیق داده‌ها، seed اصلی، checkpoint نویسندگان و تمام تنظیمات preprocessing در مقاله منتشر نشده‌اند. به همین دلیل هدف این repository یک بازپیاده‌سازی نزدیک و قابل‌بررسی از روش مقاله است، نه ادعای تطابق بیت‌به‌بیت با اجرای نویسندگان.

---

## خروجی‌ها

### Smoke Mode

```text
outputs/smoke/
├── metrics.json
├── history.csv
├── train_manifest.csv
├── validation_manifest.csv
├── test_manifest.csv
├── checkpoints/
│   └── best_model.pt
└── figures/
    ├── figure_01_unet_architecture.png
    ├── ...
    └── figure_11_contour_overlay.png
```

### Paper Mode

```text
outputs/paper/
├── metrics.json
├── history.csv
├── train_manifest.csv
├── validation_manifest.csv
├── test_manifest.csv
├── PAPER_COMPARISON.md
├── checkpoints/
│   └── best_model.pt
└── figures/
    ├── figure_01_unet_architecture.png
    ├── ...
    └── figure_11_contour_overlay.png
```

Figureهای اصلی شامل معماری U-Net، workflow، نمونه‌ی radiograph و mask، نمودارهای Dice/IoU، خروجی segmentation، post-processing، contour و اندازه‌گیری‌های پیکسلی هستند.

---

## اجرای همه مراحل

برای اجرای Smoke و سپس Paper Mode:

```bash
make all
```

یا:

```bash
python scripts/run_pipeline.py both --download
```

---

## بررسی خروجی نهایی

بعد از اجرای Paper Mode می‌توان کامل بودن خروجی‌ها را با این فرمان بررسی کرد:

```bash
python scripts/acceptance_check.py \
  --output-dir outputs/paper \
  --require-paper-data
```

این بررسی وجود checkpoint، metrics، manifests و Figureهای موردنیاز را کنترل می‌کند.

---

## فرمان‌های پرکاربرد

```bash
# نصب وابستگی‌ها
pip install -r requirements.txt

# دانلود همه دیتاست‌ها
make datasets

# فقط TDD
make datasets-tdd

# Smoke Test
make smoke

# اجرای اصلی مقاله
make paper

# اجرای همه مراحل
make all

# بسته‌بندی خروجی‌ها
make package
```

---

## فایل‌های مهم پروژه

- `README.md` — راهنمای اصلی فارسی
- `README.en.md` — نسخه‌ی انگلیسی
- `download_datasets.sh` — wrapper ساده برای دریافت دیتاست‌ها
- `scripts/download_datasets.py` — دانلود و آماده‌سازی دیتاست‌ها
- `scripts/run_pipeline.py` — اجرای Smoke و Paper Mode
- `scripts/reproduce_all.py` — آموزش، ارزیابی و تولید خروجی‌ها
- `docs/RUNBOOK.md` — راهنمای مرحله‌به‌مرحله‌ی فارسی
- `docs/RUNBOOK.en.md` — نسخه‌ی انگلیسی Runbook
- `docs/DATASETS.md` — توضیحات مربوط به دیتاست‌ها
- `docs/REPRODUCIBILITY_REPORT.md` — جزئیات بازتولیدپذیری پروژه

---

اگر فقط می‌خواهید سریع پروژه را بررسی کنید، `make smoke` بهترین نقطه‌ی شروع است. برای اجرای کامل مقاله، ابتدا `make datasets-tdd` و سپس `make paper` را اجرا کنید.

برای نسخه‌ی انگلیسی این راهنما: **[README.en.md](README.en.md)**
