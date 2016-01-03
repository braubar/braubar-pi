$(document).ready(function () {
    // Get context with jQuery - using jQuery's .get() method.
    var ctx = $("#myChart").get(0).getContext("2d");
    // This will get the first returned node in the jQuery collection.
    $.getJSON('/brew/chart/data', function (data) {
        chart(data)
    });

    function chart(temp_data) {



        console.log(Object.keys(temp_data));
        //var labels = Object.keys(temp_data);
        //var temp_current =  $.map(temp_data, function(element,index) {return console.log(JSON.parse(element)); });
        //var temp_target =  $.map(temp_data, function(element,index) {return element["temp_target"]});
        console.log(temp_data.date)
        var data = {
            labels: temp_data.date,
            datasets: [
                {
                    label: "Temperature Current",
                    fillColor: "rgba(0,220,220,0.2)",
                    strokeColor: "rgba(0,220,220,1)",
                    pointColor: "rgba(0,220,220,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(220,220,220,1)",
                    data: temp_data.target
                },
                {
                    label: "Temperature expected",
                    fillColor: "rgba(151,187,205,0.2)",
                    strokeColor: "rgba(151,187,205,1)",
                    pointColor: "rgba(151,187,205,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(151,187,205,1)",
                    data: temp_data.temp
                },
                {
                    label: "Temperature expected",
                    fillColor: "rgba(101,187,205,0.2)",
                    strokeColor: "rgba(101,187,205,1)",
                    pointColor: "rgba(101,187,205,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(101,187,205,1)",
                    data: temp_data.change
                }
            ]
        };

        var options_a = {

            ///Boolean - Whether grid lines are shown across the chart
            scaleShowGridLines: true,
            //String - Colour of the grid lines
            scaleGridLineColor: "rgba(0,0,0,.05)",
            //Number - Width of the grid lines
            scaleGridLineWidth: 1,
            //Boolean - Whether to show horizontal lines (except X axis)
            scaleShowHorizontalLines: true,
            //Boolean - Whether to show vertical lines (except Y axis)
            scaleShowVerticalLines: true,
            scaleOverride: true,
            scaleStartValue: -7,
            scaleStepWidth: 5,
            scaleSteps: 23,
            //Boolean - Whether the line is curved between points
            bezierCurve: true,
            //Number - Tension of the bezier curve between points
            bezierCurveTension: 0.4,
            //Boolean - Whether to show a dot for each point
            pointDot: true,
            //Number - Radius of each point dot in pixels
            pointDotRadius: 3,
            //Number - Pixel width of point dot stroke
            pointDotStrokeWidth: 1,
            //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
            pointHitDetectionRadius: 10,
            //Boolean - Whether to show a stroke for datasets
            datasetStroke: true,
            //Number - Pixel width of dataset stroke
            datasetStrokeWidth: 5,
            //Boolean - Whether to fill the dataset with a colour
            datasetFill: false,
            //String - A legend template
            legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"
        };


        var myNewChart = new Chart(ctx).Line(data, options_a);

        Chart.defaults.global = {
            // Boolean - Whether to animate the chart
            animation: true,
            // Number - Number of animation steps
            animationSteps: 60,
            // String - Animation easing effect
            // Possible effects are:
            // [easeInOutQuart, linear, easeOutBounce, easeInBack, easeInOutQuad,
            //  easeOutQuart, easeOutQuad, easeInOutBounce, easeOutSine, easeInOutCubic,
            //  easeInExpo, easeInOutBack, easeInCirc, easeInOutElastic, easeOutBack,
            //  easeInQuad, easeInOutExpo, easeInQuart, easeOutQuint, easeInOutCirc,
            //  easeInSine, easeOutExpo, easeOutCirc, easeOutCubic, easeInQuint,
            //  easeInElastic, easeInOutSine, easeInOutQuint, easeInBounce,
            //  easeOutElastic, easeInCubic]
            animationEasing: "easeOutQuart",
            // Boolean - If we should show the scale at all
            showScale: true,
            // Boolean - If we want to override with a hard coded scale
            scaleOverride: false,
            // ** Required if scaleOverride is true **
            // Number - The number of steps in a hard coded scale
            scaleSteps: null,
            // Number - The value jump in the hard coded scale
            scaleStepWidth: null,
            // Number - The scale starting value
            scaleStartValue: null,
            // String - Colour of the scale line
            scaleLineColor: "rgba(0,0,0,.1)",
            // Number - Pixel width of the scale line
            scaleLineWidth: 1,
            // Boolean - Whether to show labels on the scale
            scaleShowLabels: true,
            // Interpolated JS string - can access value
            scaleLabel: "<%=value%>",
            // Boolean - Whether the scale should stick to integers, not floats even if drawing space is there
            scaleIntegersOnly: true,
            // Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
            scaleBeginAtZero: false,
            // String - Scale label font declaration for the scale label
            scaleFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
            // Number - Scale label font size in pixels
            scaleFontSize: 12,
            // String - Scale label font weight style
            scaleFontStyle: "normal",
            // String - Scale label font colour
            scaleFontColor: "#666",
            // Boolean - whether or not the chart should be responsive and resize when the browser does.
            responsive: true,
            // Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
            maintainAspectRatio: true,
            // Boolean - Determines whether to draw tooltips on the canvas or not
            showTooltips: true,
            // Function - Determines whether to execute the customTooltips function instead of drawing the built in tooltips (See [Advanced - External Tooltips](#advanced-usage-custom-tooltips))
            customTooltips: false,
            // Array - Array of string names to attach tooltip events
            tooltipEvents: ["mousemove", "touchstart", "touchmove"],
            // String - Tooltip background colour
            tooltipFillColor: "rgba(0,0,0,0.8)",
            // String - Tooltip label font declaration for the scale label
            tooltipFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
            // Number - Tooltip label font size in pixels
            tooltipFontSize: 14,
            // String - Tooltip font weight style
            tooltipFontStyle: "normal",
            // String - Tooltip label font colour
            tooltipFontColor: "#fff",
            // String - Tooltip title font declaration for the scale label
            tooltipTitleFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
            // Number - Tooltip title font size in pixels
            tooltipTitleFontSize: 14,
            // String - Tooltip title font weight style
            tooltipTitleFontStyle: "bold",
            // String - Tooltip title font colour
            tooltipTitleFontColor: "#fff",
            // Number - pixel width of padding around tooltip text
            tooltipYPadding: 6,
            // Number - pixel width of padding around tooltip text
            tooltipXPadding: 6,
            // Number - Size of the caret on the tooltip
            tooltipCaretSize: 8,
            // Number - Pixel radius of the tooltip border
            tooltipCornerRadius: 6,
            // Number - Pixel offset from point x to tooltip edge
            tooltipXOffset: 10,
            // String - Template string for single tooltips
            tooltipTemplate: "<%if (label){%><%=label%>: <%}%><%= value %>",
            // String - Template string for multiple tooltips
            multiTooltipTemplate: "<%= value %>",
            // Function - Will fire on animation progression.
            onAnimationProgress: function () {
            },
            // Function - Will fire on animation completion.
            onAnimationComplete: function () {
            }
        }
    }
});



