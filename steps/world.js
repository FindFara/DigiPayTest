const { setWorldConstructor, Before, After, Status } = require('@cucumber/cucumber');
const { chromium, firefox, webkit } = require('@playwright/test');
const { env } = require('../helpers/env');

const browsers = { chromium, firefox, webkit };

class CustomWorld {
  constructor({ parameters }) {
    this.parameters = parameters || {};
    this.env = env;
  }
}

setWorldConstructor(CustomWorld);

Before(async function () {
  const browserName = this.parameters.browserName || process.env.BROWSER || 'chromium';
  this.browser = await browsers[browserName].launch({ headless: env.headless });
  this.context = await this.browser.newContext({
    locale: 'fa-IR',
    timezoneId: 'Asia/Tehran',
    viewport: { width: 1366, height: 768 },
    recordVideo: process.env.CI ? { dir: 'test-results/videos' } : undefined
  });
  this.page = await this.context.newPage();
});

After(async function (scenario) {
  if (scenario.result?.status === Status.FAILED && this.page) {
    const image = await this.page.screenshot({ fullPage: true });
    await this.attach(image, 'image/png');
  }
  await this.context?.close();
  await this.browser?.close();
});
