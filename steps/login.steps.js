const { Given, When, Then } = require('@cucumber/cucumber');
const { LoginPage } = require('../pages/LoginPage');

Given('کاربر صفحه ورود دیجی‌پی را باز کرده است', async function () {
  this.loginPage = new LoginPage(this.page);
  await this.loginPage.open();
});

When('شماره موبایل معتبر خود را وارد می‌کند', async function () {
  await this.loginPage.submitMobile(this.env.testMobile);
});

When('شماره موبایل نامعتبر وارد می‌کند', async function () {
  await this.loginPage.submitMobile(this.env.invalidMobile);
});

Then('باید وارد مرحله دریافت کد تایید شود', async function () {
  await this.loginPage.expectOtpStep();
});

Then('باید پیام خطای اعتبارسنجی شماره موبایل را ببیند', async function () {
  await this.loginPage.expectMobileValidation();
});
