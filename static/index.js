// index.js

function setGame(variable, val) {
    $.ajax({
        type: 'POST',
        url: '/set_game?var=' + variable + '&val=' + val,
        success: function(response) {
            console.log("Succesfully updated " + variable + " to " + val);
            window.location.reload();
        },
        error: function(error) {
            console.log("setGame() Didn't work.")
        }
    });
}

function setDate(dateString, type) {
    $.ajax({
        type: 'POST',
        url: '/set_date?date=' + dateString + "&type=" + type,
        success: function(response) {
            console.log("Succesfully update " + dateString + " to " + type);
            window.location.reload();
        },
        error: function(error) {
            console.log("setDate() Didn't work.")
        }
    });
}

$(document).ready(function() {

    $('.game-select #ac').click(function() {
        setGame('game', 'AC');
    });

    $('.game-select #mfc').click(function() {
        setGame('game', 'MFC');
    })

    $('.select-start-date button').click(function() {
        var thisId = $(this).attr('id');
        setDate(thisId, "start")
    });

    $('.select-end-date button').click(function() {
        var thisId = $(this).attr('id');
        setDate(thisId, "end")
    });
});