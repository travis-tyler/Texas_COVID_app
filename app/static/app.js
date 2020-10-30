function buildPlot(county) {

  /* data route */
  const url = `/county_data?county=${county}`;
  d3.json(url).then(function(response) {

      // Trace for new case data
      let traceNewCases = {
          x: response.date,
          y: response.new_cases,
          type: 'bar',
          bar:{
            color: 'orange'
          },
          name: 'New cases'
      };

      // Trace for rolling case data
      let traceRollingCases = {
        x: response.date,
        y: response.rolling_cases,
        type: 'line',
        line:{
          color: 'lightblue',
          dash: 'dot'
        },
        name: '14-day rolling avg.'
      };

      // Trace for total cases data
      let traceAllCases = {
          x: response.date,
          y: response.total_cases,
          yaxis: 'y2',
          type: "line",
          line:{
            color: 'orange'
          },
          name: "Total cases"
      };

      let dataCases = [traceNewCases, traceRollingCases, traceAllCases];

      // Layout for duel-axis graph
      let layoutCases = {
          title: `${county} County Cumulative Cases (log) and New Daily Cases (linear)`,
          height: 700,
          width: 1200,
          xaxis: {
            title: 'Date'
          },
          yaxis: {
            title: 'New cases'
          },
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(0,0,0,0)',
          yaxis2: {
            title: 'Total cases (log)',
            overlaying: 'y',
            side: 'right',
            type: 'log',
            autorange: true,
            dtick: 1          
          },
          font: {
              color: "white"
          }        
      };

      let config = {responsive: true}

      Plotly.newPlot('casePlot', dataCases, layoutCases, config);

      // Trace for new death data
      let traceNewDealths = {
        x: response.date,
        y: response.new_deaths,
        type:'bar',
        name:'New deaths'
      };

      // Trace for rolling death data
      let traceRollingDeath = {
        x: response.date,
        y: response.rolling_death,
        type:'line',
        line:{
          color:'lightblue',
          dash: 'dot'
        },
        name:'14-day rolling avg.'
      };

      // Trace for total death data
      let traceAllDeaths = {
          x: response.date,
          y: response.total_deaths,
          yaxis: 'y2',
          type: 'line',
          line:{
            color:'orange'
          },
          name: 'Total deaths'
      };

      let dataDeaths = [traceNewDealths, traceRollingDeath, traceAllDeaths];

      // Layout for duel-axis graph
      let layoutDeaths = {
          title: `${county} Cumulative deaths (log) and New Daily Deaths (linear)`,
          height: 700,
          width: 1200,
          xaxis: {
              title: 'Date'
          },
          yaxis: {
            title: 'New deaths',
          },
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(0,0,0,0)',
          yaxis2: {
            title: 'Total deaths (log)',
            overlaying: 'y',
            side: 'right',
            type: 'log',
            autorange: true,
            dtick: 1          
          },
          font: {
              color: 'white'
          }        
      };

      Plotly.newPlot('deathPlot', dataDeaths, layoutDeaths, config);

  });
}

// Select dropdown menu using D3
var selectDrop = d3.select('#selDataset');

// Display default selected data (Travis County) on page load
d3.select(window).on('load', runEnter());

// Create event handler
selectDrop.on('change',runEnter);

// Event handler function
function runEnter() {
  // Select the input element and get HTML node
  var inputElement = d3.select('select');
  // Get the value property of the input element
  var userCounty = inputElement.property('value');

  buildPlot(userCounty);
};