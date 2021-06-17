Plotly.plot('chart', {}, {});

function create_data_obj() {
    let models = []
    $('.select-models__checkbox').each(function(index, checkbox) {
        if ($(checkbox).is(':checked'))
            models.push($(checkbox).attr('name'))
    })

    let ans = {
        ticket: $('#ticket-select').val(),
        models: models
    }
    return ans;
}

$('.form__submit').click(function (){

    $.ajax({
        url: '/plot/past',
        method: 'POST',
        data: JSON.stringify(create_data_obj()),
        contentType: "application/json",
        dataType: 'json',
        success: function(data) {
            Plotly.newPlot('chart', data, {})
        }
    })

    return false
});

$(window).resize(function(){
    location = location
});