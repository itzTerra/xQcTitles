function FilterButton(){
    return `
    <button type="button" class="btn btn-danger"><i class="bi bi-x-lg"></i></button>
    `;
}

function RevertButton(){
    return `
    <button type="button" class="btn btn-success"><i class="bi bi-arrow-90deg-left"></i></button>
    `;
}

$(document).on("click", "td button", function(){
    $.ajax({
        type: "GET",
        data: {filterEntry: $(this).parents("tr").find("td").html()},
        success: function(response){
            $("table[data-toggle='table']").bootstrapTable('refresh');
        },
        error: function(response){
            throw(response);
        }
    })
});

const table = $("#table");

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