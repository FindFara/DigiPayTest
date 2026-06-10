# پروژه تست E2E دیجی‌پی برای مصاحبه QA

این ریپو یک نمونه پروژه **End-to-End Testing** برای سناریوهای ورود و خرید شارژ در `https://app.mydigipay.com` است. تست‌ها با **Playwright** و رویکرد **BDD / Gherkin** نوشته شده‌اند تا هم برای تیم فنی خوانا باشند و هم در مصاحبه بتوانید درباره طراحی تست، معماری، گزارش‌گیری و CI/CD توضیح بدهید.

> نکته مصاحبه: اگر از شما پرسیدند چرا BDD انتخاب شده، بگویید سناریوها به زبان کسب‌وکار نوشته شده‌اند، بنابراین QA، دولوپر و Product Owner می‌توانند روی رفتار مورد انتظار سیستم توافق مشترک داشته باشند.

## پوشش سناریوها

### ورود

- ورود با شماره موبایل معتبر و رسیدن به مرحله کد تایید.
- جلوگیری از ورود با شماره موبایل نامعتبر و نمایش پیام اعتبارسنجی.

### خرید شارژ

- شروع خرید شارژ مستقیم با اطلاعات معتبر و رسیدن به مرحله تایید سفارش یا ورود.
- نمایش خطا هنگام ادامه خرید شارژ با شماره موبایل نامعتبر.

## ساختار پروژه

```text
/project-root
├── .github/workflows/ci.yml     # اجرای خودکار تست‌ها در CI
├── helpers/                     # داده‌های محیطی و ابزارهای مشترک
├── pages/                       # Page Object Model
├── reports/                     # خروجی گزارش‌های Cucumber
├── scripts/                     # اسکریپت‌های کمکی گزارش
├── steps/                       # Step Definition های BDD
├── tests/features/              # فایل‌های Feature با زبان فارسی
├── .env.example                 # نمونه متغیرهای محیطی
├── cucumber.js                  # تنظیمات Cucumber
├── playwright.config.js         # تنظیمات Playwright
├── Dockerfile                   # اجرای قابل تکرار در کانتینر
└── package.json                 # اسکریپت‌ها و وابستگی‌ها
```

## پیش‌نیازها

- Node.js نسخه 20 یا بالاتر
- npm
- دسترسی شبکه به دامنه `https://app.mydigipay.com`
- Chromium که با دستور نصب Playwright دریافت می‌شود

## راه‌اندازی سریع

```bash
npm install
npx playwright install --with-deps chromium
cp .env.example .env
npm run test:chromium
```

بعد از اجرا، گزارش HTML در مسیر زیر ساخته می‌شود:

```text
reports/cucumber-report.html
```

## متغیرهای محیطی

| متغیر | مقدار پیش‌فرض | توضیح |
| --- | --- | --- |
| `BASE_URL` | `https://app.mydigipay.com` | آدرس اپلیکیشن تحت تست |
| `HEADLESS` | `true` | اجرای مرورگر بدون UI؛ برای دیباگ می‌توانید `false` کنید |
| `TEST_MOBILE_NUMBER` | `09123456789` | شماره موبایل معتبر برای سناریوی ورود |
| `TEST_INVALID_MOBILE` | `0912` | شماره نامعتبر برای بررسی Validation |
| `RECHARGE_TARGET_MOBILE` | `09123456789` | شماره مقصد خرید شارژ |
| `RECHARGE_AMOUNT` | `20000` | مبلغ شارژ تستی |

نمونه اجرای Headed برای دیباگ:

```bash
HEADLESS=false npm run test:chromium
```

## دستورات مهم

```bash
npm test
```

اجرای همه Featureها با تنظیمات پیش‌فرض Cucumber.

```bash
npm run test:chromium
```

اجرای تست‌ها روی Chromium Headless. این دستور همان دستور اصلی برای CI و تحویل مصاحبه است.

```bash
npm run test:headed
```

اجرای تست‌ها با باز شدن مرورگر برای دیباگ محلی.

```bash
npm run test:report
```

بررسی وجود گزارش HTML بعد از اجرای تست‌ها.

## معماری و دلیل انتخاب‌ها

### Page Object Model

کد تعامل با صفحات در پوشه `pages/` قرار دارد. این کار باعث می‌شود Stepها ساده، خوانا و نزدیک به زبان کسب‌وکار باقی بمانند. اگر UI تغییر کند، معمولا فقط Page Objectها اصلاح می‌شوند و نیازی نیست همه سناریوها تغییر کنند.

### BDD با Gherkin فارسی

