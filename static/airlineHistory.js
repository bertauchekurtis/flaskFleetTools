window.onload = function(){
    const windowWidth = $(window).width();
    let divOne = document.getElementById("airlineChartDiv");
    let divTwo = document.getElementById("rawChartDiv");
    setSize(divOne, windowWidth);
    setSize(divTwo, windowWidth);

    function setSize(element, windowWidth){
      element.style.width = String(windowWidth * 0.75) + "px";
      element.style.height = String(windowWidth * 0.4) + "px";
    }
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
    const mtx = document.getElementById('rawChart');
    $.get("/getAirlineHistoryRawCap?airline=" + $('#airlineName').text(), function(data){
        console.log("Data gotted!");
        //const totals = data["totals"];
        const dates = data["dates"];
        const caps = data["caps"]
        const datasets = []
        datasets.push({label: 'Total Raw Capacity', data: caps, borderWidth: 1})

        new Chart(mtx, {
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

