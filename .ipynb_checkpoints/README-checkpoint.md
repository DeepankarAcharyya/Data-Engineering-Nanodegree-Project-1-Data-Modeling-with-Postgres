# Project : Data Modeling with Postgres

## Introduction :
>Sparkify, a startup wants to analyze their user activities based on the data collected by them via their new music streaming app. The collected data is present across several JSON files which makes it inconvinient to make queries and analyze the data. The analytics team of the startup is particularly interested in understanding the trends, what songs users are listening to.

### Project Description :
>The project aims at creating a ETL pipeline, which will create a Postgres database with tables, load the data from the JSON files into the database tables, making it easier to query and analyze the data. The whole pipeline is implemented using Python and SQL.  

&nbsp;
## Datasets :
***
Sparkify's music streaming app collect data for song and user activities in JSON files, located in the following two directories :
- "data/log_data"
- "data/song_data"

&nbsp;
The format of the JSON files are as follows :
- Song Data 
>{

>"num_songs": 1,

>"artist_id": "ARJIE2Y1187B994AB7",

>"artist_latitude": null,

>"artist_longitude": null,

>"artist_location": "",

>"artist_name": "Line Renaud",

>"song_id": "SOUPIRU12A6D4FA1E1",

>"title": "Der Kleine Dompfaff",

>"duration": 152.92036,

>"year": 0

>}

&nbsp;
- Log Data
>{

>"artist":"Des'ree",

>"auth":"Logged In",

>"firstName":"Kaylee",

>"gender":"F",

>"itemInSession":1,

>"lastName":"Summers",

>"length":246.30812,

>"level":"free",

>"location":"Phoenix-Mesa-Scottsdale, AZ",

>"method":"PUT",

>"page":"NextSong",

>"registration":1540344794796.0,

>"sessionId":139,

>"song":"You Gotta Be",

>"status":200,

>"ts":1541106106796,

>"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/35.0.1916.153 Safari\/537.36\"",

>"userId":"8"

>}

&nbsp;
&nbsp;
The JSON files are read using function (read_json()) from the pandas library.

&nbsp;
## Schema :
***
The data is organised into the following (star) schema :

&nbsp;
&nbsp;
**The Fact Table** : 
&nbsp;
- Table : songplays

| Column Name |  Type     | Constraints           |
|-------------|-----------|-----------------------|
| songplay_id | INT       | SERIAL , PRIMARY KEY  |    
| start_time  | TIMESTAMP |                       |  
| user_id     | INT       |                       |
| level       | VARCHAR   |                       |
| song_id     | VARCHAR   |                       |
| artist_id   | VARCHAR   |                       |
| session_id  | INT       |                       |
| location    | VARCHAR   |                       |
| user_agent  | VARCHAR   |                       |

&nbsp;
&nbsp;

**The Dimension Tables** :
&nbsp;
- Table :  users

| Column Name |  Type     | Constraints   |
|-------------|-----------|---------------|
| user_id     |  INT      |  PRIMARY KEY  |
| first_name  |  VARCHAR  |  NOT NULL     |
| last_name   |  VARCHAR  |  NOT NULL     |
| gender      |  CHAR(1)  |  NOT NULL     |
| level       |  VARCHAR  |  NOT NULL     |

&nbsp;
- Table :  songs

| Column Name |  Type   | Constraints  |
|-------------|---------|--------------|
| song_id     | VARCHAR | PRIMARY KEY  |
| title       | VARCHAR | NOT NULL     |
| artist_id   | VARCHAR | NOT NULL     |
| year        | INT     | NOT NULL     |
| duration    | FLOAT   | NOT NULL     |

&nbsp;
- Table :  artists

| Column Name |  Type    | Constraints |
|-------------|----------|-------------|
| artist_id   | VARCHAR  | PRIMARY KEY |
| name        | VARCHAR  |             |
| location    | VARCHAR  |             |
| latitude    | FLOAT    |             |
| longitude   | FLOAT    |             |

&nbsp;
- Table :  time

| Column Name |  Type      | Constraints |
|-------------|------------|-------------|
| start_time  |  TIMESTAMP | NOT NULL    |
| hour        |  INT       | NOT NULL    |
| day         |  INT       | NOT NULL    |
| week        |  INT       | NOT NULL    |
| month       |  INT       | NOT NULL    |
| year        |  INT       | NOT NULL    |
| weekday     |  INT       | NOT NULL    |

&nbsp;
&nbsp;

The tables **songs** and **artists** are populated from the song data. From the log data, the dimensional tables **time** and **users** are populated as well as the fact table **songplays** .

&nbsp;
&nbsp;

The schema adapted ensures that all the required information can be retrieved using simple queries. Moreover the ETL process ensure that the database contains data relevant to the analysis.

&nbsp;
&nbsp;

## Tech Stack :
***
The Project is implemented using Python 3 and SQL. The following python libraries are used in the project :
> * psycopg2
> * pandas

&nbsp;

## Running the Project :
***
To run the project locally, make sure the required libraries are installed.

Run the following script to create the database tables :
> python create_tables.py

Run the following script to perform the ETL process and populate the tables in the database :
> python etl.py

Data in the database can be verified using the **test.ipynb** jupyter notebook.
