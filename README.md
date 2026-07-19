# بازپیاده‌سازی مقاله IEEE AIIoT 2024 — سگمنتیشن دندان با U-Net

**زبان:** **فارسی** | [English](README.en.md)

مقاله‌ی هدف:

**Rohini Joshi, “Segmentation of Teeth in Panoramic X-ray Image Using U-net Algorithm,” IEEE AIIoT 2024.**

این مخزن یک پکیج بازتولیدپذیر و قابل‌تحویل به کاربر است که دو حالت اجرای کاملاً جدا دارد:

- **Smoke Mode:** تست سریع و کامل کل پایپ‌لاین با دیتاست مصنوعی/Bootstrap برای اطمینان از سالم بودن کد.
- **Paper Mode:** دانلود دیتاست واقعی Tufts Dental Database، آماده‌سازی، اعتبارسنجی، آموزش U-Net، محاسبه‌ی معیارها و تولید Figureهای 1 تا 11 مقاله.

> این مخزن هیچ دیتاست دیگری را به‌صورت پنهانی جایگزین TDD نمی‌کند و نتیجه‌ی آن را به نام مقاله گزارش نمی‌دهد.

---

## 1) کلون کردن مخزن و نصب محیط

```bash
git clone https://github.com/hadifarajvand/Teeth-UNet-Paper.git
cd Teeth-UNet-Paper

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 2) دانلود دیتاست‌ها مستقیماً داخل همین Repository

فرمان اصلی دانلود و آماده‌سازی دیتاست‌ها:

```bash
./download_datasets.sh --dataset all
```

یا معادل پایتون:

```bash
python scripts/download_datasets.py --dataset all
```

تمام داده‌ها داخل پوشه‌ی `data/` همین repository قرار می‌گیرند:

```text
data/
├── bootstrap_synthetic/          # دیتاست Smoke
├── tdd_download/                 # فایل‌های خام/دانلودشده‌ی TDD
├── tdd/                          # دیتاست نهایی آماده برای Paper Mode
│   ├── images/
│   └── masks/
└── open_reference_download/      # دیتاست مرجع اختیاری
```

### دانلود فقط دیتاست اصلی مقاله، TDD

```bash
./download_datasets.sh --dataset tdd
```

این فرمان به‌صورت خودکار مراحل زیر را انجام می‌دهد:

```text
دانلود TDD
→ استخراج فایل‌ها
→ Pair کردن تصویر و Mask
→ نرمال‌سازی ساختار فایل‌ها
→ انتقال/آماده‌سازی داخل data/tdd/
→ اعتبارسنجی دیتاست
→ بررسی حداقل 900 جفت معتبر تصویر/Mask
```

بعد از موفقیت، دیتاستی که Paper Mode استفاده می‌کند دقیقاً اینجاست:

```text
data/tdd/images/
data/tdd/masks/
```

### ساخت/دانلود فقط دیتاست Smoke

```bash
./download_datasets.sh --dataset smoke
```

### دانلود دیتاست مرجع اختیاری

```bash
./download_datasets.sh --dataset open-reference
```

### دانلود مجدد از ابتدا

```bash
./download_datasets.sh --dataset tdd --force
```

### استفاده از آرشیو رسمی/مجاز TDD که قبلاً دانلود شده است

```bash
./download_datasets.sh \
  --dataset tdd \
  --archive /absolute/path/to/tufts-dental-database.zip
