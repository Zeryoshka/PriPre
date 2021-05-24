Plotly.plot('chart', {}, {})

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
        method: 'get',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(create_data_obj()),
        success: function(data) {
            Plotly.plot('chart', data, {})
        }
    })
    return false
});