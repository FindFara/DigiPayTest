const persianDigits = '۰۱۲۳۴۵۶۷۸۹';
const englishDigits = '0123456789';

function faNumber(value) {
  return String(value).replace(/[0-9]/g, digit => persianDigits[Number(digit)]);
}

function mobileVariants(value) {
  return [String(value), faNumber(value)];
}

async function firstVisible(page, locators, options = {}) {
  const timeout = options.timeout ?? 5000;
  for (const locator of locators) {
    try {
      await locator.first().waitFor({ state: 'visible', timeout });
      return locator.first();
    } catch (_) {
      // Try next locator. Tests keep resilient selector alternatives in one place.
    }
  }
  throw new Error(`None of the candidate locators became visible within ${timeout}ms`);
}

async function clickFirstVisible(page, locators, options = {}) {
  const locator = await firstVisible(page, locators, options);
  await locator.click(options.clickOptions || {});
  return locator;
}

async function fillFirstVisible(page, locators, value, options = {}) {
  const locator = await firstVisible(page, locators, options);
  await locator.fill(value);
  return locator;
}

module.exports = { clickFirstVisible, fillFirstVisible, firstVisible, faNumber, mobileVariants, englishDigits };
