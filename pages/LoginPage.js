const { expect } = require('@playwright/test');
const { BasePage } = require('./BasePage');
const { clickFirstVisible, fillFirstVisible } = require('../helpers/selectors');

class LoginPage extends BasePage {
  loginTriggers() {
    return [
      this.page.getByRole('link', { name: /ورود|ثبت نام|حساب کاربری/ }),
      this.page.getByRole('button', { name: /ورود|ثبت نام|حساب کاربری/ }),
      this.page.locator('a[href*="login"], a[href*="signin"], button:has-text("ورود")')
    ];
  }

  mobileInputs() {
    return [
      this.page.getByPlaceholder(/شماره موبایل|موبایل|تلفن/),
      this.page.getByLabel(/شماره موبایل|موبایل|تلفن/),
      this.page.locator('input[type="tel"], input[inputmode="numeric"], input[name*="mobile"], input[name*="phone"]')
    ];
  }

  submitButtons() {
    return [
      this.page.getByRole('button', { name: /ادامه|ورود|دریافت کد|ثبت نام/ }),
      this.page.locator('button[type="submit"]')
    ];
  }

  async open() {
    await this.goto('/');
    try {
      await clickFirstVisible(this.page, this.loginTriggers(), { timeout: 7000 });
    } catch (_) {
      await this.goto('/login');
    }
  }

  async submitMobile(mobile) {
    await fillFirstVisible(this.page, this.mobileInputs(), mobile, { timeout: 10000 });
    await clickFirstVisible(this.page, this.submitButtons(), { timeout: 10000 });
  }

  async expectOtpStep() {
    await expect(this.page.getByText(/کد تایید|کد تأیید|رمز یکبار مصرف|OTP|پیامک/).first()).toBeVisible({ timeout: 15000 });
  }

  async expectMobileValidation() {
    await expect(this.page.getByText(/شماره موبایل.*(صحیح|معتبر)|موبایل.*(صحیح|معتبر)|خطا|نامعتبر/).first()).toBeVisible({ timeout: 10000 });
  }
}

module.exports = { LoginPage };
