$(document).ready(function () {
    $.getJSON('/chart/data', function (data) {
        InitChart(data);
    });
});


function InitChart(data) {

    var lineData = data;
    var calcTime = function(start, current) {
        return (Date.parse(current) - start)/1000/60
    };

    var vis = d3.select("#mychart"),
        WIDTH = 690,
        HEIGHT = 280,
        MARGINS = {
            top: 20,
            right: 20,
            bottom: 20,
            left: 50
        },
        xRange = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(lineData, function (d) {
            return calcTime(d.brew_id, d.date);
        }),
            d3.max(lineData, function (d) {
                return calcTime(d.brew_id, d.date);
            })
        ]),

        yRange = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([
            d3.min(lineData, function (d) {
                return Math.min(d.current, d.target);
            }),
            d3.max(lineData, function (d) {
                return Math.max(d.current, d.target, d.change);
            })
        ]),

        xAxis = d3.svg.axis()
            .scale(xRange)
            .tickSize(5)
            .tickSubdivide(true),

        yAxis = d3.svg.axis()
            .scale(yRange)
            .tickSize(5)
            .orient("left")
            .tickSubdivide(true);

    vis.append("svg:g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")")
        .call(xAxis);

    vis.append("svg:g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + (MARGINS.left) + ",0)")
        .call(yAxis);

    var currentTempLine = d3.svg.line()
        .x(function (d) {
            return xRange(calcTime(d.brew_id, d.date));
        })
        .y(function (d) {
            return yRange(d.current);
        })
        .interpolate('linear');

    var targetTempLine = d3.svg.line()
        .x(function (d) {
            return xRange(calcTime(d.brew_id, d.date));
        })
        .y(function (d) {
            return yRange(d.target);
        })
        .interpolate('linear');

    var change = d3.svg.line()
        .x(function (d) {
            return xRange(calcTime(d.brew_id, d.date));
        })
        .y(function (d) {
            return yRange(d.change);
        })
        .interpolate('linear');

    vis.append("svg:path")
        .attr("d", change(data))
        .attr("stroke", "#FFCC00")
        .attr("stroke-width", 1)
        .attr("fill", "none");

    vis.append("svg:path")
        .attr("d", currentTempLine(data))
        .attr("stroke", "blue")
        .attr("stroke-width", 2)
        .attr("fill", "none");

    vis.append("svg:path")
        .attr("d", targetTempLine(data))
        .attr("stroke", "green")
        .attr("stroke-width", 2)
        .attr("fill", "none");
}
