import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    The function processes the song data JSON files and loads the data into the songs and artists tables.
    """
    
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = list(df[["song_id","title","artist_id","year","duration"]].values[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(df[["artist_id","artist_name","artist_location","artist_latitude","artist_longitude"]].values[0])
    cur.execute(artist_table_insert, artist_data)

def extract_time_data(d):
    """ 
    The function extracts the hour, year, month, week of the year, day, day of the week from the timestamp data and return the required data in the form of a list.
    """
    hour = d.hour
    year = d.year
    month = d.month
    week_of_year = d.weekofyear
    day = d.day
    weekday = d.dayofweek
    timestamp = pd.Timestamp(d)
    
    return [timestamp, hour, day, week_of_year, month, year, weekday]
    
def process_log_file(cur, filepath):
    """
    The function processes the log data JSON files and loads the relevant data into the following tables : songplays, users and time.
    """
    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df = df[df["page"]=="NextSong"]

    # convert timestamp column to datetime
    t = pd.DataFrame()
    t["ts"] = pd.to_datetime(df["ts"])
    t["time_data"] = t.apply(lambda row : extract_time_data(row["ts"]),axis =1)
    
    # insert time data records
    time_data = list(t["time_data"].values)
    column_labels = ["start_time","hour","day","week","month","year","weekday"]
    time_df = pd.DataFrame(time_data, columns = column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId","firstName","lastName","gender","level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [pd.Timestamp(row.ts),row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    The function lists out the JSON files and passes the files to the respective functions. 
    The data from the JSON files will be processed and the relevant data will be loaded into the database tables.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()