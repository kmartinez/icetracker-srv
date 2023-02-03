// Listen for rover id changes and update date ranges
$(`#roverIdSelect`).change(function (_) {
    const form = document.getElementById("exportDataForm");
    const formData = new FormData(form);

    // Extract the rover_id option
    const roverID = formData.get("roverId");

    // Update the hard limits on the timestamps
    // Fetch the max and min times from the API
    apiRequest("GET", `api/query/timestamp_min?rover_id=${roverID}`, false, (responseText) => {
        let timestampJSON = JSON.parse(responseText);
        let timestamp = timestampJSON.timestamp;
        let startDateInput = document.getElementById(`startDateInput`);
        let endDateInput = document.getElementById(`endDateInput`);

        startDateInput.min = timestamp.split("T")[0];
        endDateInput.min = timestamp.split("T")[0];
        startDateInput.value = timestamp.split("T")[0];
    }, () => {
    });

    apiRequest("GET", `api/query/timestamp_max?rover_id=${roverID}`, false, (responseText) => {
        let timestampJSON = JSON.parse(responseText);
        let timestamp = timestampJSON.timestamp;
        let startDateInput = document.getElementById(`startDateInput`);
        let endDateInput = document.getElementById(`endDateInput`);

        startDateInput.max = timestamp.split("T")[0];
        endDateInput.max = timestamp.split("T")[0];
        endDateInput.value = timestamp.split("T")[0];
    }, () => {
    });
});

// Update preview table on form change
$("#exportDataForm").change(() => updateTable())

$(`#exportDataButton`).click(function (_) {
    const form = document.getElementById("exportDataForm");
    const formData = new FormData(form);

    // Get relevant options from form
    const roverID = formData.get("roverId");
    const timestampStart = formData.get("startDate");
    const timestampEnd = formData.get("endDate");
    const dataFormat = formData.get("fileType");

    // Get requested fields from form
    let requestedFields = [];
    let checkboxes = document.querySelectorAll("input[type='checkbox'][id$='Check']");

    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            requestedFields.push(checkbox.name);
        }
    })

    // Send the API request to retrieve the data records
    apiRequest("GET", generateRetrieveURL(roverID, dataFormat, timestampStart, timestampEnd, requestedFields), true,
        (recordsText) => {
            createExportAlert("alert-success", `Data successfully exported as ${dataFormat}`);

            // Download the file via the browser
            const a = document.createElement("a");
            if (dataFormat === "csv") {
                a.href = URL.createObjectURL(new Blob([recordsText], {
                    type: "text/csv"
                }));
                a.setAttribute("download", `glacsweb_export_${new Date().toISOString()}.json`);
            } else {
                // Sanitize and beautify the JSON (e.g. removing \n characters)
                let cleanJSON = JSON.stringify(JSON.parse(recordsText), null, 2);
                a.href = URL.createObjectURL(new Blob([cleanJSON], {
                    type: "application/json"
                }));
                a.setAttribute("download", `glacsweb_export_${new Date().toISOString()}.json`);
            }

            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        },
        (responseError) => {
            createExportAlert("alert-danger", responseError);
        });
});

// Request the full list of rovers that are possible
apiRequest("GET", "api/query/rovers", true, (roversText) => {
    let roversJSON = JSON.parse(roversText);

    let roverSelectDropdown = document.getElementById(`roverIdSelect`);

    // Populate the rover dropdown menu with each rover
    roversJSON.forEach((rover) => {
        let option = document.createElement("option");
        option.text = `Rover ${rover.rover_id} - ${rover.glacier}`;
        option.value = rover.rover_id;

        roverSelectDropdown.appendChild(option);
    });
}, () => {
});

// Show a pop up box explaining if the data was a success or failure
function createExportAlert(alertType, message) {
    // Overwrite the existing alert if it exists
    let exportAlert = document.getElementById("exportAlert");
    if (exportAlert == null) {
        exportAlert = document.createElement("div");
    }

    // Create the alert box
    exportAlert.id = "exportAlert";
    exportAlert.classList = "alert show m-3 " + alertType;
    exportAlert.role = "alert";
    exportAlert.innerText = message;

    let exportDataDiv = document.getElementById("exportDataDiv");
    exportDataDiv.appendChild(exportAlert);
}

function updateTable() {
    const form = document.getElementById("exportDataForm");
    const formData = new FormData(form);

    // Get relevant options from form
    const roverID = formData.get("roverId");
    const timestampStart = formData.get("startDate");
    const timestampEnd = formData.get("endDate");

    // Get requested fields from form
    let requestedFields = [];
    let checkboxes = document.querySelectorAll("input[type='checkbox'][id$='Check']");

    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            requestedFields.push(checkbox.name);
        }
    });

    // Send the API request to retrieve the data records
    apiRequest("GET", generateRetrieveURL(roverID, "json", timestampStart, timestampEnd, requestedFields), true,
        (recordsText) => {
            let table = $('#statsTable');

            // If there are records in the response
            if (recordsText !== "[]") {
                // Destroy if already a DataTable
                if (table[0].classList.contains("dataTable")) {
                    table[0].innerHTML = "";
                    table.DataTable().destroy();
                }

                // Delete existing heading
                table[0].deleteTHead();

                // Create table headings
                let header = table[0].createTHead();
                let headerRow = header.insertRow(0);

                let retrievedHeadings = Object.keys(JSON.parse(recordsText)[0]);

                retrievedHeadings.forEach(heading => {
                    let headingCell = headerRow.insertCell();

                    // insertCell uses <td> by default, so we have to swap for <th>
                    headingCell.outerHTML = `<th>${heading}</th>`;
                });

                table.DataTable({
                    data: JSON.parse(recordsText),
                    columns: retrievedHeadings.map(key => ({data: key})) // Map heading names into form {data: "heading1", ...}
                })
            } else {
                // If already a DataTable, clear all records
                if (table[0].classList.contains("dataTable")) {
                    table.DataTable().clear();
                    table.DataTable().draw();
                }
            }
        },
        () => {
        });
}
