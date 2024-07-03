/*
const displayChart = (data, labels, puntoEncuentros) => {
  const colors = [
    'rgba(255, 99, 71, 0.9)', 'rgba(75, 0, 130, 0.9)', 'rgba(173, 255, 47, 0.9)',
    'rgba(0, 255, 255, 0.9)', 'rgba(255, 20, 147, 0.9)', 'rgba(128, 0, 128, 0.9)',
    'rgba(255, 165, 0, 0.9)', 'rgba(0, 100, 0, 0.9)', 'rgba(30, 144, 255, 0.9)',
    'rgba(210, 105, 30, 0.9)', 'rgba(106, 90, 205, 0.9)', 'rgba(139, 0, 0, 0.9)',
    'rgba(255, 215, 0, 0.9)', 'rgba(47, 79, 79, 0.9)', 'rgba(240, 128, 128, 0.9)',
    'rgba(46, 139, 87, 0.9)', 'rgba(0, 128, 128, 0.9)', 'rgba(218, 112, 214, 0.9)',
    'rgba(139, 69, 19, 0.9)', 'rgba(255, 99, 132, 0.9)'
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

      displayChart(data, labels, puntoEncuentros);
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
};

// Intercambios por estado
const displayChart2 = (data, labels) => {
  var ctx_estado = document.getElementById("piechart_intercambios_estado").getContext("2d");
  var donut_estado = new Chart(ctx_estado, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        label: 'Intercambios por Estado',
        data: data,
        backgroundColor: [
          'rgba(255, 99, 71, 0.9)', 'rgba(75, 0, 130, 0.9)', 'rgba(173, 255, 47, 0.9)',
          'rgba(0, 255, 255, 0.9)', 'rgba(255, 20, 147, 0.9)', 'rgba(128, 0, 128, 0.9)',
          'rgba(255, 165, 0, 0.9)', 'rgba(0, 100, 0, 0.9)', 'rgba(30, 144, 255, 0.9)',
          'rgba(210, 105, 30, 0.9)', 'rgba(106, 90, 205, 0.9)', 'rgba(139, 0, 0, 0.9)',
          'rgba(255, 215, 0, 0.9)', 'rgba(47, 79, 79, 0.9)', 'rgba(240, 128, 128, 0.9)',
          'rgba(46, 139, 87, 0.9)', 'rgba(0, 128, 128, 0.9)', 'rgba(218, 112, 214, 0.9)',
          'rgba(139, 69, 19, 0.9)', 'rgba(255, 99, 132, 0.9)'
      ],
        hoverOffset: 4
      }]
    }
  });
}

const getIntercambiosEstado = () => {
  fetch("/metricas_intercambios_estado")
    .then((res) => res.json())
    .then((res1) => {
      const results = res1.intercambios_estado;
      const [labels, data] = [Object.keys(results), Object.values(results)];
      displayChart2(data, labels);
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
};

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
      const results = res1.intercambios_dia_total;
      const labels = Object.keys(results);
      const data = Object.values(results);
      displayChartAcumulados(data, labels);
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
};


// Function to display the bar chart
const displayIntercambiosCategoria = (data) => {
  const labels = Object.keys(data);
  const values = Object.values(data);

  const colors = [
    'rgba(255, 99, 71, 0.9)', 'rgba(75, 0, 130, 0.9)', 'rgba(173, 255, 47, 0.9)',
    'rgba(0, 255, 255, 0.9)', 'rgba(255, 20, 147, 0.9)', 'rgba(128, 0, 128, 0.9)',
    'rgba(255, 165, 0, 0.9)', 'rgba(0, 100, 0, 0.9)', 'rgba(30, 144, 255, 0.9)',
    'rgba(210, 105, 30, 0.9)', 'rgba(106, 90, 205, 0.9)', 'rgba(139, 0, 0, 0.9)',
    'rgba(255, 215, 0, 0.9)', 'rgba(47, 79, 79, 0.9)', 'rgba(240, 128, 128, 0.9)',
    'rgba(46, 139, 87, 0.9)', 'rgba(0, 128, 128, 0.9)', 'rgba(218, 112, 214, 0.9)',
    'rgba(139, 69, 19, 0.9)', 'rgba(255, 99, 132, 0.9)'
];

  const borderColors = colors.map(color => color.replace('0.2', '1'));

  var ctx = document.getElementById("intercambios_categoria").getContext("2d");
  var chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: '#',
        data: values,
        backgroundColor: colors,
        borderColor: borderColors,
        borderWidth: 2,
        borderRadius: 5,
        borderSkipped: false,
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
};

const getIntercambiosCategorias = () => {
  fetch("/metricas_intercambios_categoria")
    .then((res) => res.json())
    .then((data) => {
      displayIntercambiosCategoria(data.intercambios_categoria);
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
};

// Initialize DataTable
let dataTable;
let dataTableInitialized = false;

const dataTableOptions = {
  columnDefs: [
    { className: "centered", targets: [0, 1, 2, 3, 4] }
  ]
};

const initDatatable = async () => {
  if (dataTableInitialized) {
    dataTable.destroy();
  }
  await listIntercambios();
  dataTable = $("#datatable_estadisticas").DataTable(dataTableOptions);
  dataTableInitialized = true;
};

const listIntercambios = async () => {
  try {
    const response = await fetch("/metricas_mostrar_tabla");
    const data = await response.json();
    let content = ``;
    data.intercambios.forEach((intercambio, index) => {
      content += `
        <tr>
          <td>${intercambio.punto_encuentro}</td>
          <td>${intercambio.year_month}</td>
          <td>${intercambio.estado}</td>
          <td>${intercambio.publicacion_ofertante__categoria}</td>
          <td>${intercambio.total}</td>
        </tr>
      `;
    });
    tabla_intercambios.innerHTML = content;
  } catch (ex) {
    alert(ex);
  }
};


// Consolidate all onload functions
window.onload = () => {
  getIntercambiosMes();
  getIntercambiosEstado();
  getIntercambiosAcumulados();
  getIntercambiosCategorias();
  initDatatable();
};
*/
document.addEventListener('DOMContentLoaded', function() {
  fetchInitialData(); // Fetch initial data when the page loads
});

