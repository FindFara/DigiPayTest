const { expect } = require('@playwright/test');
const { BasePage } = require('./BasePage');
const { clickFirstVisible, fillFirstVisible } = require('../helpers/selectors');

class RechargePage extends BasePage {
  rechargeLinks() {
    return [
      this.page.getByRole('link', { name: /خرید شارژ|شارژ/ }),
      this.page.getByRole('button', { name: /خرید شارژ|شارژ/ }),
      this.page.locator('a[href*="charge"], a[href*="recharge"], [data-testid*="charge"], [data-cy*="charge"]')
    ];
  }

  directChargeOptions() {
    return [
      this.page.getByRole('button', { name: /شارژ مستقیم|مستقیم/ }),
      this.page.getByRole('link', { name: /شارژ مستقیم|مستقیم/ }),
      this.page.locator('label:has-text("مستقیم"), [data-testid*="direct"], [data-cy*="direct"]')
    ];
  }

  mobileInputs() {
    return [
      this.page.getByPlaceholder(/شماره موبایل|موبایل|تلفن/),
      this.page.getByLabel(/شماره موبایل|موبایل|تلفن/),
      this.page.locator('input[type="tel"], input[inputmode="numeric"], input[name*="mobile"], input[name*="phone"]')
    ];
  }

  amountOptions(amount) {
    return [
      this.page.getByRole('button', { name: new RegExp(amount) }),
      this.page.getByText(new RegExp(amount)).first(),
      this.page.locator(`[data-amount="${amount}"]`)
    ];
  }

  submitButtons() {
    return [
      this.page.getByRole('button', { name: /ادامه|خرید|پرداخت|تایید|تأیید/ }),
      this.page.locator('button[type="submit"]')
    ];
  }

  async open() {
    await this.goto('/');
    await clickFirstVisible(this.page, this.rechargeLinks(), { timeout: 10000 });
  }

  async chooseDirectRecharge() {
    await clickFirstVisible(this.page, this.directChargeOptions(), { timeout: 10000 });
  }

  async fillRechargeForm({ mobile, amount }) {
    await fillFirstVisible(this.page, this.mobileInputs(), mobile, { timeout: 10000 });
    if (amount) {
      try {
        await clickFirstVisible(this.page, this.amountOptions(amount), { timeout: 4000 });
      } catch (_) {
        const amountInput = this.page.locator('input[name*="amount"], input[placeholder*="مبلغ"]').first();
        await amountInput.fill(amount);
      }
    }
  }

  async continuePurchase() {
    await clickFirstVisible(this.page, this.submitButtons(), { timeout: 10000 });
  }

  async expectCheckoutOrLogin() {
    await expect(this.page.getByText(/پرداخت|تایید|تأیید|کد تایید|ورود|ثبت نام|خلاصه سفارش/).first()).toBeVisible({ timeout: 15000 });
  }

  async expectValidationMessage() {
    await expect(this.page.getByText(/شماره موبایل.*(صحیح|معتبر)|موبایل.*(صحیح|معتبر)|انتخاب.*اپراتور|مبلغ|نامعتبر|خطا/).first()).toBeVisible({ timeout: 10000 });
  }
}

module.exports = { RechargePage };
