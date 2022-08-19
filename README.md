# Return 2Dim Array

API helps format data from various sources into two-dimensional array with field types for schema generation.

## Demo Deplyment
---

A demo deployment can be foud on heroku.

* <https://return-2dim-array.herokuapp.com/docs>

Demo deployment has free tier limitations.

* https://devcenter.heroku.com/articles/limits

## Example Usage
---

### Google Sheets

Google sheets can consume the two-dimensional data directly to sheet.

* <https://docs.google.com/spreadsheets/d/1Vj4xr8E45BVQbE875F-KmeMGY1kKK-5Gakphc0Neey0/edit?usp=sharing>

w/Apps Script Function

```js
function Return2DimArray(api_route, url){
  var payload = {
    "url": url
  }
  var options = {
    'method' : 'post',
    'contentType': 'application/json',
    'payload' : JSON.stringify(payload)
  }
  response = UrlFetchApp.fetch(api_route, options)
  data = JSON.parse(response.getContentText())
  return data["data"]
}
```

A timed trigger has also ben setup for every 5 minutes to ensure data from function is refreshed. Any function that references `setup!"B1"` will be refreshed with this trigger (see lax_parking).
```js
function RefreshTrigger(){
  let ss = SpreadsheetApp.getActiveSpreadsheet()
  let ws = ss.getSheetByName("setup")
  let value = ws.getRange("B1").getValue()
  ws.getRange("B1").setValue(value + 1)
  ws.getRange("B2").setValue(new Date())
}
```

### Data Studio

Data Studio can then be used to connect to sheet and visualize data.

* <https://datastudio.google.com/reporting/f8e7591c-07a7-417c-bc78-2910fbc55bc9>

![Data Studio LAX Parking](images/data-studio-lax-parking.png)


## Docker
---

Build image:

`docker build -t twodim .`

Start container:

`docker run -d --name twodim -p 80:80 twodim`

## Google Cloud Platform CI/CD
---

A `cloudbuild.yaml` is provided for CI/CD with Google Cloud Run.

