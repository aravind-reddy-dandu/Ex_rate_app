function showCurr() {

    // Get date element
    let dateObj = document.getElementById('example-date-input');
    dateObj = dateObj.valueAsDate
    //Get decomposition. Month starts from 0 in this
    const month = dateObj.getUTCMonth() + 1;
    const day = dateObj.getUTCDate();
    const year = dateObj.getUTCFullYear();
    //Old method to get values directly from API
    // ex_url = 'https://api.exchangeratesapi.io/' + year + '-' + month + '-' + day + '?base=' + selectedValue;
    //Build URL
    let ex_url = '/get_rate_loc/' + selectedValue + '/' + year + '/' + month + '/' + day;
    $.ajax({
        url: ex_url,
        type: 'GET',
        success: function (response) {
            //Getting table and appending rows to it
            let tbody = $('#table_body').empty();
            $.each(response.rates, function (key, rate) {
                $('<tr>').append(
                    $('<td>').text(key),
                    $('<td>').text(rate)).appendTo(tbody);
            });
        },
        error: function (error) {
            console.log(error);
        }
    });

}

//Some functions to be executed in the start after document load
//This is to populate the dropdown with available currencies
$(function () {
    // $('#example-date-input').datepicker({
    //     endDate: "now()"
    // });
    let currencies = 'CAD,HKD,PHP,DKK,HUF,CZK,GBP,RON,SEK,IDR,INR,BRL,RUB,LTL,EEK,JPY,THB,CHF,EUR,MYR,BGN,TRY,CNY,NOK,NZD,ZAR,USD,MXN,SGD,AUD,KRW,PLN,HRK'.split(',');
    currencies.forEach(function (item, index) {
        $("#items_list").append('<li><a class=\"dropdown-item\" href="#">' + item + '</a></li>');
    })
});

let selectedValue = '';

//To populate selected item on dropdown label
$(document).ready(function () {
    $('.dropdown').each(function (key, dropdown) {
        let $dropdown = $(dropdown);
        $dropdown.find('.dropdown-menu a').on('click', function () {
            $dropdown.find('button').text($(this).text()).append(' <span class="caret"></span>');
            selectedValue = $(this).text();
        });
    });
});