function fetchInitialData() {
  fetchChartData(); // Fetch chart data when the page loads
  fetchTableData(); // Fetch table data when the page loads
}

// Function to destroy existing charts
let charts = {
  intercambios_categoria: null,
  intercambios_mes: null,
  piechart_intercambios_estado: null,
  intercambios_totales: null
};

function getRandomColors(count) {
  // Generate random colors in hexadecimal format
  let colors = [];
  for (let i = 0; i < count; i++) {
    let color = '#' + Math.floor(Math.random() * 16777215).toString(16);
    colors.push(color);
  }
  return colors;
}

function fetchChartData() {
  let startDate = document.getElementById('start_date').value;
  let endDate = document.getElementById('end_date').value;

  fetch(`/metricas_intercambios_mes?start_date=${startDate}&end_date=${endDate}`)
      .then(response => response.json())
      .then(data => {
          console.log("Intercambios Mes Data:", data);
          // Crear gráfico de total por filial
          createBarChart('intercambios_mes', data.intercambios_mes);
      });
  
  fetch(`/metricas_intercambios_estado?start_date=${startDate}&end_date=${endDate}`)
      .then(response => response.json())
      .then(data => {
          console.log("Intercambios Estado Data:", data);
          destroyChart(charts.piechart_intercambios_estado);
          let ctx = document.getElementById('piechart_intercambios_estado').getContext('2d');
          let chartData = formatPieData(data.intercambios_estado);
          charts.piechart_intercambios_estado = new Chart(ctx, {
              type: 'pie',
              data: chartData,
              options: {}
          });
      });

  fetch(`/metricas_intercambios_totales?start_date=${startDate}&end_date=${endDate}`)
      .then(response => response.json())
      .then(data => {
          console.log("Intercambios Totales Data:", data);
          destroyChart(charts.intercambios_totales);
          let ctx = document.getElementById('intercambios_totales').getContext('2d');
          let chartData = formatLineData(data.intercambios_dia_total);
          charts.intercambios_totales = new Chart(ctx, {
              type: 'line',
              data: chartData,
              options: {}
          });
      });

  fetch(`/metricas_intercambios_categoria?start_date=${startDate}&end_date=${endDate}`)
      .then(response => response.json())
      .then(data => {
          console.log("Intercambios Categoria Data:", data);
          // Crear gráfico de total por categoría
          createBarChart('intercambios_categoria', data.intercambios_categoria);
      });
}

function createBarChart(chartName, data) {
  let canvas = document.getElementById(chartName);
  
  if (!canvas) {
    console.error(`Element with ID '${chartName}' not found.`);
    return;
  }

  let ctx = canvas.getContext('2d');

  if (charts[chartName]) {
    charts[chartName].destroy(); // Destruir el gráfico existente si existe
  }

  charts[chartName] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(data),
      datasets: [{
        label: `Total por ${chartName.replace('_', ' ')}`,
        data: Object.values(data),
        backgroundColor: getRandomColors(Object.keys(data).length)
      }]
    },
    options: {}
  });
}

function fetchTableData() {
  let startDate = document.getElementById('start_date').value;
  let endDate = document.getElementById('end_date').value;

  fetch(`/metricas_mostrar_tabla?start_date=${startDate}&end_date=${endDate}`)
      .then(response => response.json())
      .then(data => {
          console.log("Table Data:", data);
          updateTable(data);
      });
}

function updateTable(data) {
  let table = $('#datatable_estadisticas').DataTable();
  table.clear().draw(); // Limpiar y dibujar la tabla nuevamente

  if (Array.isArray(data)) {
      // Si data es un array, asumimos que son los datos directos de la tabla
      data.forEach(row => {
          table.row.add([
              row.filial,
              row.year_month,
              row.estado,
              row.publicacion_ofertante__categoria,
              row.total,
              row.donaciones  // Agregar la nueva columna de donaciones
          ]).draw(false); // Agregar fila y dibujarla
      });
  } else if (data && data.intercambios) {
      // Si data tiene la propiedad 'intercambios', asumimos que es el objeto completo
      data.intercambios.forEach(row => {
          table.row.add([
              row.filial__nombre,
              row.year_month,
              row.estado,
              row.publicacion_ofertante__categoria,
              row.total,
              row.donaciones  // Agregar la nueva columna de donaciones
          ]).draw(false); // Agregar fila y dibujarla
      });
  } else {
      console.error("Formato de datos no reconocido:", data);
  }
}

function formatPieData(data) {
  let labels = Object.keys(data);
  let values = Object.values(data);
  let colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'];

  return {
      labels: labels,
      datasets: [{
          data: values,
          backgroundColor: colors
      }]
  };
}

function formatLineData(data) {
  let labels = Object.keys(data);
  let values = Object.values(data);

  return {
      labels: labels,
      datasets: [{
          label: 'Intercambios diarios acumulados',
          data: values,
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
      }]
  };
}
function destroyChart(chart) {
  if (chart) {
      chart.destroy();
  }
}