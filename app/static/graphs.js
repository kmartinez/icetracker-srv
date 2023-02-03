let graphs = [];
let graphConfigs = [];
let updateLock = false;

function addGraph(config = undefined) {
    let graphID;

    if (!config) {
        graphID = graphConfigs.length;

        // Hard cap on number of graphs (= 6)
        if (graphID > 5) {
            return;
        }

        const data = {
            datasets: [{
                label: "Glacsweb Dataset",
                showLine: true,
                yAxisID: "y",
            }]
        };

        config = {
            type: "scatter",
            data: data,
            startDate: undefined,
            endDate: undefined,
            activeGraphPreset: undefined,
            y2Enabled: false,
            options: {
                normalized: true,
                plugins: {
                    legend: {
                        labels: {
                            filter: function (_, _) {
                                // Hides dataset legends
                                return false;
                            }
                        }
                    },
                    zoom: {
                        pan: {
                            enabled: true,
                            mode: "xy",
                            scaleMode: "xy"
                        },
                        zoom: {
                            wheel: {
                                enabled: true,
                            },
                            pinch: {
                                enabled: true
                            },
                            mode: "xy",
                            scaleMode: "xy",
                        }
                    },
                },
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                        },
                    },
                    y: {
                        title: {
                            display: true,
                        },
                    }
                },
            },
            id: graphID
        };

        saveConfig(graphID, config);
    } else {
        graphID = config.id;
    }

    // Workaround: manually re-add filter to hide dataset legend
    // Either because deep copy doesn't go deep enough, or it thinks the filter is unused so discards it
    config.options.plugins.legend.labels = {
        filter: function (_, _) {
            // Hides dataset legends
            return false;
        }
    };

    // Keep the graph configuration in cookies and variable scope
    graphConfigs.push(config);

    let graph = new Chart(
        document.getElementById(`graph${graphID}`), config
    );

    graphs.push(graph)

    // Find the template accordion menu entry and clone it
    const template = document.getElementById(`accordionTemplate${graphID}`);
    const accordion = document.getElementById("graphSideMenu");
    const clone = template.content.cloneNode(true);

    // Add template contents to accordion menu
    accordion.appendChild(clone);

    updateConfigurationMenu(graphID, config);

    // Highlight corresponding graph when clicking on accordion menu item
    $(`#accordionButton${graphID}`).click(function (_) {
        selectGraph(graphID, false);
    });

    // Listen for form changes to update graph automatically
    $(`#graphForm${graphID}`).change(function (_) {
        if (!updateLock) {
            updateGraph(graphID);
        }
    });

    // Listen for rover id changes and update date ranges
    $(`#graphRoverIdSelect${graphID}`).change(function (_) {
        if (!updateLock) {
            updateDateInputs(graphID);
        }
    });

    $(`#y2AxisEnabled${graphID}`).click(function (e) {
        // Select all <div> input groups for Y2 and the Y2 styling label
        let y2AxisElements = document.querySelectorAll(`div[id^='y2Axis'][id$='InputGroup${graphID}'],label[id='y2AxisStylingLabel${graphID}']`);

        if (this.checked) {
            // Show elements if Y2 axis checkbox is checked (default: "flex")
            y2AxisElements.forEach(element => element.style.display = "flex");
        } else {
            // Hide if not checked
            y2AxisElements.forEach(element => element.style.display = "none");
        }
    });

    $(`#y2AxisLabel${graphID}`).click(function (e) {
        let id = parseInt(e["currentTarget"].id.replace("y2AxisLabel", ""));

        let y2AxisCheckbox = document.getElementById(`y2AxisEnabled${id}`);
        let form = document.getElementById(`graphForm${id}`)

        y2AxisCheckbox.checked = !y2AxisCheckbox.checked;

        // Click the checkbox
        let clickEvent = new Event("click");
        y2AxisCheckbox.dispatchEvent(clickEvent);

        let changeEvent = new Event("change");
        form.dispatchEvent(changeEvent);
    });

    // Request the full list of rovers that are possible
    apiRequest("GET", "api/query/rovers?hide_unused", true, (roversText) => {
        let roversJSON = JSON.parse(roversText);

        let roverSelectDropdown = document.getElementById(`graphRoverIdSelect${graphID}`);

        // Populate the rover dropdown menu with each rover
        roversJSON.forEach((rover) => {
            let option = document.createElement("option");
            option.text = `Rover ${rover.rover_id} - ${rover.glacier}`;
            option.value = rover.rover_id;

            roverSelectDropdown.appendChild(option);
        });
    }, () => {
    });
}

