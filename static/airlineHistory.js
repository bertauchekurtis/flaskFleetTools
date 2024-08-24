window.onload = function(){
    const ctx = document.getElementById('airlineChart');
    $.get("/getAirlineHistory?airline=" + $('#airlineName').text(), function(data){
        console.log("Data gotted!");
        const totals = data["totals"];
        const dates = data["dates"];
        const details = data["details"]
        const datasets = []
        datasets.push({label: 'Total Number of Aircraft', data: totals, borderWidth: 1})
        for(const  [label, data] of Object.entries(details)){
          datasets.push({label: label, data: data, borderWidth: 1})
        }

        new Chart(ctx, {
            type: 'line',
            data: {
              labels: dates,
              datasets: datasets
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

