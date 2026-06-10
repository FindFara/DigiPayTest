module.exports = {
  default: {
    paths: ['tests/features/**/*.feature'],
    require: ['steps/**/*.js'],
    format: [
      'progress',
      'html:reports/cucumber-report.html',
      'json:reports/cucumber-report.json'
    ],
    publishQuiet: true,
    parallel: 1,
    retry: process.env.CI ? 1 : 0,
    timeout: 60000
  }
};
