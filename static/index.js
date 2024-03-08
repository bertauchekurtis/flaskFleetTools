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

function clearCoookies() {
    $.ajax({
        type: 'POST',
        url: '/clear_cookies',
    });
}

function toggleAircraftTables(tableToShow) {
    const tableids = ["top-20-table","biggest-popularity-changes-table","fastest-growing-aircraft-table","fastest-shrinking-aircraft-table","raw-aircraft-table"];
    indexToShow = tableids.indexOf(tableToShow);
    tableids.splice(indexToShow, 1);
    var divToShow = document.getElementById(tableToShow);
    divToShow.style.display = 'block';
    for(var i = 0; i < tableids.length; i++) {
        console.log(tableids[i]);
        var divToHide = document.getElementById(tableids[i]);
        divToHide.style.display = 'none';
    }
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

    $('.home-button').click(function() {
        window.location.href = "/";
    })

    $('#cookie').click(function() {
        clearCoookies();
    })

    $('#circulation-tables-buttons button').click(function() {
        var thisButtonId = $(this).attr('class');
        toggleAircraftTables(thisButtonId);
    })
});
