var TIME_ZONE = 'America/Los_Angeles';

// Populate this array only in the private Apps Script project. Never commit
// real Drive folder IDs or GA4 property IDs to the shared or consuming repo.
var SITES = [
  {
    domain: 'example.com',
    gscProperty: 'sc-domain:example.com',
    folderId: 'DRIVE_FOLDER_ID',
    propertyId: 'GA4_PROPERTY_ID'
  }
];

var GSC_REPORTS = [
  {suffix: 'gsc_queries', dimensions: ['query']},
  {suffix: 'gsc_pages', dimensions: ['page']},
  {suffix: 'gsc_countries', dimensions: ['country']},
  {suffix: 'gsc_devices', dimensions: ['device']},
  {suffix: 'gsc_search_appearance', dimensions: ['searchAppearance']},
  {suffix: 'gsc_dates', dimensions: ['date']}
];

function setupAndRunBackfill() {
  installWeeklyTrigger();
  return runWeeklySeoExport();
}

function installWeeklyTrigger() {
  ScriptApp.getProjectTriggers().forEach(function(trigger) {
    if (trigger.getHandlerFunction() === 'runWeeklySeoExport') {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  ScriptApp.newTrigger('runWeeklySeoExport')
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .atHour(9)
    .inTimezone(TIME_ZONE)
    .create();
}

function runWeeklySeoExport() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) {
    throw new Error('Another SEO export is already running.');
  }

  try {
    var period = previousCompleteWeek_();
    var result = {
      period: period.start + '_to_' + period.end,
      startedAt: new Date().toISOString(),
      sites: []
    };

    SITES.forEach(function(site) {
      var siteResult = exportSite_(site, period);
      result.sites.push(siteResult);
      console.log(JSON.stringify(siteResult));
    });

    result.finishedAt = new Date().toISOString();
    console.log(JSON.stringify(result, null, 2));
    return result;
  } finally {
    lock.releaseLock();
  }
}

function exportSite_(site, period) {
  var result = {domain: site.domain, created: [], skipped: [], errors: []};
  var folder;

  try {
    validateSite_(site);
    folder = DriveApp.getFolderById(site.folderId);
  } catch (error) {
    result.errors.push('configuration: ' + error.message);
    return result;
  }

  exportGa4_(folder, site, period, result);

  GSC_REPORTS.forEach(function(report) {
    exportOne_(folder, filename_(period, report.suffix), result, function() {
      return gscCsv_(site.gscProperty, report.dimensions, period);
    });
  });

  return result;
}

function exportGa4_(folder, site, period, result) {
  var csvFilename = filename_(period, 'ga4_organic_landing_pages');
  var manifestFilename = ga4SourceFilename_(period);

  try {
    var csvFiles = folder.getFilesByName(csvFilename);
    var manifestFiles = folder.getFilesByName(manifestFilename);

    if (csvFiles.hasNext()) {
      if (!manifestFiles.hasNext()) {
        throw new Error('Existing GA4 export has no source manifest');
      }
      var manifest = JSON.parse(
        manifestFiles.next().getBlob().getDataAsString('UTF-8')
      );
      if (
        manifest.domain !== site.domain ||
        String(manifest.propertyId) !== String(site.propertyId) ||
        manifest.startDate !== period.start ||
        manifest.endDate !== period.end
      ) {
        throw new Error('Existing GA4 export source does not match configured property');
      }
      result.skipped.push(csvFilename);
      result.skipped.push(manifestFilename);
      return;
    }

    if (manifestFiles.hasNext()) {
      throw new Error('GA4 source manifest exists without CSV');
    }

    var csv = ga4OrganicLandingPagesCsv_(site.propertyId, period);
    folder.createFile(Utilities.newBlob(csv, 'text/csv', csvFilename));
    result.created.push(csvFilename);

    var source = {
      schemaVersion: 1,
      domain: site.domain,
      propertyId: String(site.propertyId),
      startDate: period.start,
      endDate: period.end,
      generatedAt: new Date().toISOString()
    };
    folder.createFile(
      Utilities.newBlob(
        JSON.stringify(source, null, 2),
        'application/json',
        manifestFilename
      )
    );
    result.created.push(manifestFilename);
  } catch (error) {
    result.errors.push(csvFilename + ': ' + error.message);
  }
}

function exportOne_(folder, filename, result, buildCsv) {
  try {
    if (folder.getFilesByName(filename).hasNext()) {
      result.skipped.push(filename);
      return;
    }
    var csv = buildCsv();
    folder.createFile(Utilities.newBlob(csv, 'text/csv', filename));
    result.created.push(filename);
  } catch (error) {
    result.errors.push(filename + ': ' + error.message);
  }
}

function ga4OrganicLandingPagesCsv_(propertyId, period) {
  var request = {
    dateRanges: [{startDate: period.start, endDate: period.end}],
    dimensions: [
      {name: 'landingPagePlusQueryString'},
      {name: 'sessionDefaultChannelGroup'}
    ],
    metrics: [
      {name: 'sessions'},
      {name: 'totalUsers'},
      {name: 'engagedSessions'},
      {name: 'engagementRate'}
    ],
    dimensionFilter: {
      filter: {
        fieldName: 'sessionDefaultChannelGroup',
        stringFilter: {matchType: 'EXACT', value: 'Organic Search'}
      }
    },
    orderBys: [{metric: {metricName: 'sessions'}, desc: true}],
    limit: '100000'
  };

  var report = withRetry_(function() {
    return AnalyticsData.Properties.runReport(request, 'properties/' + propertyId);
  });
  var headers = (report.dimensionHeaders || []).map(function(item) { return item.name; })
    .concat((report.metricHeaders || []).map(function(item) { return item.name; }));
  var rows = (report.rows || []).map(function(row) {
    return (row.dimensionValues || []).map(function(item) { return item.value; })
      .concat((row.metricValues || []).map(function(item) { return item.value; }));
  });
  return toCsv_([headers].concat(rows));
}

function gscCsv_(siteUrl, dimensions, period) {
  var endpoint = 'https://www.googleapis.com/webmasters/v3/sites/' +
    encodeURIComponent(siteUrl) + '/searchAnalytics/query';
  var allRows = [];
  var startRow = 0;
  var pageSize = 25000;

  while (true) {
    var payload = {
      startDate: period.start,
      endDate: period.end,
      dimensions: dimensions,
      rowLimit: pageSize,
      startRow: startRow,
      dataState: 'final'
    };
    var response = withRetry_(function() {
      return UrlFetchApp.fetch(endpoint, {
        method: 'post',
        contentType: 'application/json',
        payload: JSON.stringify(payload),
        headers: {Authorization: 'Bearer ' + ScriptApp.getOAuthToken()},
        muteHttpExceptions: true
      });
    }, function(value) {
      return value.getResponseCode();
    });

    var status = response.getResponseCode();
    if (status < 200 || status >= 300) {
      throw new Error('Search Console HTTP ' + status + ': ' +
        response.getContentText().slice(0, 500));
    }
    var body = JSON.parse(response.getContentText() || '{}');
    var rows = body.rows || [];
    allRows = allRows.concat(rows);
    if (rows.length < pageSize) break;
    startRow += rows.length;
  }

  var headers = dimensions.concat(['clicks', 'impressions', 'ctr', 'position']);
  var values = allRows.map(function(row) {
    return (row.keys || []).concat([row.clicks, row.impressions, row.ctr, row.position]);
  });
  return toCsv_([headers].concat(values));
}

function withRetry_(operation, statusCode) {
  var retryable = {429: true, 500: true, 502: true, 503: true, 504: true};
  var lastError;
  for (var attempt = 0; attempt < 5; attempt++) {
    try {
      var value = operation();
      var code = statusCode ? statusCode(value) : 200;
      if (!retryable[code]) return value;
      lastError = new Error('Transient HTTP ' + code);
    } catch (error) {
      lastError = error;
      var message = String(error && error.message || error);
      if (!/(429|500|502|503|504|rate|quota|temporar|backend|internal)/i.test(message)) {
        throw error;
      }
    }
    if (attempt < 4) Utilities.sleep(Math.pow(2, attempt) * 1000);
  }
  throw lastError;
}

function previousCompleteWeek_() {
  var now = new Date();
  var day = Number(Utilities.formatDate(now, TIME_ZONE, 'u'));
  var localNoon = new Date(Utilities.formatDate(now, TIME_ZONE, 'yyyy-MM-dd') + 'T12:00:00');
  var thisMonday = new Date(localNoon.getTime() - (day - 1) * 86400000);
  var start = new Date(thisMonday.getTime() - 7 * 86400000);
  var end = new Date(thisMonday.getTime() - 1 * 86400000);
  return {
    start: Utilities.formatDate(start, TIME_ZONE, 'yyyy-MM-dd'),
    end: Utilities.formatDate(end, TIME_ZONE, 'yyyy-MM-dd')
  };
}

function filename_(period, suffix) {
  return period.start + '_to_' + period.end + '_' + suffix + '.csv';
}

function ga4SourceFilename_(period) {
  return period.start + '_to_' + period.end + '_ga4_source.json';
}

function validateSite_(site) {
  ['domain', 'gscProperty', 'folderId', 'propertyId'].forEach(function(key) {
    if (!site[key] || /_ID$/.test(site[key])) throw new Error('Missing private ' + key);
  });
}

function auditExporterHealth() {
  var seen = {};
  var errors = [];

  SITES.forEach(function(site) {
    if (seen[site.domain]) errors.push('Duplicate site: ' + site.domain);
    seen[site.domain] = true;
    try {
      validateSite_(site);
    } catch (error) {
      errors.push(site.domain + ': ' + error.message);
    }
  });

  var triggers = ScriptApp.getProjectTriggers().filter(function(trigger) {
    return trigger.getHandlerFunction() === 'runWeeklySeoExport';
  });
  if (triggers.length !== 1) {
    errors.push('Expected exactly one runWeeklySeoExport trigger; found ' + triggers.length);
  }

  var health = {
    ok: errors.length === 0,
    configuredSites: SITES.length,
    weeklyTriggerCount: triggers.length,
    errors: errors
  };
  console.log(JSON.stringify(health));
  return health;
}

function toCsv_(rows) {
  return rows.map(function(row) {
    return row.map(csvCell_).join(',');
  }).join('\r\n') + '\r\n';
}

function csvCell_(value) {
  if (value === null || value === undefined) return '';
  var text = String(value);
  if (/[",\r\n]/.test(text)) return '"' + text.replace(/"/g, '""') + '"';
  return text;
}