function updateConfigurationMenu(id) {
    updateLock = true;
    const form = document.forms[`graphForm${id}`];

    // Extract timestamp range options
    const timestampStart = getGraphConfig(id).options.startDate;
    const timestampEnd = getGraphConfig(id).options.endDate;

    // Extract X axis options
    let xAxisDataSource = getGraphConfig(id).options.xAxisDataSource;
    const xAxisScaleStart = getGraphConfig(id).options.scales["x"].min;
    const xAxisScaleEnd = getGraphConfig(id).options.scales["x"].max;
    const xAxisLabel = getGraphConfig(id).options.scales["x"].title.text;

    // Extract Y axis options
    let yAxisDataSource = getGraphConfig(id).options.yAxisDataSource;
    const yAxisScaleStart = getGraphConfig(id).options.scales["y"].min;
    const yAxisScaleEnd = getGraphConfig(id).options.scales["y"].max;
    const yAxisLabel = getGraphConfig(id).options.scales["y"].title.text;
    const yAxisLineColour = getGraphConfig(id).data.datasets[0].borderColor.slice(0, -2);

    // Extract Y axis style options
    let yAxisGraphType;
    const yAxisLineShown = getGraphConfig(id).data.datasets[0].showLine;

    const graphPreset = getGraphConfig(id).activeGraphPreset;

    if (yAxisLineShown) {
        yAxisGraphType = "Line";
    } else {
        yAxisGraphType = "Scatter";
    }

    // Update graph preset option
    form.elements["graphPreset"].value = graphPreset;

    // Update timestamp range options
    form.elements["startDate"].value = timestampStart;
    form.elements["endDate"].value = timestampEnd;

    // Update X axis options
    form.elements["xAxisDataSource"].value = xAxisDataSource;
    form.elements["xAxisScaleStart"].value = (xAxisScaleStart ? xAxisScaleStart : "Auto");
    form.elements["xAxisScaleEnd"].value = (xAxisScaleEnd ? xAxisScaleEnd : "Auto");
    form.elements["xAxisLabel"].value = xAxisLabel;

    // Update Y axis options
    form.elements["yAxisDataSource"].value = yAxisDataSource;
    form.elements["yAxisScaleStart"].value = (yAxisScaleStart ? yAxisScaleStart : "Auto");
    form.elements["yAxisScaleEnd"].value = (yAxisScaleEnd ? yAxisScaleEnd : "Auto");
    form.elements["yAxisLabel"].value = yAxisLabel;

    // Update Y axis style options
    form.elements["yAxisLineColour"].value = yAxisLineColour;
    form.elements["yAxisGraphType"].value = yAxisGraphType;

    // Check if Y2 is enabled
    let y2AxisEnabled = getGraphConfig(id).y2AxisEnabled;

    if (y2AxisEnabled) {
        // Extract Y2 axis options
        let y2AxisDataSource = getGraphConfig(id).options.y2AxisDataSource;
        const y2AxisScaleStart = getGraphConfig(id).options.scales["y2"].min;
        const y2AxisScaleEnd = getGraphConfig(id).options.scales["y2"].max;
        const y2AxisLabel = getGraphConfig(id).options.scales["y2"].title.text;
        const y2AxisLineColour = getGraphConfig(id).data.datasets[1].borderColor.slice(0, -2);
        const y2AxisLineShown = getGraphConfig(id).data.datasets[1].showLine;
        let y2AxisGraphType;

        if (y2AxisLineShown) {
            y2AxisGraphType = "Line";
        } else {
            y2AxisGraphType = "Scatter";
        }

        // Update Y2 axis options
        form.elements["y2AxisEnabled"].checked = true;

        // Select all <div> input groups for Y2 and the Y2 styling label
        let y2AxisElements = document.querySelectorAll(`div[id^='y2Axis'][id$='InputGroup${id}'],label[id='y2AxisStylingLabel${id}']`);

        // Show Y2 elements (default: "flex")
        y2AxisElements.forEach(element => element.style.display = "flex");

        form.elements["y2AxisDataSource"].value = y2AxisDataSource;
        form.elements["y2AxisScaleStart"].value = (y2AxisScaleStart ? y2AxisScaleStart : "Auto");
        form.elements["y2AxisScaleEnd"].value = (y2AxisScaleEnd ? y2AxisScaleEnd : "Auto");
        form.elements["y2AxisLabel"].value = y2AxisLabel;

        // Update Y axis style options
        form.elements["y2AxisLineColour"].value = y2AxisLineColour;
        form.elements["y2AxisGraphType"].value = y2AxisGraphType;
    } else {

    }

    updateLock = false;
}