Featureها در مسیر `tests/features/` با زبان فارسی نوشته شده‌اند. این کار برای مصاحبه خوب است چون نشان می‌دهد می‌توانید تست‌ها را به شکل قابل فهم برای افراد غیرتکنیکال هم مستندسازی کنید.

### Helperها

در `helpers/env.js` متغیرهای محیطی متمرکز شده‌اند و در `helpers/selectors.js` توابع کمکی انتخاب المنت‌ها وجود دارد. هدف این است که تکرار کد کم شود و تغییرات selector در یک نقطه مدیریت شود.

### گزارش‌گیری

Cucumber خروجی‌های زیر را تولید می‌کند:

- `reports/cucumber-report.html`
- `reports/cucumber-report.json`

در صورت Fail شدن سناریو، Screenshot به گزارش Cucumber attach می‌شود. در CI نیز پوشه‌های `reports/` و `test-results/` به عنوان Artifact آپلود می‌شوند.

## استراتژی انتخاب Selectorها و کاهش Flaky Test

- اولویت با selectorهای کاربرمحور مثل `getByRole`، متن دکمه و Label است.
- اگر selector معنایی در دسترس نباشد، از fallbackهایی مثل `data-testid`، `data-cy`، `href` یا نوع input استفاده شده است.
- انتخاب selectorها در Page Objectها متمرکز شده تا نگهداری آسان‌تر باشد.
- از `waitFor({ state: 'visible' })` و assertionهای Playwright استفاده شده و از `sleep` ثابت استفاده نشده است.
- سناریوها به OTP واقعی یا پرداخت واقعی وابسته نیستند؛ فقط تا مرحله قابل تست و امن مثل صفحه کد تایید، تایید سفارش یا ورود پیش می‌روند.
- روی CI برای کاهش خطاهای لحظه‌ای، `retry` محدود فعال است.

## CI/CD

Workflow در `.github/workflows/ci.yml` روی `push` و `pull_request` اجرا می‌شود. مراحل CI:

1. Checkout کد.
2. نصب Node.js.
3. نصب dependencyها با `npm install`.
4. نصب Chromium و dependencyهای سیستم.
5. اجرای `npm run test:chromium`.
6. آپلود گزارش‌ها و خروجی‌های شکست تست.

## اجرای با Docker

برای اجرای قابل تکرار در محیطی شبیه CI:

```bash
docker build -t digipay-e2e .
docker run --rm --env-file .env digipay-e2e
```

## نکاتی که در مصاحبه توضیح بدهم

- **هدف پروژه:** تست مسیرهای اصلی کاربر در دیجی‌پی شامل ورود و خرید شارژ، بدون ورود به پرداخت واقعی یا عملیات حساس.
- **چرا Playwright:** پایداری خوب، اجرای Headless، Trace/Screenshot/Video، پشتیبانی مناسب از Chromium و قابلیت استفاده در CI.
- **چرا BDD:** سناریوها خوانا هستند و به زبان کسب‌وکار نوشته شده‌اند؛ این باعث می‌شود خروجی برای QA، Developer و Product قابل فهم باشد.
- **چرا POM:** نگهداری ساده‌تر، جداسازی منطق صفحه از منطق سناریو و کاهش تکرار کد.
- **چطور با Flaky Test مقابله کردم:** استفاده نکردن از timeout ثابت، صبر کردن روی حالت visible، selectorهای چندلایه و retry محدود در CI.
- **گزارش‌گیری:** Cucumber report، JSON report و Screenshot هنگام شکست برای تحلیل سریع مشکل.
- **CI/CD:** تست‌ها در Pull Request اجرا می‌شوند تا قبل از Merge مشکل‌های E2E مشخص شود.
- **محدودیت‌ها:** چون OTP و پرداخت واقعی نباید در تست خودکار مصرف شوند، تست‌ها تا مرحله امن مثل نمایش صفحه کد تایید یا تایید سفارش ادامه می‌دهند.
- **اگر زمان بیشتری داشتم:** برای محیط Staging داده تستی مستقل، selectorهای رسمی `data-testid`، Mock کردن OTP، Trace viewer و گزارش Allure اضافه می‌کردم.

## پیشنهاد برای بهبود آینده

- اضافه کردن `data-testid` پایدار در اپلیکیشن اصلی.
- تعریف test user اختصاصی در محیط staging.
- جداسازی کامل smoke، regression و critical path suite.
- اضافه کردن Allure report یا dashboard برای مشاهده روند Failها.
- اجرای موازی تست‌ها بعد از پایدار شدن داده‌ها و selectorها.
