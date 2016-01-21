$(function () {

});

function next() {
    console.log("refresh pushed")
    $.getJSON('/next', function (data) {
        refresh()
    });
};

function refresh() {
    console.log("refresh pushed")
    //$.getJSON('/chart/data', function (data) {
    //});
    //$.getJSON('/status', function (data) {
    //});
    location.reload(true);
};