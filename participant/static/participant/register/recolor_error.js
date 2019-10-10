$(function () {
    let error_message = $('li.red_message');

    if (error_message !== undefined)
    {
        $("div#messages").css('background', '#cc0000');
    }
});