function dateSorter(a, b){
    a = a.split(" | ");
    aDMY = a[0].split("/");
    a = a[1].split(":");

    b = b.split(" | ");
    bDMY = b[0].split("/");
    b = b[1].split(":");

    a = new Date(aDMY[2], aDMY[1]-1, aDMY[0], a[0], a[1]).getTime();
    b = new Date(bDMY[2], bDMY[1]-1, bDMY[0], b[0], b[1]).getTime();

    return a - b;
}

function percentFormatter(value) {
    return value + " %";
}