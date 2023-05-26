jQuery.expr.filters.offscreen = function(el) {
    var rect = el.getBoundingClientRect();
    return (
                (rect.x + rect.width) < 0 
                || (rect.y + rect.height) < 0
                || (rect.x > window.innerWidth || rect.y > window.innerHeight)
            );
};

$(".dropdown-menu li").hover(function(){
    var submenu = $(this).children(".submenu");
    if (submenu.is(":offscreen")){
        submenu.css("left", "0%");
        submenu.css("right", "100%");
    }
})

$(document).on({
    mouseenter: function () {
        $(".card-flex").addClass("no-hover");
    },
    mouseleave: function () {
        $(".card-flex").removeClass("no-hover");
    }
}, ".card-flex > .card");

var timezoneTables = [];
var timezoneCharts = [];

$(document).on("change", "select[name=timezone]", function(){
    $.ajax({
        type: "GET",
        data: {
            timezone: $("select[name=timezone]").val(),
        },
        success: function(response){
            timezoneTables.forEach(function(t){t.bootstrapTable('refresh');});
            timezoneCharts.forEach(function(func){func();});
        },
        error: function(response){
            throw(response);
        },
    })
})

const cardHTML = `
<div class="card hidden">
    <div class="card-header pe-2">
        <div class="btn-group w-100">
            <button class="btn btn-outline-success fw-bold text-start" disabled>None</button>
            <button type="button" class="btn btn-success dropdown-toggle dropdown-toggle-split flex-grow-0" data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false">
                <span class="visually-hidden">Toggle Dropdown</span>
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
                <li><h6 class="dropdown-header">Choose statistic...</h6></li>
                <li><button class="dropdown-item active" type="button" value="0">None</button></li>
                <li><hr class="dropdown-divider"></hr></li>
                <li>
                <button class="dropdown-item d-flex unclickable" type="button">Title Overview<span class="ms-auto">»</span></button>
                <ul class="dropdown-menu submenu">
                    <li><button class="dropdown-item" type="button" value="3">Time Period Overview</button></li>
                    <li><button class="dropdown-item" type="button" value="8">All-Time Avg. Overview</button></li>
                </ul>
                <li>
                    <button class="dropdown-item d-flex unclickable" type="button">Counts<span class="ms-auto">»</span></button>
                    <ul class="dropdown-menu submenu">
                        <li><button class="dropdown-item" type="button" value="1">Words</button></li>
                        <li><button class="dropdown-item" type="button" value="2">Emojis</button></li>
                        <li><button class="dropdown-item" type="button" value="9">Characters</button></li>
                    </ul>
                </li>
                <li>
                    <button class="dropdown-item d-flex unclickable" type="button">
                        <span>Sorts <span class="badge rounded-pill bg-warning text-dark">wide</span></span>
                        <span class="ms-auto">»</span>
                    </button>
                    <ul class="dropdown-menu submenu">
                        <li><button class="dropdown-item" type="button" value="5" data-type="wide">Length</button></li>
                        <li><button class="dropdown-item" type="button" value="6" data-type="wide">Capital Letters</button></li>
                    </ul>
                </li>
                <li><button class="dropdown-item" type="button" value="4">Category Chart</button></li>
                <li><button class="dropdown-item" type="button" value="7">Entries per Hour Chart</button></li>
            </ul>
            <button type="button" class="btn-close ms-2" aria-label="Close"></button>
        </div>
    </div>
    <div class="card-body"></div>
</div>
<div class="add-icon-div">
    <svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" fill="currentColor" class="bi bi-plus-square add-icon" viewBox="0 0 16 16">
        <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>
        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
    </svg>
</div>
`;

var cardContentID = 0;
function FillCard(card, id){
    let btn = $(card).find(`button[value=${id}]`)
    btn.parents('.dropdown-menu-end').find('.active').removeClass("active");
    btn.addClass("active");
    btn.parents('.btn-group').children().first().html(btn.text());

    if ($(`.card .dropdown-menu button[value="${id}"]`).attr("data-type")){
        card.addClass("card-wide");
    }

    if (id == "0"){
        card.find(".card-body").html("");
    }
    else{
        $.ajax({
            type: "POST",
            data: {
                csrfmiddlewaretoken: window.CSRF_TOKEN, 
                id: id, 
                cardContentID: cardContentID,
            },
            success: function(response){
                card.find(".card-body").html(response);
            },
            error: function(response){
                throw(response);
            },
            complete: function(data){
                $("table[data-toggle='table']").bootstrapTable();
            }
        })
        cardContentID += 1;
    }
}

function AppendCard(id = 0, start = false){
    $(".add-icon-div").last().replaceWith(cardHTML);

    $(".card.hidden").fadeIn(400, function(){
        $(this).removeClass("hidden");
        $(this).css("display", "flex")
    });
    
    if (id != 0){
        FillCard($(".card").last(), id);
    }

    if (!start){
        let url = new URL(window.location);
        let t = url.searchParams.get("t");
        url.searchParams.set('t', t+id);
        window.history.pushState({}, '', url);
    }
}

function DeleteCard(card){
    let i = $(".card").index(card);
    let url = new URL(window.location);
    let t = url.searchParams.get("t");
    t = t.substring(0, i) + t.substring(i + 1);
    url.searchParams.set('t', t);
    window.history.pushState({}, '', url);

    card.remove();
}

$(document).on("click", "button.btn-close", function(){
    let card = $(this).parents(".card")
    card.fadeOut(200, function(){
        DeleteCard(card);
    });
});

$(".unclickable").click(function(e){
    e.stopPropagation();
    if (this.next().hasClass("submenu")){
        this.next().css("display", "block");
    }
})

$(document).on("click", ".dropdown-menu li button", function(){
    let btn = $(this);
    if (!btn.hasClass("unclickable")){
        bootstrap.Dropdown.getInstance($(this).parents(".dropdown-menu").last().prev()).toggle();

        let card = btn.parents(".card");
        let id = btn[0].getAttribute("value");
        FillCard(card, id);
              
        let url = new URL(window.location);
        let t = url.searchParams.get("t");
        let i = $(".card").index(card);
        t = t.substring(0, i) + id + t.substring(i + 1);
        url.searchParams.set('t', t);
        window.history.pushState({}, '', url);
    }
});

$(document).on("click", ".add-icon", function(){
    AppendCard();
});

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

    $.ajax({
        type: "POST",
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN, 
            duplicates: this.checked,
        },
        success: function(response){
            location.reload();
        },
        error: function(response){
            throw(response);
        },
    })
})

const CARD_LIMIT = 10
function Start(){
    let duplicates = localStorage.getItem("duplicates") == "no";
    $("#duplicatesCheckbox")[0].checked = duplicates;
    $.ajax({
        type: "POST",
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN, 
            duplicates: duplicates,
        },
        error: function(response){
            throw(response);
        },
    })

    let url = new URL(window.location);
    let t = url.searchParams.get('t');
    if (t){
        for (let i = 0; i < t.length && i < CARD_LIMIT; i++){
            AppendCard(t[i], true);
        }
    }
}
Start();
