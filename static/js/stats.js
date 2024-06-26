const displayChart = (data, labels, puntoEncuentros) => {
    const colors = [
        'rgba(255, 99, 132)', 'rgba(54, 162, 235)', 'rgba(255, 206, 86)',
        'rgba(75, 192, 192)', 'rgba(153, 102, 255)', 'rgba(255, 159, 64)',
        'rgba(199, 199, 199)', 'rgba(83, 102, 255)', 'rgba(66, 133, 244)',
        'rgba(219, 68, 55)', 'rgba(244, 180, 0)', 'rgba(15, 157, 88)',
        'rgba(255, 87, 34)', 'rgba(121, 85, 72)', 'rgba(233, 30, 99)',
        'rgba(103, 58, 183)', 'rgba(0, 150, 136)', 'rgba(3, 169, 244)',
        'rgba(255, 235, 59)', 'rgba(96, 125, 139)'
    ];

    const borderColors = colors.map(color => color.replace('0.2', '1'));

    var ctx_mes = document.getElementById("intercambios_mes").getContext("2d");
    var datasets = puntoEncuentros.map((puntoEncuentro, index) => ({
        label: puntoEncuentro,
        data: labels.map(label => data[label][puntoEncuentro] || 0),
        backgroundColor: colors[index % colors.length],
        borderColor: borderColors[index % borderColors.length],
        borderWidth: 1
    }));

    var barchart_mes = new Chart(ctx_mes, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            scales: {
                x: {
                    stacked: true
                },
                y: {
                    stacked: true
                }
            }
        }
    });
}

const getIntercambiosMes = () => {
    fetch("/metricas_intercambios_mes")
      .then((res) => res.json())
      .then((res1) => {
        const results = res1.intercambios_mes;
        const labels = Object.keys(results);
        const puntoEncuentros = [...new Set(Object.values(results).flatMap(item => Object.keys(item)))];
        const data = results;
        
        console.log("results", results);
        displayChart(data, labels, puntoEncuentros);
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

