# ران‌بوک بازتولید مقاله

**زبان:** **فارسی** | [English](RUNBOOK.en.md)

این مخزن دو حالت اجرای مستقل دارد:

1. **Smoke Mode** — تست سریع end-to-end برای اطمینان از سالم بودن کل پایپ‌لاین.
2. **Paper Mode** — دانلود و استفاده از دیتاست واقعی Tufts Dental Database (TDD)، آموزش U-Net و تولید خروجی‌های مقاله.

هیچ دیتاست دیگری به‌صورت پنهانی جایگزین TDD نمی‌شود.

---

## 1) آماده‌سازی محیط

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

برای اجرای Paper Mode با ورودی `512×512` استفاده از GPU توصیه می‌شود.

---

## 2) دانلود دیتاست‌ها داخل همین Repository

فرمان اصلی:

```bash
python scripts/download_datasets.py --dataset all
```

یا با wrapper:

```bash
bash download_datasets.sh --dataset all
```

تمام داده‌ها داخل `data/` همین repository قرار می‌گیرند:

```text
data/
├── bootstrap_synthetic/          # Smoke dataset
├── tdd_download/                 # فایل‌های خام دانلودشده
├── tdd/                          # دیتاست نهایی Paper Mode
│   ├── images/
│   └── masks/
└── open_reference_download/      # دیتاست مرجع اختیاری
```

### فقط دیتاست اصلی TDD

```bash
python scripts/download_datasets.py --dataset tdd
```

این فرمان کل مراحل زیر را انجام می‌دهد:

```text
دانلود
→ استخراج
→ Pair کردن Image/Mask
→ نرمال‌سازی ساختار فایل‌ها
→ آماده‌سازی داخل data/tdd/
→ Dataset Validation
→ بررسی حداقل 900 جفت معتبر TDD
```

### استفاده از آرشیو رسمی/مجاز محلی

```bash
python scripts/download_datasets.py \
  --dataset tdd \
  --archive /absolute/path/to/tufts-dental-database.zip
```

### دانلود مجدد از صفر

```bash
python scripts/download_datasets.py --dataset tdd --force
```

### فقط دیتاست Smoke

```bash
python scripts/download_datasets.py --dataset smoke
```

### دیتاست مرجع اختیاری

```bash
python scripts/download_datasets.py --dataset open-reference
```

---

## 3) زنجیره‌ی Acquisition دیتاست TDD

اسکریپت به‌ترتیب مسیرهای معتبر را امتحان می‌کند:

1. mirror کامل TDD روی Kaggle: `iftakharh/tufts-dental-datasetcustomized`
2. KaggleHub / Kaggle CLI / Direct Kaggle API
3. آرشیو رسمی Radiographهای Tufts از طریق fallback ترکیبی
4. mirror فعال Radiographها: `manarmaged/tufts-radiographs`
5. Tooth Maskهای واقعی TDD از منبع عمومی مبتنی بر Tufts
6. Pair کردن سخت‌گیرانه بر اساس Original Numeric Image ID
7. حداقل **900 Pair معتبر** برای اجازه‌ی Paper Mode

اگر Kaggle نیاز به login/API token داشته باشد، credential استاندارد Kaggle را تنظیم کنید و همان فرمان دانلود را دوباره اجرا کنید.

---

## 4) اجرای Smoke Simulation

```bash
bash run_smoke.sh
```

یا:

```bash
python scripts/run_pipeline.py smoke
```

پایپ‌لاین:

```text
Bootstrap Dataset
→ Deterministic Split
→ U-Net Training
→ Dice / IoU
→ Checkpoint
→ Prediction
→ Morphology
→ Connected Components
→ Contours / Measurements
→ Figures 1–11
```

خروجی‌ها:

```text
outputs/smoke/
├── metrics.json
├── history.csv
├── train_manifest.csv
├── validation_manifest.csv
├── test_manifest.csv
├── checkpoints/best_model.pt
└── figures/figure_01...figure_11
```

نتیجه‌ی Smoke فقط اجرای صحیح نرم‌افزار را ثابت می‌کند و نتیجه‌ی Paper Mode محسوب نمی‌شود.

---

