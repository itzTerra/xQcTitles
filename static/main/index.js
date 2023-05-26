const table = $("#table");

$(document).on("click", "[name=refresh]", function(){
    table.bootstrapTable('refresh');
})

function queryParams(params){
    params.duplicates = localStorage.getItem("duplicates");
    return params;
}

$(document).on("change", "select[name=timezone]", function(){
    $.ajax({
        type: "GET",
        data: {
            timezone: $("select[name=timezone]").val(),
        },
        success: function(response){
            table.bootstrapTable('refresh');
        },
        error: function(response){
            throw(response);
        },
    })
})

var djangoContext = JSON.parse(document.getElementById('djangoContext').textContent);
const duplicateInfoPopover = new bootstrap.Popover(document.getElementById('duplicateCheckInfo'), 
    {trigger: "hover click",
    delay: { "show": 500, "hide": 100 },
    html: true,
    sanitize: false,
    content: `
    <p class="mb-1">Filters out similar entries from within the same time period.</p>
    <strong>Example:</strong>
    <table class="fs-6 my-2">
        <tbody>
            <tr class="bg-error">
                <td>01/12/2021 | 04:42</td>
                <td>LAST MAN STANDING ON TWITCH.TV HAVING MID-LIFE CRISIS STREAMS WASHED UP CONTENT (IMPOSSIBLE)</td>
            </tr>
            <tr>
                <td>01/12/2021 | 04:41</td>
                <td>LAST MAN STANDING ON TWITCH.TV HAVING MID-LIFE CRISIS STREAMS WASHED UP CONTENT (IMPOSSIBLE) !HelloFresh | USE CODE XQC14 #AD</td>
            </tr>
        </tbody>
    </table>
    <p>The entries to be filtered have to be reviewed manually. (Newer entries may still be duplicate.)</p>
    <div class="fw-semibold text-center bg-primary">
        <p class="mb-0">Filter Ratio: <span class="fw-bolder">${Math.round(djangoContext.filterCount / djangoContext.entryCount * 100)} %</span> (${djangoContext.filterCount}/${djangoContext.entryCount})</p>
        <p class="mb-0">Last Review: <span class="fw-bolder">${djangoContext.ndLastReview}</span></p>
    </div>
    `
});

$("#duplicatesCheckbox").change(function(){
    localStorage.setItem("duplicates", this.checked ? "no" : "yes");
    table.bootstrapTable('refresh');
})
$("#duplicatesCheckbox")[0].checked = localStorage.getItem("duplicates") == "no";

var pageSize = 10;
table.on('load-success.bs.table', function (e, data) {
    pageSize = table.bootstrapTable('getOptions').pageSize;
});

table.on('page-change.bs.table', function (e, number, size) {
    if (size == pageSize) return;
    pageSize = size;

    if (size == "All"){
        table.bootstrapTable('refreshOptions', {
            exportDataType: 'all'
        });
    }
    else{
        table.bootstrapTable('refreshOptions', {
            exportDataType: 'basic'
        });
    }
});