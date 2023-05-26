var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
})

$("#temperatureRange").on("input", function(){
    $("#temperatureValueLabel").html($(this).val());
});

const loadingHTML = `
<div class="flex-grow-1 d-flex justify-content-center align-items-center">
    <div class="spinner-border text-success m-5" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>
</div>
`;

var resultHistory = [];

function parseHistory(){
    return `
    <h4>History</h4>
    <div class="d-flex flex-column flex-grow-1 opacity-75">
        ${(function(){
            let res = "";
            resultHistory.slice().reverse().forEach(function(obj){
                res += `
                <div class="col-auto bg-dark rounded-top p-1 align-self-start">
                    <span class="badge bg-warning" name="startInput">${obj.input}</span>
                    <span class="badge bg-danger" name="minLength">${obj.length}</span>
                    <span class="badge bg-primary" name="temperature">${obj.temp}</span>
                </div>
                <div class="fs-5 text-break bg-dark p-2 mb-2" name="title">${obj.result}</div>
                `;
            });
            return res;
        })()}
    </div>
    `;
}

function parseResult(input, length, temp, res, similars){
    return `
    <div class="col-auto bg-teal rounded-top p-1 align-self-start">
        <span class="badge bg-warning" name="startInput">${input}</span>
        <span class="badge bg-danger" name="minLength">${length}</span>
        <span class="badge bg-primary" name="temperature">${temp}</span>
    </div>
    <div class="fs-5 text-break bg-teal p-2" name="title">${res}</div>
    <table class="table table-sm table-bordered caption-bottom mb-0">
        <caption>Three most similar original titles</caption>
        <thead>
            <tr>
                <th scope="col" width="150px">Time</th>
                <th scope="col">Title</th>
                <th scope="col" width="50px">Distance</th>
            </tr>
        </thead>
        <tbody>
            ${(function(){
                let res = "";
                similars.forEach(function(row){
                    res += `
                    <tr>
                        <td>${row.time}</td>
                        <td><div class="text-break">${row.title}</div></td>
                        <td>${row.distance}</td>
                    </tr>
                    `;
                });
                return res;
            })()}
        </tbody>
    </table>
    `;
}

$("#generatorForm").submit(function(event) {
    event.preventDefault();

    let input = $("#startInput").val();
    let length = $("#minLength").val();
    let temp = $("#temperatureRange").val();

    let resultHTML = $("#result");
    if (resultHTML.children().length){
        if (resultHistory.length >= 3){
            resultHistory.shift();
        }
        resultHistory.push({
            input: resultHTML.find("[name='startInput']").text(),
            length: resultHTML.find("[name='minLength']").text(),
            temp: resultHTML.find("[name='temperature']").text(),
            result: resultHTML.find("[name='title']").text(),
        });
    }
    if (resultHistory.length){
        $("#resultHistory").html(parseHistory());
    }

    $.ajax({
        type: "POST",
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            startInput: input,
            minLength: length,
            temperature: temp},
        beforeSend: function(c){
            $("#result").html(loadingHTML);
        },
        success: function(response){
            if (!input) input = String.fromCodePoint(response.result.codePointAt(0));

            $("#result").html(parseResult(input, length, temp, response.result, response.similars));
        },
        error: function(response){
            $("#result").html("");
            throw(response);
        },
    });
});

function SavePage(){
    let formData = [$("#startInput").val(), $("#minLength").val(), $("#temperatureRange").val()];
    localStorage.setItem("formData", JSON.stringify(formData));

    if ($("#result").children().length){
        let headers = ["time", "title", "distance"];
        let similars = [];
        $('#result tbody tr').each(function(i) {
            let rowObj = {};
            $(this).find('td').each(function(i) {
                rowObj[headers[i]] = $(this).text()
            });
            if (rowObj) similars.push(rowObj);
        });

        let lastResult = {input: $("#result [name='startInput']").text(),
                        length: $("#result [name='minLength']").text(),
                        temp: $("#result [name='temperature']").text(),
                        res: $("#result [name='title']").text(),
                        similars: similars};
        sessionStorage.setItem("lastResult", JSON.stringify(lastResult));
    }
    else{
        sessionStorage.removeItem("lastResult");
    }

    sessionStorage.setItem("resultHistory", JSON.stringify(resultHistory));
}

$(window).on("beforeunload", SavePage);


$(document).ready(function() {
    let formData = JSON.parse(localStorage.getItem("formData"));
    if (formData){
        $("#startInput").val(formData[0]);
        $("#minLength").val(formData[1]);
        $("#temperatureRange").val(formData[2]).trigger("input");
    }

    let lastResult = JSON.parse(sessionStorage.getItem("lastResult"));
    if (lastResult){
        $("#result").html(parseResult(lastResult.input, lastResult.length, lastResult.temp, lastResult.res, lastResult.similars));
    }

    let historyObj = JSON.parse(sessionStorage.getItem("resultHistory"));
    if (historyObj && historyObj.length){
        resultHistory = historyObj;
        $("#resultHistory").html(parseHistory());
    }
});