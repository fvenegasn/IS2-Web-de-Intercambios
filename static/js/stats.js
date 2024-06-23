
var ctx_mes = document.getElementById("intercambios_mes").getContext("2d");
var barchart_mes = new Chart(ctx_mes,  {
    type: 'bar',
    data: {
        labels: [1, 2, 3, 4, 5, 6, 7],
        datasets: [{
          label: 'Intercambios Por Mes',
          data: [65, 59, 80, 81, 56, 55, 40],
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




// Intercambios por estado
var ctx_estado = document.getElementById("piechart_intercambios_estado").getContext("2d");
var donut_estado = new Chart(ctx_estado,  {
    
        type: 'doughnut',
        data: {
            labels: [
              'Finalizado',
              'Cancelado',
              'Pendiente'
            ],
            datasets: [{
              label: 'Intercambios por Estado',
              data: [300, 50, 100],
              backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
              ],
              hoverOffset: 4
            }]
          }
      }
    
)


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

