# وضعیت User Deliverable

## موارد تکمیل‌شده

- کد کامل بازپیاده‌سازی U-Net.
- Configهای مستقل Smoke و Paper.
- Runnerهای end-to-end برای Smoke / Paper / Both.
- `README.md` به‌عنوان راهنمای اصلی فارسی.
- `README.en.md` به‌عنوان نسخه‌ی انگلیسی ثانویه.
- `docs/RUNBOOK.md` به‌عنوان Runbook اصلی فارسی.
- `docs/RUNBOOK.en.md` به‌عنوان Runbook انگلیسی.
- اسکریپت اصلی `scripts/download_datasets.py` برای دانلود و آماده‌سازی دیتاست‌ها مستقیماً داخل `data/` همین repository.
- wrapper ریشه‌ی مخزن: `download_datasets.sh`.
- زنجیره‌ی خودکار acquisition دیتاست TDD با official/mirror fallbackها.
- آماده‌سازی نهایی دیتاست Paper Mode در:
  - `data/tdd/images/`
  - `data/tdd/masks/`
- Strict TDD provenance validation با حداقل 900 Pair.
- Paper-target comparison و Final Acceptance tooling.
- Smoke metrics/history/manifests اجراشده.
- بسته‌ی ZIP شامل checkpoint، هر 11 Figure Smoke، PDF مقاله، code، notebook و documentation.

## فرمان اصلی دانلود دیتاست‌ها

```bash
python scripts/download_datasets.py --dataset all
```

یا:

```bash
bash download_datasets.sh --dataset all
```

برای فقط دیتاست مقاله:

```bash
python scripts/download_datasets.py --dataset tdd
```

این مسیر دانلود → استخراج → Pairing → آماده‌سازی در `data/tdd/` → validation → >=900-pair provenance check را انجام می‌دهد.

## Smoke Verification اجراشده

- Dice: `0.9171192049980164`
- IoU: `0.846945196390152`
- Loss: `0.43136271834373474`
- Figures: `11/11`

این اعداد فقط صحت اجرای پایپ‌لاین را نشان می‌دهند و به‌عنوان نتیجه‌ی TDD مقاله گزارش نمی‌شوند.

## وضعیت Exact Paper Run

محیط build مورد استفاده برای آماده‌سازی deliverable نتوانست فایل‌های 1000 Radiograph دیتاست Tufts را از hostهای upstream Tufts/Kaggle دریافت کند. پروژه‌های عمومی GitHub، Tooth Maskها و Split Metadata واقعی TDD را نشان می‌دهند ولی تصاویر پزشکی بیمار را در Git history قرار نداده‌اند.

بنابراین repository نتیجه‌ی جعلی به نام «Exact Paper Run» تولید نمی‌کند و مسیرهای معتبر زیر را به‌صورت خودکار امتحان می‌کند:

1. cited full-TDD Kaggle mirror
2. official Tufts `Radiographs.zip`
3. active Tufts radiograph Kaggle fallback
4. verified real TDD tooth masks
5. strict original numeric-ID pairing
6. >=900-pair provenance gate

Paper Mode فقط زمانی Complete محسوب می‌شود که Real TDD provenance، training/checkpoint، finite metrics، هر 11 Figure، paper comparison و acceptance check همگی موفق باشند.
