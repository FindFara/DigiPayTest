# چارچوب تست خودکار QA برای DigiPay Top-up

این پروژه یک چارچوب Production-ready برای تست‌های **E2E** با **Python + Playwright + Pytest + pytest-bdd** است. ساختار پروژه بر اساس **Page Object Model (POM)** طراحی شده تا کدها تمیز، قابل توسعه، قابل نگهداری و مناسب ارائه در مصاحبه QA Automation باشند.

## سناریوهای نمونه

- Login flow: ارسال شماره موبایل معتبر و رسیدن به مرحله OTP.
- Login validation: نمایش خطا برای شماره موبایل نامعتبر.
- Top-up purchase flow: شروع خرید شارژ مستقیم با داده معتبر تا مرحله Checkout یا Login.
- Top-up validation: نمایش خطا برای شماره نامعتبر در خرید شارژ.

> تصمیم معماری: تست‌ها تا OTP، ورود، تایید سفارش یا پرداخت پیش می‌روند و پرداخت واقعی یا مصرف OTP واقعی انجام نمی‌دهند؛ این رویکرد برای تست E2E امن‌تر و پایدارتر است.

## ساختار کامل پروژه

```text
qa-topup-task/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── __init__.py
│   └── test_data.py
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── home_page.py
│   ├── login_page.py
│   └── topup_page.py
├── reports/
│   └── .gitkeep
├── screenshots/
│   └── .gitkeep
├── tests/
│   ├── __init__.py
│   ├── features/
│   │   ├── login.feature
│   │   └── topup.feature
│   ├── steps/
│   │   ├── __init__.py
│   │   ├── login_steps.py
│   │   └── topup_steps.py
│   ├── test_login.py
│   └── test_topup.py
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   └── screenshots.py
├── .env.example
├── .gitignore
├── conftest.py
├── Dockerfile
├── pytest.ini
├── README.md
└── requirements.txt
```

## نصب و راه‌اندازی

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
playwright install --with-deps chromium
cp .env.example .env
```

## متغیرهای محیطی

| متغیر | توضیح | نمونه |
| --- | --- | --- |
| `BASE_URL` | آدرس اپلیکیشن تحت تست | `https://app.mydigipay.com` |
| `PHONE_NUMBER` | شماره موبایل تستی معتبر | `09123456789` |
| `OTP` | مقدار OTP تستی در صورت وجود محیط تست/Mock | `12345` |
| `HEADLESS` | اجرای مرورگر بدون UI | `true` |
| `SLOW_MO` | کند کردن اجرای مرورگر برای دیباگ | `0` |
| `DEFAULT_TIMEOUT` | timeout پیش‌فرض Playwright بر حسب میلی‌ثانیه | `10000` |

## اجرای تست‌ها

اجرای همه تست‌ها:

```bash
pytest
```

اجرای فقط Smoke:

```bash
pytest -m smoke
```

اجرای فقط Login:

```bash
pytest -m login
```

اجرای فقط Top-up:

```bash
pytest -m topup
```

اجرای Headed برای دیباگ محلی:

```bash
HEADLESS=false pytest -m smoke
```

## گزارش‌ها

بعد از اجرای تست‌ها خروجی‌ها در مسیرهای زیر تولید می‌شوند:

- HTML report: `reports/report.html`
- Allure results: `reports/allure-results/`
- Log file: `reports/test-execution.log`
- Failure screenshots: `screenshots/`
- Failure videos: `reports/videos/`

برای مشاهده Allure report:

```bash
allure serve reports/allure-results
```

## اجرای Docker

```bash
docker build -t qa-topup-task .
docker run --rm --env-file .env qa-topup-task
```

## معماری و Best Practices

### Page Object Model

تمام رفتارهای مرتبط با صفحات در پوشه `pages/` قرار دارند. Step definitionها مستقیما با selectorها کار نمی‌کنند و فقط متدهای سطح بالای Page Object را صدا می‌زنند. این کار باعث می‌شود تغییرات UI فقط در یک لایه اعمال شود.

### BasePage

