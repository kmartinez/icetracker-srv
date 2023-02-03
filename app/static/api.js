// Create the GET request URL to retrieve tracker data
function generateRetrieveURL(roverID, dataFormat, timestampStart, timestampEnd, requestedFields) {
    if (timestampStart) timestampStart += "T00:00:00";
    if (timestampEnd) timestampEnd += "T23:59:59";

    // Append the max/min for each date to make date ranges inclusive
    let requestURL = `api/retrieve?rover_id=${roverID}&data_format=${dataFormat}&timestamp_start=${timestampStart}&timestamp_end=${timestampEnd}`;

    requestedFields.forEach(field => {
        requestURL += "&requested_fields=" + field
    });

    return requestURL;
}

// Makes a request to the glacsweb API
function apiRequest(method, url, async, callbackSuccessFunc, callbackErrorFunc) {
    let request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState === 4) {
            let responseText = this.responseText;
            if (this.status === 200) {
                callbackSuccessFunc(responseText);
            } else if (this.status === 400) {
                callbackErrorFunc(responseText);
            }
        }
    }

    request.open(method, url, async);
    request.send();
}