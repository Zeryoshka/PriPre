var NUM_LEN = 7

Plotly.plot('chart', {}, {})

$('#form').on('submit', function(e){
    let start = $('#date_start').val()
    let end = $('#date_end').val()
    if (start >= end) {
        alert('Неверный временной промежуток')
        return false
    }

    $.ajax({
        url: '/get_stats',
        type: 'GET',
        data: $('#form').serialize(),
        dataType: 'json',
        success: function(json){
            $('#stat-avg').text(json.stats.avg.toPrecision(NUM_LEN))
            $('#stat-median').text(json.stats.median.toPrecision(NUM_LEN))
            $('#stat-variants').text(json.stats.variants.toPrecision(NUM_LEN))
            $('#stat-mode').text(json.stats.mode.toPrecision(NUM_LEN))
            $('#stat-std').text(json.stats.std.toPrecision(NUM_LEN))
            Plotly.newPlot('chart', json.chart)
        },
        statusCode: {
            400: function() {
              alert('Неверные параметры запроса')
            }
        }
    })
    return false
});