## 5) اجرای کامل Paper Simulation

```bash
bash run_paper.sh
```

یا:

```bash
python scripts/run_pipeline.py paper --download
```

Runner کل فرایند را خودش اجرا می‌کند:

```text
دانلود TDD داخل repository/data/
→ آماده‌سازی data/tdd/images و data/tdd/masks
→ Dataset Validation
→ TDD Provenance Validation با حداقل 900 Pair
→ ذخیره‌ی Train/Validation/Test Manifest
→ U-Net 512×512
→ Binary Cross Entropy
→ Adam, lr=0.001
→ تا 50 Epoch
→ Best Checkpoint
→ Dice / IoU / Loss
→ Post-processing
→ Figures 1–11
→ PAPER_COMPARISON.md
→ Final Acceptance Gate
```

اگر TDD از قبل آماده شده باشد:

```bash
python scripts/run_pipeline.py paper --skip-prepare
```

---

## 6) اجرای Smoke و Paper با هم

```bash
bash run_all.sh
```

یا:

```bash
python scripts/run_pipeline.py both --download
```

Smoke ابتدا اجرا می‌شود. Paper Mode فقط بعد از آماده‌شدن و اعتبارسنجی TDD ادامه پیدا می‌کند.

---

## 7) تنظیمات اصلی مقاله

بر اساس pseudocode منتشرشده:

- `U-Net`
- `Binary Cross Entropy`
- `Adam`
- Learning Rate = `0.001`
- Epochs = `50`
- Paper input = `512×512`

مقادیر گزارش‌شده‌ی مقاله:

```text
Dice ≈ 0.88
IoU  ≈ 0.79
```

مخزن به‌صورت مصنوعی مدل را مجبور نمی‌کند که دقیقاً به این اعداد برسد.

مقاله موارد زیر را کامل منتشر نکرده است:

- Exact Split IDs
- Random Seed اصلی
- Original Checkpoint
- تمام Augmentation Parameters
- تمام Preprocessing/Post-processing Parameters
- Raw Training History

بنابراین مقایسه باید صادقانه به‌شکل زیر انجام شود:

```text
Paper Reported
vs
Our TDD Execution
vs
Absolute Difference
vs
Relative Difference
```

---

## 8) نقشه‌ی Figureها

| Figure | خروجی |
|---|---|
| 1 | معماری U-Net |
| 2 | Workflow |
| 3 | Radiograph + Ground Truth Mask |
| 4 | IoU Diagram |
| 5 | Train/Validation Dice Curve |
| 6 | Train/Validation IoU Curve |
| 7 | Test Panoramic Radiograph |
| 8 | Predicted Mask + Contours + Connected Components |
| 9 | Input / GT / Prediction / Overlay |
| 10 | Bounding Boxes + Pixel Measurements |
| 11 | Contour Overlay |

Figureهای 3 و 5 تا 11 در Paper Mode مستقیماً به دیتاست و اجرای واقعی وابسته‌اند.

---

## 9) خروجی Paper Mode

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

## 10) Final Acceptance Gate

یک اجرای Paper فقط زمانی User-Deliverable است که همه‌ی شرایط زیر پاس شوند:

- حداقل 900 جفت واقعی TDD Image/Mask
- Dataset Validation موفق
- Train/Validation/Test Manifest موجود
- Training کامل و Best Checkpoint موجود
- Loss/Dice/IoU معتبر
- هر 11 Figure موجود
- `PAPER_COMPARISON.md` موجود
- Final Acceptance Check موفق

فرمان:

```bash
python scripts/acceptance_check.py \
  --output-dir outputs/paper \
  --require-paper-data
```

---

## 11) بسته‌بندی Deliverable

```bash
python scripts/package_deliverable.py
```

فایل‌های بزرگ دیتاست پزشکی داخل `data/` همین clone دانلود می‌شوند ولی به‌صورت پیش‌فرض توسط `.gitignore` وارد Git history نمی‌شوند تا تصاویر پزشکی حجیم یا محدودشده ناخواسته منتشر نشوند.

برای نسخه‌ی انگلیسی Runbook: **[RUNBOOK.en.md](RUNBOOK.en.md)**
