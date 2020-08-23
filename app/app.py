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

# Create new 'county_state' column for easier selection
df['county_state'] = df['COUNTY_NAME'] + ', ' + df['PROVINCE_STATE_NAME']

# Remove uncessary columns and rename others
df = df[['county_state',
        'PROVINCE_STATE_NAME',
        'COUNTY_NAME',
        'REPORT_DATE',
        'PEOPLE_POSITIVE_NEW_CASES_COUNT',
        'PEOPLE_POSITIVE_CASES_COUNT',
        'PEOPLE_DEATH_NEW_COUNT',
        'PEOPLE_DEATH_COUNT']]
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
county_list = df_texas['county_state'].unique().tolist()
county_list = sorted(county_list)
county_list.insert(0,'Texas - Sum')
county_list.insert(0,'USA - Sum')

##########################################################

# create route that renders index.html template
@app.route("/")
def home():
    return render_template('index.html', all_counties=county_list)

# Route to take a county name and return COVID data in JSON form for app.js
@app.route("/county_data" , methods=['GET', 'POST'])
def county_data():

    county = request.args.get('county')
    
    # Returns total USA numbers
    if county == 'USA - Sum':
        total_usa = df.sort_values('date')
        total_usa = total_usa.groupby('date')[['new_cases','total_cases','new_deaths','total_deaths']].sum()
        total_usa['rolling_cases'] = total_usa.new_cases.rolling(14).mean() 
        total_usa['rolling_death'] = total_usa.new_deaths.rolling(14).mean() 
        total_usa = total_usa.dropna(how='any')
        output_json = {'date':total_usa.index.to_list(),
                       'new_cases':total_usa.new_cases.to_list(),
                       'total_cases':total_usa.total_cases.to_list(),
                       'new_deaths':total_usa.new_deaths.to_list(),
                       'total_deaths':total_usa.total_deaths.to_list(),
                       'rolling_cases':total_usa.rolling_cases.to_list(),
                       'rolling_death':total_usa.rolling_death.to_list()
        }

    elif county == 'Texas - Sum':
        total_texas = df_texas.sort_values('date')
        total_texas = total_texas.groupby('date')[['new_cases','total_cases','new_deaths','total_deaths']].sum()
        total_texas['rolling_cases'] = total_texas.new_cases.rolling(14).mean() 
        total_texas['rolling_death'] = total_texas.new_deaths.rolling(14).mean() 
        total_texas = total_texas.dropna(how='any')
        output_json = {'date':total_texas.index.to_list(),
                       'new_cases':total_texas.new_cases.to_list(),
                       'total_cases':total_texas.total_cases.to_list(),
                       'new_deaths':total_texas.new_deaths.to_list(),
                       'total_deaths':total_texas.total_deaths.to_list(),
                       'rolling_cases':total_texas.rolling_cases.to_list(),
                       'rolling_death':total_texas.rolling_death.to_list()
        }

        
    # Returns individual county numbers
    else:
        county_df = df_texas.loc[df_texas.county_state==county]
        county_df = county_df.sort_values('date')
        county_df['rolling_cases'] = county_df.new_cases.rolling(14).mean() 
        county_df['rolling_death'] = county_df.new_deaths.rolling(14).mean() 
        county_df = county_df.dropna(how='any')
        output_json = {'date':county_df.date.to_list(),
                       'new_cases':county_df.new_cases.to_list(),
                       'total_cases':county_df.total_cases.to_list(),
                       'new_deaths':county_df.new_deaths.to_list(),
                       'total_deaths':county_df.total_deaths.to_list(),
                       'rolling_cases':county_df.rolling_cases.to_list(),
                       'rolling_death':county_df.rolling_death.to_list()
        }
        
    # Send to "/county_data"
    return jsonify(output_json)

# Run app
if __name__ == "__main__":
    app.run(debug=True)