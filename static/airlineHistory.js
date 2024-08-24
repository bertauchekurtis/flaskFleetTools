window.onload = function(){
    const ctx = document.getElementById('airlineChart');
    $.get("/getAirlineHistory?airline=" + $('#airlineName').text(), function(data){
        console.log("Data gotted!");
        const totals = data["totals"];
        const dates = data["dates"];
        console.log(totals);

        new Chart(ctx, {
            type: 'line',
            data: {
              labels: dates,
              datasets: [{
                label: 'Total Number of Aircraft',
                data: totals,
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          });
    });
};

