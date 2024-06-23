

const displayChart = (data, labels) => {
    var ctx_mes = document.getElementById("intercambios_mes").getContext("2d");
    var barchart_mes = new Chart(ctx_mes,  {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
            label: 'Intercambios Por Mes',
            data: data,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(153, 102, 255)',
                'rgb(201, 203, 207)'
            ],
            borderWidth: 1
            }]
        },
        options: {
        scales: {
            y: {
            beginAtZero: true
            }
         }
        },
    }
    )
}

const getIntercambiosMes = () => {
    fetch("/metricas_intercambios_mes")
      .then((res) => res.json())
      .then((res1) => {
        const results = res1.intercambios_mes;
        const [labels, data] = [Object.keys(results), Object.values(results)];
        console.log("results", results);
        displayChart(data, labels);
      });
  };
  
document.onload = getIntercambiosMes();



// Intercambios por estado

const displayChart2 = (data, labels) => {
    var ctx_estado = document.getElementById("piechart_intercambios_estado").getContext("2d");
    var donut_estado = new Chart(ctx_estado,  {
    
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                label: 'Intercambios por Estado',
                 data: data,
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 205, 86)',
                    'rgb(255, 50, 86)',
                    'rgb(100, 205, 86)',
                    'rgb(255, 20, 10)'
                ],
                hoverOffset: 4
                }]
            }
         }
    
    )
}

const getIntercambiosEstado = () => {
    fetch("/metricas_intercambios_estado")
      .then((res) => res.json())
      .then((res1) => {
        const results = res1.intercambios_estado
        const [labels, data] = [Object.keys(results), Object.values(results)];
        console.log("results", results);
        displayChart2(data, labels);
      });
  };

document.onload = getIntercambiosEstado();

// Intercambios filial


var ctx_filial = document.getElementById("intercambios_filial").getContext("2d");
var barchart_mes = new Chart(ctx_filial,  {
    type: 'bar',
    data: {
        labels: ["Filial 1", "Filial 2", "Filial 3"],
        datasets: [
          {
            label: 'Categoria 1',
            data: [10, 30, 20],
            backgroundColor: 'rgb(255, 99, 132)',
          },
          {
            label: 'Categoria 1',
            data: [30, 10, 60],
            backgroundColor: 'rgb(54, 162, 235)',
          },
          {
            label: 'Categoria 1',
            data: [50, 10, 10],
            backgroundColor: 'rgb(255, 205, 86)',
          },
        ]
      },
    options: {
      plugins: {
        title: {
          display: true,
          text: 'Intercambios por Filiales y categoria'
        },
      },
      responsive: true,
      scales: {
        x: {
          stacked: true,
        },
        y: {
          stacked: true
        }
      }
    }
  }
)

