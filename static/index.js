// index.js

function setSessionVar(variable, val) {
    $.ajax({
        type: 'POST',
        url: '/set_session_variable?var=' + variable + '&val=' + val,
        success: function(response) {
            console.log("Succesfully updated " + variable + " to " + val)
        },
        error: function(error) {
            console.log("Didn't work.")
        }
    })
}

$(document).ready(function() {

    $('.game-select #ac').click(function() {
        setSessionVar('game', 'AC');
        $('#game-label').text("AC");
    });

    $('.game-select #mfc').click(function() {
        setSessionVar('game', 'MFC');
        $('#game-label').text("MFC");
    })

    $('.select-start-date button').click(function() {
        console.log("button clickeD!");
        var thisId = $(this).attr('id');
        console.log(thisId);
    });

    $('.select-end-date button').click(function() {
        console.log("button clickeD!");
    });
});