function getGraphConfig(id) {
    // Graph config index may not be equal to ID, so get by ID instead
    return graphConfigs.find(config => {
        return config.id === id;
    })
}

function updateGraph(id) {
    // Destroy existing chart
    graphs[id].destroy();

    const form = document.querySelector(`#graphForm${id}`);
    const formData = new FormData(form);

    const graphPreset = formData.get("graphPreset");
    getGraphConfig(id).activeGraphPreset = graphPreset;

    let xAxisDataSource;
    let xAxisLabel;

    let yAxisDataSource;
    let yAxisLabel;

    let y2AxisEnabled = false;
    let y2AxisDataSource;
    let y2AxisLabel;

    switch (graphPreset) {
        case "Custom...":
            xAxisDataSource = formData.get("xAxisDataSource");
            yAxisDataSource = formData.get("yAxisDataSource");
            y2AxisDataSource = formData.get("y2AxisDataSource");
            y2AxisEnabled = form.elements["y2AxisEnabled"].checked;
            break;
        case "Latitude/Longitude":
            xAxisDataSource = "longitude";
            yAxisDataSource = "latitude";
            xAxisLabel = capitaliseLabel(xAxisDataSource);
            yAxisLabel = capitaliseLabel(yAxisDataSource);
            break;
        case "Displacement/Time":
            xAxisDataSource = "timestamp";
            yAxisDataSource = "displacement";
            xAxisLabel = capitaliseLabel(xAxisDataSource);
            yAxisLabel = capitaliseLabel(yAxisDataSource);
            break;
        case "Velocity/Time":
            xAxisDataSource = "timestamp";
            yAxisDataSource = "velocity";
            xAxisLabel = capitaliseLabel(xAxisDataSource);
            yAxisLabel = capitaliseLabel(yAxisDataSource);
            break;
        case "Velocity/Time/Temperature":
            xAxisDataSource = "timestamp";
            yAxisDataSource = "velocity";
            xAxisLabel = capitaliseLabel(xAxisDataSource);
            yAxisLabel = capitaliseLabel(yAxisDataSource);
            y2AxisEnabled = true;
            y2AxisDataSource = "temperature";
            y2AxisLabel = capitaliseLabel(y2AxisDataSource);
            break;
    }

    if (!y2AxisLabel && y2AxisEnabled) {
        y2AxisLabel = capitaliseLabel(y2AxisDataSource);
    }

    updateLock = true;

    let y2AxisCheckbox = form.elements["y2AxisEnabled"];

    // Click the Y2 axis checkbox if necessary
    if (y2AxisEnabled && !y2AxisCheckbox.checked) {
        // Check the checkbox
        y2AxisCheckbox.checked = true;

        // Click the checkbox (does *not* check the checkbox)
        let clickEvent = new Event("click")
        y2AxisCheckbox.dispatchEvent(clickEvent);
    } else if (!y2AxisEnabled && y2AxisCheckbox.checked) {
        y2AxisCheckbox.checked = false;

        let clickEvent = new Event("click")
        y2AxisCheckbox.dispatchEvent(clickEvent);
    }

    // Update configuration menu in case preset was used
    if (graphPreset !== "Custom...") {
        form.elements["xAxisDataSource"].value = xAxisDataSource;
        form.elements["yAxisDataSource"].value = yAxisDataSource;
        form.elements["y2AxisDataSource"].value = y2AxisDataSource;
        form.elements["xAxisLabel"].value = xAxisLabel;
        form.elements["yAxisLabel"].value = yAxisLabel;
        form.elements["y2AxisLabel"].value = y2AxisLabel;
    }

    updateLock = false;

    // Extract the rover_id option
    const roverID = formData.get("roverId");

    // Extract timestamp range options
    const timestampStart = formData.get("startDate");
    const timestampEnd = formData.get("endDate");

    // Extract X axis options
    const xAxisScaleStart = parseInt(formData.get("xAxisScaleStart").toString())
    const xAxisScaleEnd = parseInt(formData.get("xAxisScaleEnd").toString())

    if (!xAxisLabel) {
        xAxisLabel = formData.get("xAxisLabel");
    }

    // Extract Y axis options
    const yAxisScaleStart = parseInt(formData.get("yAxisScaleStart").toString());
    const yAxisScaleEnd = parseInt(formData.get("yAxisScaleEnd").toString());

    if (!yAxisLabel) {
        yAxisLabel = formData.get("yAxisLabel");
    }

    // Extract style options
    const yAxisLineColour = formData.get("yAxisLineColour");
    const yAxisGraphType = formData.get("yAxisGraphType").toLowerCase();

    // Extract Y axis options
    const y2AxisScaleStart = parseInt(formData.get("y2AxisScaleStart").toString());
    const y2AxisScaleEnd = parseInt(formData.get("y2AxisScaleEnd").toString());

    if (!yAxisLabel) {
        yAxisLabel = formData.get("yAxisLabel");
    }

    // Extract style options
    const y2AxisLineColour = formData.get("y2AxisLineColour");
    const y2AxisGraphType = formData.get("y2AxisGraphType").toLowerCase();

    // Ensure necessary UI fields are filled before sending a request
    if (timestampStart && timestampEnd && xAxisDataSource && yAxisDataSource) {
        // Generate the API URL including requested fields
        let requestedFields = [xAxisDataSource.toLowerCase(), yAxisDataSource.toLowerCase()]

        if (y2AxisDataSource) {
            requestedFields.push(y2AxisDataSource.toLowerCase())
        }

        let requestURL = generateRetrieveURL(roverID, "json", timestampStart, timestampEnd, requestedFields);

        // Send a request to the API to fetch the graph data
        apiRequest("GET", requestURL, true, (graphData) => {
            // Set Y2 axis options
            if (yAxisDataSource === "timestamp" && !yAxisLabel) {
                yAxisLabel = "Time";
            } else if (!yAxisLabel) {
                yAxisLabel = yAxisDataSource;
            }

            // Set the axes internal representation
            getGraphConfig(id).options.xAxisDataSource = xAxisDataSource;
            getGraphConfig(id).options.yAxisDataSource = yAxisDataSource;

            // Set timestamp options
            getGraphConfig(id).options.startDate = timestampStart;
            getGraphConfig(id).options.endDate = timestampEnd;

            let defaultXAxis = {
                title: {
                    display: true,
                    text: xAxisLabel,
                },
                min: (isNaN(xAxisScaleStart) ? undefined : xAxisScaleStart),
                max: (isNaN(xAxisScaleEnd) ? undefined : xAxisScaleEnd)
            }

            getGraphConfig(id).options.scales.x = defaultXAxis;

            let defaultYAxis = {
                title: {
                    display: true,
                    text: yAxisLabel,
                    color: yAxisLineColour,
                },
                yAxisID: "y",
                position: "left",
                min: (isNaN(yAxisScaleStart) ? undefined : yAxisScaleStart),
                max: (isNaN(yAxisScaleEnd) ? undefined : yAxisScaleEnd),
            }
            // Create the scale for the y-axis
            getGraphConfig(id).options.scales.y = defaultYAxis;

            if (yAxisDataSource === "timestamp") {
                getGraphConfig(id).options.scales.y = {
                    type: "time",
                    title: {
                        display: true,
                        text: yAxisLabel,
                        color: yAxisLineColour
                    },
                    time: {
                        minUnit: "second",
                        displayFormats: {
                            "day": "yyyy-MM-dd",
                            "hour": "yyyy-MM-dd HH:mm",
                            "minute": "yyyy-MM-dd HH:mm:ss",
                            "second": "yyyy-MM-dd HH:mm:ss"
                        },
                    },
                    ticks: {
                        callback: false,
                    },
                    position: "left",
                    min: (isNaN(yAxisScaleStart) ? undefined : yAxisScaleStart),
                    max: (isNaN(yAxisScaleEnd) ? undefined : yAxisScaleEnd),
                }
            } else {
                getGraphConfig(id).options.scales.y = defaultYAxis;
            }

            if (xAxisDataSource === "timestamp") {
                getGraphConfig(id).options.scales.x = {
                    type: "time",
                    title: {
                        display: true,
                        text: xAxisLabel,
                    },
                    time: {
                        minUnit: "second",
                        displayFormats: {
                            "day": "yyyy-MM-dd",
                            "hour": "yyyy-MM-dd HH:mm",
                            "minute": "yyyy-MM-dd HH:mm:ss",
                            "second": "yyyy-MM-dd HH:mm:ss"
                        },
                    },
                    ticks: {
                        callback: false,
                    },
                    position: "left",
                    min: (isNaN(xAxisScaleStart) ? undefined : xAxisScaleStart),
                    max: (isNaN(xAxisScaleEnd) ? undefined : xAxisScaleEnd),
                }
            } else {
                getGraphConfig(id).options.scales.x = defaultXAxis;
            }

            // Add the dataset to the graph
            getGraphConfig(id).data.datasets[0] = {
                label: "Glacsweb Dataset",
                showLine: (yAxisGraphType === "line"),
                yAxisID: "y",
                data: JSON.parse(graphData),
                parsing: {
                    xAxisKey: xAxisDataSource,
                    yAxisKey: yAxisDataSource
                },
                borderColor: yAxisLineColour + "BB",
                backgroundColor: yAxisLineColour + "DD",
            }

            if (y2AxisEnabled) {
                // Set Y2 axis options
                if (y2AxisDataSource === "timestamp" && !y2AxisLabel) {
                    y2AxisLabel = "Time";
                } else if (!y2AxisLabel) {
                    y2AxisLabel = capitaliseLabel(y2AxisDataSource);
                }

                let defaultY2Axis = {
                    title: {
                        display: true,
                        text: y2AxisLabel,
                        color: y2AxisLineColour,
                    },
                    position: "right",
                    min: (isNaN(y2AxisScaleStart) ? undefined : y2AxisScaleStart),
                    max: (isNaN(y2AxisScaleEnd) ? undefined : y2AxisScaleEnd),
                    grid: {
                        drawOnChartArea: false, // only want the grid lines for one axis to show up
                    },
                }

                // Set internal axis representation
                getGraphConfig(id).y2AxisEnabled = true;
                getGraphConfig(id).options.y2AxisDataSource = (y2AxisDataSource === "timestamp" ? "Time" : y2AxisDataSource);

                // Create the scale for the y2 axis
                getGraphConfig(id).options.scales.y2 = defaultY2Axis;

                if (y2AxisDataSource === "timestamp") {
                    getGraphConfig(id).options.scales.y2 = {
                        type: "time",
                        title: {
                            display: true,
                            text: y2AxisLabel,
                            color: y2AxisLineColour
                        },
                        time: {
                            minUnit: "second",
                            displayFormats: {
                                "day": "yyyy-MM-dd",
                                "hour": "yyyy-MM-dd HH:mm",
                                "minute": "yyyy-MM-dd HH:mm:ss",
                                "second": "yyyy-MM-dd HH:mm:ss"
                            },
                        },
                        ticks: {
                            callback: false,
                        }
                    }

                } else {
                    getGraphConfig(id).options.scales.y2 = defaultY2Axis;
                }

                // Add a new dataset to the graph
                getGraphConfig(id).data.datasets[1] = {
                    label: "Glacsweb Dataset",
                    showLine: (y2AxisGraphType === "line"),
                    yAxisID: "y2",
                    data: JSON.parse(graphData),
                    parsing: {
                        xAxisKey: xAxisDataSource.toLowerCase(),
                        yAxisKey: y2AxisDataSource.toLowerCase()
                    },
                    borderColor: y2AxisLineColour + "BB",
                    backgroundColor: y2AxisLineColour + "DD",
                }

            } else {
                // Remove any leftover data when Y2 axis disabled
                delete getGraphConfig(id).options.scales.y2;
                getGraphConfig(id).data.datasets = [getGraphConfig(id).data.datasets[0]]

                getGraphConfig(id).y2AxisEnabled = false;
                delete getGraphConfig(id).options.y2AxisDataSource;
            }

            saveConfig(id, getGraphConfig(id));

            // Recreate chart using new configuration
            graphs[id] = new Chart(document.getElementById(`graph${id}`), getGraphConfig(id));

            updateLock = false;
        }, () => {
            // Set the axes internal representation
            getGraphConfig(id).options.xAxisDataSource = [];
            getGraphConfig(id).options.yAxisDataSource = [];

            // Recreate chart using new configuration
            graphs[id] = new Chart(document.getElementById(`graph${id}`), getGraphConfig(id));

            updateLock = false;
        });
    }
}

