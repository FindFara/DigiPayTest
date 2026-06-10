require('dotenv').config();

const env = {
  baseUrl: process.env.BASE_URL || 'https://app.mydigipay.com',
  headless: process.env.HEADLESS !== 'false',
  testMobile: process.env.TEST_MOBILE_NUMBER || '09123456789',
  invalidMobile: process.env.TEST_INVALID_MOBILE || '0912',
  rechargeTargetMobile: process.env.RECHARGE_TARGET_MOBILE || '09123456789',
  rechargeAmount: process.env.RECHARGE_AMOUNT || '20000'
};

module.exports = { env };
