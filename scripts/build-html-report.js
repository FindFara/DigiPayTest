const fs = require('fs');
const reportPath = 'reports/cucumber-report.html';

if (!fs.existsSync(reportPath)) {
  console.error(`Report not found: ${reportPath}. Run npm test first.`);
  process.exit(1);
}

console.log(`Cucumber HTML report is ready at ${reportPath}`);