function saveConfig(id, config) {
    localStorage.setItem(`graph${id}`, JSON.stringify(config))
}

function selectGraph(id, toggleMenu = true) {
    // Select cell element
    let element = document.getElementById(`cell${id}`);

    // Remove highlight background from all cells
    document.querySelectorAll("[id^='cell']").forEach(function (cell) {
        if (cell !== element) {
            cell.classList.remove("bg-highlight");
        }
    });

    let graphFound = false;

    graphConfigs.forEach(function (config) {
        // Check if a graph is in the cell
        if (config.id === id) {
            graphFound = true;

            // Toggle graph selection
            if (selectedGraph === config) {
                selectedGraph = NaN;

            } else {
                selectedGraph = config;
            }

            // Toggle the cell's background highlighting
            if (element.classList.contains("bg-highlight")) {
                element.classList.remove("bg-highlight");

                if (toggleMenu) {
                    // Hide corresponding accordion menu
                    $(`#collapse${id}`).collapse("hide");
                }
            } else {
                element.classList.add("bg-highlight");

                if (toggleMenu) {
                    // Open corresponding accordion menu
                    $(`#collapse${id}`).collapse("show");
                }
            }
        }
    });

    // If the graph doesn't exist, do not select anything
    if (!graphFound) {
        selectedGraph = NaN;

        $("[id^='collapse']").each(function () {
            $(this).collapse("hide");
        });
    }
}

