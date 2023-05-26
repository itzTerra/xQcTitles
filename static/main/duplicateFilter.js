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

function Lerp(a, b, t){
    return Math.max(a, Math.min((t * a) + ((1-t) * b), b));;
}

function InverseLerp(a, b, v){
    return Math.max(0, Math.min((v - a) / (b - a), 1));
}

$("#table").on("reset-view.bs.table virtual-scroll.bs.table", function(){
    $(this).find("tbody tr").each(function(){
        var ed = $(this).children().eq(-2).html();
        var hue = Lerp(0, 230, InverseLerp(0, 140, ed));
        $(this).css("background-color", `hsl(${230-hue}, 40%, 30%)`);
    })
})