```

---

## 3) مسیرهای دانلود TDD که اسکریپت امتحان می‌کند

سیستم دانلود به‌صورت خودکار چند مسیر معتبر را امتحان می‌کند و اگر دیتاست واقعی در دسترس نباشد **Fail می‌شود**؛ دیتاست دیگری را جایگزین نمی‌کند.

ترتیب اصلی:

1. mirror کامل TDD روی Kaggle: `iftakharh/tufts-dental-datasetcustomized`
2. KaggleHub / Kaggle CLI / Direct Kaggle API
3. آرشیو رسمی Radiographهای Tufts در fallback ترکیبی
4. mirror فعال Radiographها: `manarmaged/tufts-radiographs`
5. Tooth Maskهای واقعی TDD از منبع عمومی مبتنی بر Tufts
6. تطبیق سخت‌گیرانه با **Original Numeric Image ID**
7. حداقل **900 جفت معتبر** برای اجازه‌ی شروع Paper Mode

اگر Kaggle نیاز به احراز هویت داشت، credential استاندارد Kaggle را در سیستم تنظیم کنید؛ سپس همان فرمان دانلود را دوباره اجرا کنید.

---

## 4) اجرای Smoke Simulation

```bash
./run_smoke.sh
```

یا:

```bash
python scripts/run_pipeline.py smoke
```

پایپ‌لاین:

```text
Bootstrap Dataset
→ آموزش U-Net
→ Dice / IoU
→ ذخیره Checkpoint
→ Prediction
→ Morphology
→ Connected Components
→ Contours / Measurements
→ تولید Figures 1–11
```

نتیجه‌ی Smoke که قبلاً با همین کد اجرا و اعتبارسنجی شده است:

- Dice: `0.9171192049980164`
- IoU: `0.846945196390152`
- Loss: `0.43136271834373474`

**این اعداد فقط سالم بودن پایپ‌لاین را ثابت می‌کنند و نتیجه‌ی Paper Mode روی TDD محسوب نمی‌شوند.**

---

## 5) اجرای کامل شبیه‌سازی مقاله

ساده‌ترین روش:

```bash
./run_paper.sh
```

یا:

```bash
python scripts/run_pipeline.py paper --download
```

Runner اکنون کل فرایند را خودش انجام می‌دهد:

```text
دانلود TDD داخل repository/data/
→ آماده‌سازی data/tdd/images و data/tdd/masks
→ Dataset Validation
→ TDD Provenance Validation با حداقل 900 Pair
→ ذخیره‌ی Train/Validation/Test Manifest
→ آموزش U-Net با ورودی 512×512
→ محاسبه Loss / Dice / IoU
→ ذخیره Best Checkpoint
→ تولید Figureهای 1 تا 11
→ مقایسه با مقادیر گزارش‌شده‌ی مقاله
→ Final Acceptance Gate
```

---

## 6) اجرای Smoke و Paper با هم

```bash
./run_all.sh
```

یا:

```bash
python scripts/run_pipeline.py both --download
```

---

## 7) تنظیمات اصلی Paper Mode

بر اساس pseudocode منتشرشده در مقاله:

- مدل: `U-Net`
- Loss: `Binary Cross Entropy`
- Optimizer: `Adam`
- Learning Rate: `0.001`
- Epochs: `50`
- Input در Paper Mode: `512×512`

مقادیر گزارش‌شده در مقاله:

- Dice ≈ `0.88`، در اسکرین‌شات ارزیابی حدود `0.8837`
- IoU ≈ `0.79`، در اسکرین‌شات ارزیابی حدود `0.7986`

مقاله تمام جزئیات لازم برای بازتولید بیت‌به‌بیت را منتشر نکرده است؛ از جمله Exact Split IDs، Seed اصلی، Checkpoint نویسندگان، تمام Augmentationها و همه‌ی پارامترهای Pre/Post-processing. بنابراین این مخزن خروجی را صادقانه به‌عنوان بازپیاده‌سازی paper-faithful گزارش می‌کند و عدد یا Figure جعلی تولید نمی‌کند.

---

## 8) خروجی‌ها

### خروجی Smoke

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

### خروجی Paper Mode بعد از اجرای موفق روی TDD واقعی

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

---

## 9) شرط نهایی قابل‌تحویل بودن Paper Mode

`outputs/paper/` فقط زمانی User-Deliverable محسوب می‌شود که همه‌ی موارد زیر پاس شوند:

1. حداقل 900 جفت واقعی و معتبر TDD Image/Mask
2. ذخیره‌ی Train/Validation/Test Manifest
3. پایان آموزش و وجود Best Checkpoint
4. معتبر بودن Loss، Dice و IoU
5. وجود هر 11 Figure موردنیاز
6. تولید `PAPER_COMPARISON.md`
7. پاس شدن Final Acceptance Check

فرمان بررسی:

```bash
python scripts/acceptance_check.py \
  --output-dir outputs/paper \
  --require-paper-data
```

---

## 10) فرمان‌های اصلی

```bash
# نصب وابستگی‌ها
pip install -r requirements.txt

# دانلود همه دیتاست‌ها داخل data/ همین repository
./download_datasets.sh --dataset all

# فقط دیتاست TDD
./download_datasets.sh --dataset tdd

# اجرای Smoke
make smoke

# اجرای کامل Paper Mode
make paper

# اجرای همه مراحل
make all
```

---

## 11) فایل‌های مهم پروژه

- `README.md` — راهنمای اصلی فارسی
- `README.en.md` — نسخه‌ی انگلیسی
- `download_datasets.sh` — دانلود یک‌مرحله‌ای دیتاست‌ها داخل repo
- `scripts/download_datasets.py` — دانلود + آماده‌سازی + validation دیتاست‌ها
- `scripts/download_all_data.py` — acquisition layer و fallbackها
- `scripts/download_tdd_hybrid.py` — fallback ترکیبی TDD
- `scripts/run_pipeline.py` — اجرای Smoke/Paper/Both
- `docs/RUNBOOK.md` — Runbook عملیاتی
- `docs/DATASETS.md` — provenance دیتاست‌ها
- `docs/TDD_ACQUISITION.md` — مسیرهای acquisition دیتاست TDD
- `docs/PAPER_OUTPUT_SPEC.md` — قرارداد تطابق Figure/Metric
- `docs/REPRODUCIBILITY_REPORT.md` — تفاوت تنظیمات گزارش‌شده و inferred
- `USER_DELIVERABLE_STATUS.md` — وضعیت دقیق deliverable

---

## صداقت علمی

اجرای مدل روی دیتاست مصنوعی یا یک دیتاست پانورامیک دیگر، بازتولید مقاله نیست. این مخزن عمداً در صورت نبود دیتاست واقعی TDD متوقف می‌شود و خروجی ساختگی یا دیتاست جایگزین را به نام نتیجه‌ی مقاله منتشر نمی‌کند.

برای نسخه‌ی انگلیسی این راهنما: **[README.en.md](README.en.md)**