کلاس `BasePage` عملیات تکراری زیر را متمرکز کرده است:

- `click`
- `fill`
- `wait_for_element`
- `get_text`
- `take_screenshot`

این طراحی باعث رعایت DRY و جداسازی مسئولیت‌ها می‌شود.

### Data Layer

داده‌های تست در `data/test_data.py` نگهداری می‌شوند. مقدارهای حساس یا وابسته به محیط مثل `BASE_URL`، `PHONE_NUMBER` و `OTP` از `.env` خوانده می‌شوند و داخل تست‌ها hard-code نشده‌اند.

### Fixtures

در `conftest.py` سه fixture اصلی داریم:

- `browser`: اجرای Chromium به صورت session scoped.
- `context`: context ایزوله برای هر سناریو.
- `page`: صفحه مستقل برای هر تست.

ایزوله بودن context از نشت session، cookie و storage بین تست‌ها جلوگیری می‌کند.

### Screenshot خودکار روی Failure

Hook مربوط به `pytest_runtest_makereport` در زمان fail شدن تست، screenshot می‌گیرد و آن را هم در پوشه `screenshots/` ذخیره می‌کند و هم به گزارش HTML اضافه می‌کند.

### Logging

Logger مشترک در `utils/logger.py` تعریف شده و لاگ‌ها هم در ترمینال و هم در فایل `reports/test-execution.log` ثبت می‌شوند.

### Selector Strategy

برای کاهش brittle testها از Playwright best practice استفاده شده است:

- اولویت با `get_by_role()` است چون رفتار کاربر را بهتر مدل می‌کند.
- برای نقاط تست‌پذیر از `get_by_test_id()` استفاده شده است.
- از XPath شکننده استفاده نشده است.
- در صورت تفاوت UI، locatorها در Page Object متمرکز هستند و تغییر سناریوها لازم نیست.

### Retry و Wait Strategy

- از auto-waiting و `expect(...).to_be_visible()` استفاده شده است.
- `DEFAULT_TIMEOUT` قابل تنظیم است.
- در `pytest.ini` برای کاهش flaky بودن، retry محدود با `pytest-rerunfailures` فعال شده است.
- از sleep ثابت استفاده نشده است.

## CI/CD

فایل `.github/workflows/ci.yml` روی `push` و `pull_request` اجرا می‌شود. مراحل CI:

1. Checkout repository.
2. نصب Python.
3. نصب dependencyها از `requirements.txt`.
4. نصب Chromium با Playwright.
5. اجرای تست‌ها در حالت Headless.
6. آپلود `reports/` و `screenshots/` به عنوان artifact.

## نکاتی که در مصاحبه توضیح بدهم

- این پروژه POM دارد تا تست‌ها maintainable باشند.
- BDD با pytest-bdd باعث می‌شود سناریوها برای افراد فنی و غیر فنی قابل فهم باشند.
- fixtureها lifecycle مرورگر را کنترل می‌کنند و state بین تست‌ها نشت نمی‌کند.
- داده‌های تست و config از تست‌ها جدا شده‌اند.
- screenshot، HTML report، Allure report و log برای debug سریع خطاها اضافه شده‌اند.
- تست‌ها روی Chromium Headless اجرا می‌شوند و برای CI آماده‌اند.
- مسیرهای حساس مثل پرداخت واقعی و OTP واقعی در تست خودکار مصرف نشده‌اند.

## پیشنهادهای مقیاس‌پذیری و نگهداری

- اضافه کردن `data-testid` رسمی در اپلیکیشن برای همه المنت‌های کلیدی.
- استفاده از محیط Staging با test user و OTP قابل Mock.
- اضافه کردن Allure labels مثل severity، epic و story برای گزارش مدیریتی بهتر.
- جدا کردن test suiteها به smoke، regression، critical path و nightly.
- اضافه کردن Parallel execution با `pytest-xdist` بعد از پایدار شدن داده‌ها.
- اضافه کردن contract/API setup برای ساخت داده تست قبل از اجرای UI.
- افزودن pre-commit، Ruff و mypy برای کنترل کیفیت کد Python.
