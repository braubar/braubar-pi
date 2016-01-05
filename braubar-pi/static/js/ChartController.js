$(document).ready(function () {
    // Get context with jQuery - using jQuery's .get() method.
    // This will get the first returned node in the jQuery collection.
    $.getJSON('/brew/chart/data', function (data) {
        InitChart(data);
    });

//https://github.com/gildean/PiTherm
});


function InitChart(data) {

    var lineData = data;
    var calcTime = function(start, end) {
        return (Date.parse(start) - end)/1000/60
    };

    var vis = d3.select("#mychart"),
        WIDTH = 690,
        HEIGHT = 300,
        MARGINS = {
            top: 20,
            right: 20,
            bottom: 20,
            left: 50
        },
        xRange = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(lineData, function (d) {
            return calcTime(d.date, d.brew_id);
        }),
            d3.max(lineData, function (d) {
                return calcTime(d.date, d.brew_id);
            })
        ]),

        yRange = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([d3.min(lineData, function (d) {
            return d.current;
        }),
            d3.max(lineData, function (d) {
                return Math.max(d.current, d.target);
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
            return xRange(calcTime(d.date, d.brew_id));
        })
        .y(function (d) {
            return yRange(d.current);
        })
        .interpolate('linear');

    var targetTempLine = d3.svg.line()
        .x(function (d) {
            return xRange(calcTime(d.date, d.brew_id));
        })
        .y(function (d) {
            return yRange(d.target);
        })
        .interpolate('linear');

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