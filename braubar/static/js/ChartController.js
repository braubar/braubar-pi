$(document).ready(function () {
    var socket = io();
    var chart;
    socket.on('connect', function () {
        socket.emit('connected', {data: 'I\'m connected!'});
        // console.log("connected to " + document.domain + " at port: " + location.port)
        socket.on("disconnect", function () {
            console.log("disconnected")
        })
    });
    socket.on('fullchart', function (data) {
        chart = InitChart(JSON.parse(data));
    });
    socket.on('update chart', function (dat) {
        data = JSON.parse(dat);
        // console.log(dat)
        update_chart(chart, data);
        update_board(data);
    });

    socket.on('fullchart', function (data) {
        chart = InitChart(JSON.parse(data));
    });

    socket.on("next", function (dat) {
        data = JSON.parse(dat);
        if (!data.ok) {
            alert("something went wrong")
        } else {
            $("#next").css("background-color", "#ffb64d")
        }
        update_board(data.status)

    });
    
    $("#refresh").click(function () {
        socket.emit("update chart", {msg: 'update los los!'})
    });

    $("#next").click(function () {
        // console.log("next clicked")
        $("#next").css("background-color", "red")
        socket.emit("next", {msg: "next"})
    });

    setInterval(function () {
        socket.emit("update chart", {msg: 'update los los!'})
    }, 5000)
});

function update_board(data) {
    $("#current_temp_val").text(data.current_temp);
    $("#state_val").text(data.current_state);
    $("#target_temp_val").text(data.target_temp);
    $("#timer_value").text(data.timer_passed/60); // TODO timer_delta
    $("#temp_increase_val").text(data.temp_increase);
    $("#brew_time_val").text(data.duration);
}

function update_chart(chart, dataa) {
    chart.flow({
        x: 'brew_time',
            xFormat: '%Y-%m-%dT%H:%M:%S.%L',
        columns: [
            ['brew_time', dataa.brew_time],
            ['current_temp', dataa.current_temp],
            ['target_temp', dataa.target_temp],
            ['change', dataa.change]
        ],
        keys: {
            value: ['brew_time', 'current_temp', 'target_temp', 'change']
        },
        length: 0
    })
}
function InitChart(data) {
    // console.log(data);
    var chart = c3.generate({
        bindto: '#temp-chart',
        size: {
            width: 740,
            height: 300
        },
        data: {
            types: {
                current_temp: 'line',
                target_temp: 'area-step',
                change: 'step'
            } ,
            x: 'brew_time',
            xFormat: '%Y-%m-%dT%H:%M:%S.%L',
            json: data,
            keys: {
                value: ['brew_time', 'current_temp', 'target_temp', 'change']
            },
            colors: {
                current_temp: '#2eb82e',
                target_temp: '#e68a00',
                change: '#cccc00'
            },
            names: {
                current_temp: 'Current Temperature',
                target_temp: 'Target Temperature',
                change: 'PID Output (50 is 0.0)'
            }
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    format: '%H:%M',
                    culling: {
                        max: 10
                    },
                    count: 10,
                }
            }
        },
        transition: {
            duration: 0
        },
        point: {
            show: false
        }
    });
    return chart
}
