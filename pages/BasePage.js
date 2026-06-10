const { expect } = require('@playwright/test');
const { env } = require('../helpers/env');

class BasePage {
  constructor(page) {
    this.page = page;
  }

  async goto(path = '/') {
    await this.page.goto(new URL(path, env.baseUrl).toString(), { waitUntil: 'domcontentloaded' });
  }

  async expectUrlContains(fragment) {
    await expect(this.page).toHaveURL(new RegExp(fragment));
  }

  async expectVisibleText(pattern) {
    await expect(this.page.getByText(pattern).first()).toBeVisible({ timeout: 10000 });
  }
}

module.exports = { BasePage };