function highlightGraph(id) {
    // Select cell element
    let element = document.getElementById(`cell${id}`);

    // Remove highlight background from all cells
    document.querySelectorAll("[id^='cell']").forEach(function (cell) {
        if (cell !== element) {
            element.style.padding = "11px 11px 11px 11px";

            cell.classList.remove("border");
            cell.classList.remove("border-highlight");
        }
    });

    let graphFound = false;

    graphConfigs.forEach(function (config) {
        // Check if a graph is in the cell
        if (config.id === id) {
            graphFound = true;

            element.style.cursor = "grab";

            // Toggle graph selection
            if (highlightedGraph === config) {
                highlightedGraph = NaN;

            } else {
                highlightedGraph = config;
            }

            // Toggle the cell's background highlighting
            if (element.classList.contains("border")) {
                // Account for 1px border
                element.style.padding = "11px 11px 11px 11px";

                element.classList.remove("border")
                element.classList.remove("border-highlight");

            } else {
                // No longer need to account for border
                element.style.padding = "10px 10px 10px 10px";

                element.classList.add("border");
                element.classList.add("border-highlight")
            }
        }
    });

    // If the graph doesn't exist, do not highlight anything
    if (!graphFound) {
        highlightedGraph = NaN;

        element.style.cursor = "default";
    }
}

