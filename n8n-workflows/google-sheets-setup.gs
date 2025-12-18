/**
 * PlanWell n8n Workflows - Google Sheets Auto Setup Script
 *
 * This Google Apps Script will automatically create and configure
 * the Google Sheets needed for your n8n workflows.
 *
 * HOW TO USE:
 * 1. Go to https://script.google.com/
 * 2. Click "New Project"
 * 3. Delete any default code
 * 4. Paste this entire script
 * 5. Click the disk icon to save (name it "PlanWell Setup")
 * 6. Click "Run" button and select "setupPlanWellSheets"
 * 7. Grant necessary permissions when prompted
 * 8. Check the "Logs" (View > Logs) for the Sheet IDs
 */

function setupPlanWellSheets() {
  // Create the Contact Form Submissions sheet
  const contactSheet = createContactFormSheet();

  // Create the Webinar Registration Submissions sheet
  const webinarSheet = createWebinarRegistrationSheet();

  // Log the Sheet IDs for easy copying
  Logger.log('====================================');
  Logger.log('SETUP COMPLETE! ✅');
  Logger.log('====================================');
  Logger.log('');
  Logger.log('📋 CONTACT FORM SHEET:');
  Logger.log('   Name: ' + contactSheet.getName());
  Logger.log('   ID: ' + contactSheet.getId());
  Logger.log('   URL: ' + contactSheet.getUrl());
  Logger.log('');
  Logger.log('🎓 WEBINAR REGISTRATION SHEET:');
  Logger.log('   Name: ' + webinarSheet.getName());
  Logger.log('   ID: ' + webinarSheet.getId());
  Logger.log('   URL: ' + webinarSheet.getUrl());
  Logger.log('');
  Logger.log('====================================');
  Logger.log('NEXT STEPS:');
  Logger.log('1. Copy the Sheet IDs above');
  Logger.log('2. Use them in your n8n workflow configuration');
  Logger.log('3. Follow the SETUP-GUIDE.md for importing workflows');
  Logger.log('====================================');

  // Also show a UI alert
  SpreadsheetApp.getUi().alert(
    'Setup Complete! ✅\n\n' +
    'Check the "View > Logs" menu to see your Sheet IDs.\n\n' +
    'Contact Form Sheet: ' + contactSheet.getId() + '\n' +
    'Webinar Sheet: ' + webinarSheet.getId()
  );
}

/**
 * Creates the Contact Form Submissions sheet
 */
function createContactFormSheet() {
  // Create new spreadsheet
  const ss = SpreadsheetApp.create('PlanWell Contact Form Submissions');
  const sheet = ss.getActiveSheet();

  // Set up headers
  const headers = [
    'First Name',
    'Last Name',
    'Email',
    'Phone',
    'Message',
    'Submitted At',
    'Source'
  ];

  // Write headers to first row
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format the header row
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#4285f4');
  headerRange.setFontColor('#ffffff');
  headerRange.setFontWeight('bold');
  headerRange.setHorizontalAlignment('center');

  // Set column widths
  sheet.setColumnWidth(1, 120); // First Name
  sheet.setColumnWidth(2, 120); // Last Name
  sheet.setColumnWidth(3, 200); // Email
  sheet.setColumnWidth(4, 120); // Phone
  sheet.setColumnWidth(5, 300); // Message
  sheet.setColumnWidth(6, 150); // Submitted At
  sheet.setColumnWidth(7, 150); // Source

  // Freeze header row
  sheet.setFrozenRows(1);

  // Add some example formatting for data rows
  sheet.setFrozenRows(1);

  // Add data validation for Email column (optional, but helpful)
  const emailRange = sheet.getRange('C2:C1000');
  const emailRule = SpreadsheetApp.newDataValidation()
    .requireTextIsEmail()
    .setAllowInvalid(true)
    .setHelpText('Please enter a valid email address')
    .build();
  emailRange.setDataValidation(emailRule);

  return ss;
}

/**
 * Creates the Webinar Registration Submissions sheet
 */
function createWebinarRegistrationSheet() {
  // Create new spreadsheet
  const ss = SpreadsheetApp.create('PlanWell Webinar Registrations');
  const sheet = ss.getActiveSheet();

  // Set up headers
  const headers = [
    'First Name',
    'Last Name',
    'Email',
    'Agency',
    'Retirement Timeline',
    'Submitted At',
    'Source'
  ];

  // Write headers to first row
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format the header row
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#0f9d58');
  headerRange.setFontColor('#ffffff');
  headerRange.setFontWeight('bold');
  headerRange.setHorizontalAlignment('center');

  // Set column widths
  sheet.setColumnWidth(1, 120); // First Name
  sheet.setColumnWidth(2, 120); // Last Name
  sheet.setColumnWidth(3, 200); // Email
  sheet.setColumnWidth(4, 200); // Agency
  sheet.setColumnWidth(5, 150); // Retirement Timeline
  sheet.setColumnWidth(6, 150); // Submitted At
  sheet.setColumnWidth(7, 150); // Source

  // Freeze header row
  sheet.setFrozenRows(1);

  // Add data validation for Email column
  const emailRange = sheet.getRange('C2:C1000');
  const emailRule = SpreadsheetApp.newDataValidation()
    .requireTextIsEmail()
    .setAllowInvalid(true)
    .setHelpText('Please enter a valid email address')
    .build();
  emailRange.setDataValidation(emailRule);

  // Add dropdown validation for Retirement Timeline
  const timelineRange = sheet.getRange('E2:E1000');
  const timelineRule = SpreadsheetApp.newDataValidation()
    .requireValueInList([
      '0-6 months',
      '6-12 months',
      '1-2 years',
      '2-5 years',
      '5+ years',
      'Not sure'
    ], true)
    .setAllowInvalid(true)
    .setHelpText('Select a retirement timeline')
    .build();
  timelineRange.setDataValidation(timelineRule);

  return ss;
}

/**
 * Optional: Create a summary dashboard sheet
 * Run this separately if you want a dashboard
 */
function createDashboard() {
  const ss = SpreadsheetApp.create('PlanWell Dashboard');
  const sheet = ss.getActiveSheet();
  sheet.setName('Dashboard');

  // Add title
  sheet.getRange('A1').setValue('PlanWell Submissions Dashboard');
  sheet.getRange('A1').setFontSize(18).setFontWeight('bold');

  // Add instructions
  sheet.getRange('A3').setValue('Instructions:');
  sheet.getRange('A4').setValue('1. Update the formula below with your actual Sheet IDs');
  sheet.getRange('A5').setValue('2. This dashboard will show real-time counts of submissions');

  // Placeholder formulas (user needs to update with actual sheet IDs)
  sheet.getRange('A7').setValue('Total Contact Form Submissions:');
  sheet.getRange('B7').setValue('=COUNTA(IMPORTRANGE("YOUR_CONTACT_SHEET_ID", "Sheet1!A:A"))-1');

  sheet.getRange('A8').setValue('Total Webinar Registrations:');
  sheet.getRange('B8').setValue('=COUNTA(IMPORTRANGE("YOUR_WEBINAR_SHEET_ID", "Sheet1!A:A"))-1');

  Logger.log('Dashboard created: ' + ss.getUrl());
  Logger.log('Remember to update the IMPORTRANGE formulas with your actual Sheet IDs');

  return ss;
}
