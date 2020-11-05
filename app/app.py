# Import libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import pandas as pd

# Flask Setup
app = Flask(__name__)

# Read in CSV data from URL
url = 'https://query.data.world/s/o6que7zbpjnykcz3ayncuhwkgsb3dp'
df = pd.DataFrame(pd.read_csv(url))
df = df.loc[df.COUNTRY_ALPHA_3_CODE=='USA']
df = df.dropna(how='all')

# Remove unnecessary columns and rename others
df = df.rename(columns={'REPORT_DATE':'date',
                        'PROVINCE_STATE_NAME':'state',
                        'COUNTY_NAME':'county',
                        'PEOPLE_POSITIVE_NEW_CASES_COUNT':'new_cases',
                        'PEOPLE_POSITIVE_CASES_COUNT':'total_cases',
                        'PEOPLE_DEATH_NEW_COUNT':'new_deaths',
                        'PEOPLE_DEATH_COUNT':'total_deaths'})

# Select Texas data and remove latest date
df_texas = df.loc[df.state == 'Texas']

# Create list of counties for dropdown menu
county_list = df_texas['county'].unique().tolist()
county_list = ['USA', 'Texas'] + sorted(county_list)

##########################################################

# create route that renders index.html template
@app.route("/")
def home():
    return render_template('index.html', all_counties=county_list)

# Return county name and return COVID data in JSON form for app.js to API
@app.route("/county_data" , methods=['GET', 'POST'])
def county_data():

    # Get county selection
    county = request.args.get('county')
    
    # Conditional to return USA, Texas or individual county data
    if county == 'USA':
        selected_df = df.sort_values('date')
    elif county == 'Texas':
        selected_df = df_texas.sort_values('date') 
    else:
        selected_df = df_texas.loc[df_texas.county==county].sort_values('date')

    selected_df = selected_df.groupby('date')[['new_cases','total_cases','new_deaths','total_deaths']].sum()
    selected_df['rolling_cases'] = selected_df.new_cases.rolling(14).mean() 
    selected_df['rolling_death'] = selected_df.new_deaths.rolling(14).mean() 
    output_df = selected_df.dropna(how='any')

    output_json = {'date':output_df.index.to_list(),
                   'new_cases':output_df.new_cases.to_list(),
                   'total_cases':output_df.total_cases.to_list(),
                   'new_deaths':output_df.new_deaths.to_list(),
                   'total_deaths':output_df.total_deaths.to_list(),
                   'rolling_cases':output_df.rolling_cases.to_list(),
                   'rolling_death':output_df.rolling_death.to_list()
    }
        
    # Send to "/county_data"
    return jsonify(output_json)

# Run app
if __name__ == "__main__":
    app.run(debug=True)