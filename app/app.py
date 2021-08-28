# Import libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import pandas as pd
import numpy as np
import datetime as dt

# Flask Setup
app = Flask(__name__)

# Read in CSV data from URL
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
df = pd.DataFrame(pd.read_csv(url, skipinitialspace=True, parse_dates=['date']))
df[['new_cases','new_deaths']] = df.groupby(['state','county'], as_index=False)[['cases','deaths']].diff().fillna(0)

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

# Return county name and return COVID data in JSON form to API for app.js 
@app.route("/county_data" , methods=['GET', 'POST'])
def county_data():

    # Get county selection
    county = request.args.get('county')
    
    # Conditional to return USA, Texas or individual county data
    if county == 'USA':
        selected_df = df.groupby('date', as_index=False)[['cases','deaths','new_cases','new_deaths']].sum()
    elif county == 'Texas':
        selected_df = df_texas.groupby('date', as_index=False)[['cases','deaths','new_cases','new_deaths']].sum()
    else:
        selected_df = df_texas.loc[df_texas.county==county]

    # np.where to replace negative numbers with 0
    # TODO: find better solution to graph corrections
    selected_df['new_cases'] = np.where(selected_df.new_cases<0, 0, selected_df.new_cases)
    selected_df['new_deaths'] = np.where(selected_df.new_deaths<0, 0, selected_df.new_deaths)

    selected_df['rolling_cases'] = selected_df.new_cases.rolling(14).mean() 
    selected_df['rolling_death'] = selected_df.new_deaths.rolling(14).mean() 
    output_df = selected_df.dropna(how='any')
    output_df['date'] = output_df['date'].astype('str')

    output_json = {'date':output_df.date.to_list(),
                   'new_cases':output_df.new_cases.to_list(),
                   'total_cases':output_df.cases.to_list(),
                   'new_deaths':output_df.new_deaths.to_list(),
                   'total_deaths':output_df.deaths.to_list(),
                   'rolling_cases':output_df.rolling_cases.to_list(),
                   'rolling_death':output_df.rolling_death.to_list()}
        
    # Send to "/county_data"
    return jsonify(output_json)

# Run app
if __name__ == "__main__":
    app.run(debug=True)