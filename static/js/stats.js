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

// Intercambios acumulados

const displayChartAcumulados = (data, labels) => {
  console.log("Data for chart:", data);
  console.log("Labels for chart:", labels);

  var ctx_mes = document.getElementById("intercambios_totales").getContext("2d");

  var lineChart = new Chart(ctx_mes, {
      
      type: 'line',
      data: {
          labels: labels,
          datasets: [{
              label: 'Intercambios Diarios Acumulados',
              data: data,
              fill: false,
              cubicInterpolationMode: 'monotone',
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.4
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: {
                  position: 'top',
              },
              title: {
                  display: true,
                  text: 'Intercambios Diarios Acumulados'
              }
          },
          scales: {
              x: {
                  type: 'time',
                  time: {
                      unit: 'day',
                      tooltipFormat: 'MMM D, YYYY'
                  },
                  title: {
                      display: true,
                      text: 'Fecha'
                  }
              },
              y: {
                  title: {
                      display: true,
                      text: 'Total Acumulado'
                  }
              }
          }
      },
  });
};

const getIntercambiosAcumulados = () => {
  fetch("/metricas_intercambios_totales")
      .then((res) => res.json())
      .then((res1) => {
          console.log("API response:", res1);
          const results = res1.intercambios_dia_total;
          const labels = Object.keys(results);
          const data = Object.values(results);

          displayChartAcumulados(data, labels);
      })
      .catch((error) => {
          console.error("Error fetching data:", error);
      });
};

window.onload = getIntercambiosAcumulados;


// tabla

let dataTable;
let dataTableInitialized = false;

const dataTableOptions =  {
  columnDefs : [
    {className : "centered", targets : [0, 1, 2, 3]}
  ]
};

const initDatatable = async ()=>{
  if (dataTableInitialized){
    dataTable.destroy();
  }
  await listIntercambios();
  dataTable = $("#datatable_estadisticas").DataTable(dataTableOptions);
  dataTableInitialized = true;
};

const listIntercambios = async()=>{
  try{
    const response = await fetch("/metricas_mostrar_tabla");
    const data = await response.json();
    let content = ``;
    data.intercambios.forEach((intercambio, index)=>{
      content+=`
        <tr>
          <td>${intercambio.punto_encuentro}</td>
          <td>${intercambio.year_month}</td>
          <td>${intercambio.estado}</td>
          <td>${intercambio.total}</td>
        </tr>
      `;
    });
    tabla_intercambios.innerHTML = content;
  }catch(ex){
    alert(ex);
  }

};

window.addEventListener('load', async()=>{
  await initDatatable();
});