import pandas as pd
import datetime as dt
from pyproj import Proj, transform


def concat_data_frames(q1, q2, q3, q4):
    frames = [q1, q2, q3, q4]
    df = pd.concat(frames)

    return df


def clean_cols(df):
    items_to_drop = ['CAD Num', 'Inc Type Desc', 'Shift', 'Address', 'Apt',
                'City', 'Zip', 'BC District', 'Fire District',
                'Medic First Due', 'Notify Date', 'Arrival Date',
                'Clear Date', 'Action Taken', 'Property Loss',
                'Property Value', 'Mutual Aid', 'Cause of Ignition',
                'Fire Spread', 'Injury/Fatality', 'Geo Status',
                'How Geocoded', 'Incident Date', 'Total Resource Time',
                'Record ID']

    for col in items_to_drop:
        df.drop(col, axis=1, inplace=True)

    df.columns = df.columns.str.replace(' ', '_')
    df.columns = map(str.lower, df.columns)
    df.rename(columns={'inc_type_desc.1': 'incident_type'}, inplace=True)

    return df


def to_time(df):
    df['date_time'] = pd.to_datetime(df['911_date'])
    df['hour'] = df['date_time'].dt.hour
    df['day'] = df['date_time'].dt.dayofweek

    return df


def clean_xy_cords(df):
    inProj = Proj(init='epsg:3857')
    outProj = Proj(init='epsg:4326')
    x, y = transform(inProj, outProj, df['x'].to_numpy(), df['y'].to_numpy())
    df['x_trans'] = y
    df['y_trans'] = x

    return df


def save(df):
    df.to_csv('smfr_2019.csv')


if __name__ == '__main__':
    q1 = pd.read_csv('data/jan-mar 2019 csv.csv')
    q2 = pd.read_csv('data/apr-jun15 2019 csv.csv')
    q3 = pd.read_csv('data/jun16-aug21 2019 csv.csv')
    q4 = pd.read_csv('data/23nov-31dec 2019.csv')

    df = concat_data_frames(q1, q2, q3, q4)
    df = clean_cols(df)
    df = to_time(df)
    df = clean_xy_cords(df)
    save(df)

