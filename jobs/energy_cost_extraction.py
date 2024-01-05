import sys
sys.path.append(".") # Adds higher directory to python modules path.

import pathlib
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
from numpy import ceil
from extractor.jobs.electricity_costs import cost_extract, costs_transform
from extractor.load.load_sqlite import df_sqlite_load

def populate_intensity():
    pass


def update_cost(db_path):
    conn = sqlite3.connect(db_path)

    # Update sources
    current_datetime = datetime.now()
    min_datetime = datetime(2018,1,1) 
    
    # Update sources Costs
    max_timestamp_df = pd.read_sql_query("""
        SELECT max(unixTimestamp) as max_timestamp 
        FROM 'sources.costs' 
        WHERE dnoRegion=21;
        """, conn)
    
    max_days_range = 14

    if max_timestamp_df['max_timestamp'][0] is None:
        # No data -> Update from the beggining
        print("... Cost table is empty ")
        update_from =  min_datetime
    else:
        # Some data is present
        max_datetime = datetime.fromtimestamp(max_timestamp_df['max_timestamp'][0] )
        update_from = max(max_datetime,min_datetime)
        print(f"... Cost table last record: {update_from}")
    
    
    diff= current_datetime-update_from
    print(f"...... Days to update: {(current_datetime-update_from).days}")
    
    dt = timedelta(days=max_days_range)
    load_config = {"db_path":db_path,"target_table":"sources.costs"}
    while (current_datetime-update_from).days>0:
        print(f"...... Estimated queries for update: {ceil((current_datetime-update_from).days / max_days_range)}")
        to_date = min(update_from+dt,current_datetime)
        job = {
            'dno':21,
            'voltage':'HV',
            'start':update_from.strftime("%d-%m-%Y"),
            'end':to_date.strftime("%d-%m-%Y"),
            }
        raw_data = cost_extract(job)
        df = costs_transform(raw_data)
        df_sqlite_load(df,load_config)
        update_from = to_date
    

if __name__=="__main__":
    
    # Welcome
    app_dir = pathlib.Path(__file__).parent.parent.resolve()
    print("Welcome to the Grid App, currently located in:", app_dir)
    
    # Database verification
    print("Connecting to local database...")
    db_path = app_dir.joinpath('db','database.db') 
    conn = sqlite3.connect(db_path)


    # Update sources
    update_cost(db_path)
