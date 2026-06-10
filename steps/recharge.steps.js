const { Given, When, Then } = require('@cucumber/cucumber');
const { RechargePage } = require('../pages/RechargePage');

Given('کاربر صفحه خرید شارژ دیجی‌پی را باز کرده است', async function () {
  this.rechargePage = new RechargePage(this.page);
  await this.rechargePage.open();
});

When('گزینه شارژ مستقیم را انتخاب می‌کند', async function () {
  await this.rechargePage.chooseDirectRecharge();
});

When('اطلاعات معتبر خرید شارژ را تکمیل می‌کند', async function () {
  await this.rechargePage.fillRechargeForm({
    mobile: this.env.rechargeTargetMobile,
    amount: this.env.rechargeAmount
  });
});

When('بدون شماره موبایل معتبر ادامه می‌دهد', async function () {
  await this.rechargePage.fillRechargeForm({ mobile: this.env.invalidMobile, amount: this.env.rechargeAmount });
});

When('روی ادامه خرید شارژ کلیک می‌کند', async function () {
  await this.rechargePage.continuePurchase();
});

Then('باید به مرحله تایید سفارش یا ورود هدایت شود', async function () {
  await this.rechargePage.expectCheckoutOrLogin();
});

Then('باید پیام خطای فرم خرید شارژ نمایش داده شود', async function () {
  await this.rechargePage.expectValidationMessage();
});
