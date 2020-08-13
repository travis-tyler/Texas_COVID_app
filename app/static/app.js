// d3.csv("static/COVID-19 Activity.csv", function(d) {
//     return {
//     //   date: new Date(+d.REPORT_DATE), 
//       county_no: +d.COUNTY_FIPS_NUMBER,
//       new_cases: +d.PEOPLE_POSITIVE_CASES_COUNT,
//       total_cases: +d.PEOPLE_POSITIVE_NEW_CASES_COUNT,
//       new_death: +d.PEOPLE_DEATH_NEW_COUNT, 
//       total_death: +d.PEOPLE_DEATH_COUNT
//     };
//   }, function(error, rows) {
//     console.log(rows);
//   });

// (async function(){
//     var covidData = await d3.json("static/travis_co.json").catch(function(error) {
//       console.log(error);
//     });
//     console.log(covidData);


// })()



function buildPlot(county) {

  console.log(county)


  /* data route */
  const url = `/county_data?county=${county}`;
  d3.json(url).then(function(response) {


      // Trace for new case data
      let traceNewCases = {
          x: response.date,
          y: response.new_cases,
          type:"bar",
          name:"New cases"
      };

      // Trace for total cases data
      let traceAllCases = {
          x: response.date,
          y: response.total_cases,
          yaxis: 'y2',
          type: "line",
          name: "Total cases"
      };

      let dataCases = [traceNewCases, traceAllCases];

      // Layout for duel-axis graph
      let layoutCases = {
          title: "Cumulative Cases (log) and New Daily Cases (linear)",
          height: 700,
          width: 1200,
          xaxis: {
              title: "Date"
            },
            yaxis: {
              title: "New cases",
            },
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(0,0,0,0)',
          yaxis2: {
            title: 'Total cases (log)',
            overlaying: 'y',
            side: 'right',
            type: 'log',
          },
          font: {
              color: "white"
          }        
      };

      Plotly.newPlot("casePlot", dataCases, layoutCases);

      // Trace for new case data
      let traceNewDealths = {
        x: response.date,
        y: response.new_deaths,
        type:"bar",
        name:"New deaths"
      };

      // Trace for total cases data
      let traceAllDeaths = {
          x: response.date,
          y: response.total_deaths,
          yaxis: 'y2',
          type: "line",
          name: "Total deaths"
      };

      let dataDeaths = [traceNewDealths, traceAllDeaths];

      // Layout for duel-axis graph
      let layoutDeaths = {
          title: "Cumulative deaths (log) and New Daily Deaths (linear)",
          height: 700,
          width: 1200,
          xaxis: {
              title: "Date"
            },
            yaxis: {
              title: "New deaths",
            },
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(0,0,0,0)',
          yaxis2: {
            title: 'Total deaths (log)',
            overlaying: 'y',
            side: 'right',
            type: 'log',
          },
          font: {
              color: "white"
          }        
      };

      Plotly.newPlot("deathPlot", dataDeaths, layoutDeaths);

  });
}

// Select dropdown menu using D3
var selectDrop = d3.select("#selDataset");


// Create event handler
selectDrop.on("change",runEnter);
// Event handler function
function runEnter() {
  // Prevent the page from refreshing
  d3.event.preventDefault();
  // Select the input element and get HTML node
  var inputElement = d3.select("select");
  // Get the value property of the input element
  var userCounty = inputElement.property("value");

  buildPlot(userCounty);
};