function removeGraph(id) {
    // Deselect graph to be deleted
    selectGraph(id, true);

    // Destroy all graphs
    graphs.forEach(function (graph) {
        graph.destroy();
    });

    // Remove all stored references to the graph to be deleted
    localStorage.removeItem(`graph${id}`);
    graphs = graphs.slice(0, id).concat(graphs.slice(id + 1));
    graphConfigs = graphConfigs.slice(0, id).concat(graphConfigs.slice(id + 1));

    // Reset accordion menu
    for (let i = 0; i < 6; i++) {
        let accordionElement = document.getElementById(`accordionItem${i}`);

        if (accordionElement) {
            accordionElement.remove();
        }
    }

    // Move succeeding graphs backwards in the grid
    graphConfigs.slice(id).forEach(function (config) {
        localStorage.removeItem(`graph${config.id}`);

        config.id -= 1;

        localStorage.setItem(`graph${config.id}`, JSON.stringify(config));
    });

    // Reset, then recreate all graphs in correct positions
    graphs = [];
    graphConfigs = [];

    for (let i = 0; i < 6; i++) {
        let config = JSON.parse(localStorage.getItem(`graph${i}`));

        if (config) {
            addGraph(config);
        }
    }
}

function updateDateInputs(graphID) {
    const form = document.querySelector(`#graphForm${graphID}`);
    const formData = new FormData(form);

    // Extract the rover_id option
    const roverID = formData.get("roverId");

    // Update the hard limits on the timestamps
    // Fetch the max and min times from the API
    apiRequest("GET", `api/query/timestamp_min?rover_id=${roverID}`, false, (responseText) => {
        let timestampJSON = JSON.parse(responseText);
        let timestamp = timestampJSON.timestamp;
        let startDateInput = document.getElementById(`startDateInput${graphID}`);

        startDateInput.min = timestamp.split("T")[0];
        startDateInput.value = timestamp.split("T")[0];
    }, () => {
    });

    apiRequest("GET", `api/query/timestamp_max?rover_id=${roverID}`, false, (responseText) => {
        let timestampJSON = JSON.parse(responseText);
        let timestamp = timestampJSON.timestamp;
        let endDateInput = document.getElementById(`endDateInput${graphID}`);

        endDateInput.max = timestamp.split("T")[0];
        endDateInput.value = timestamp.split("T")[0];
    }, () => {
    });
}

function capitaliseLabel(label) {
    return label.charAt(0).toUpperCase() + label.slice(1);
}

function removeSelectedGraph() {
    // Iterate through all graph cells
    document.querySelectorAll("[id^='cell']").forEach(function (cell) {
        // Check if the cell is selected
        if (cell.classList.contains("bg-highlight")) {
            // Delete corresponding selected graph
            let id = parseInt(cell.id.replace("cell", ""));
            removeGraph(id);
        }
    });
}

function exportSelectedGraph() {
    // Iterate through all graph cells
    document.querySelectorAll("[id^='cell']").forEach(function (cell) {
        // Check if the cell is selected
        if (cell.classList.contains("bg-highlight")) {
            // Delete corresponding selected graph
            let id = parseInt(cell.id.replace("cell", ""));
            let image = graphs[id].toBase64Image();

            let a = document.createElement('a');
            a.href = image;
            a.download = `glacsweb_graph${id}_${new Date().toISOString()}.png`;

            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    });
}
