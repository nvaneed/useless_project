var ss = SpreadsheetApp.openById('18gDZzYJcLABBQl5lRQF1MDGuj_iaHUpy9v7Or6aqPeo'); 
var sheet = ss.getSheetByName('Sheet1');
var timezone = "Asia/Kolkata";

function doGet(e) {
  Logger.log(JSON.stringify(e));

  if (!e.parameter.mode) {
    return ContentService.createTextOutput("No mode received. Full request: " + JSON.stringify(e));
  }

  // Clean up the mode string (remove spaces, force lowercase)
  var mode = e.parameter.mode.trim().toLowerCase();

  if (mode === "esp32") {
    var Curr_Date = new Date();
    var Curr_Time = Utilities.formatDate(Curr_Date, timezone, 'HH:mm:ss');
    var name = stripQuotes(e.parameter.name);

    var nextRow = sheet.getLastRow() + 1;
    sheet.getRange("A" + nextRow).setValue(Curr_Date);
    sheet.getRange("B" + nextRow).setValue(Curr_Time);
    sheet.getRange("C" + nextRow).setValue(name);

    return ContentService.createTextOutput("ESP32 data stored at row " + nextRow);
  } 
  else if (mode === "verify") {
    var lastRow = sheet.getLastRow();
    sheet.getRange("D" + lastRow).setValue("Verified");
    return ContentService.createTextOutput("Row " + lastRow + " marked as Verified");
  } 
  else if (mode === "reject") {
    var lastRow = sheet.getLastRow();
    sheet.getRange("D" + lastRow).setValue("Rejected");
    return ContentService.createTextOutput("Row " + lastRow + " marked as Rejected");
  }

  return ContentService.createTextOutput("Invalid request. Mode received: '" + mode + "'");
}

function stripQuotes(value) {
  return value.toString().replace(/^["']|['"]$/g, "");
}

