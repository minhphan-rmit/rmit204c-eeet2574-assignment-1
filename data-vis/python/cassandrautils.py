import os
import sys
import pandas as pd
from cassandra.cluster import Cluster, BatchStatement, ConsistencyLevel
from cassandra.query import dict_factory


# Environment variables and defaults
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "kafkapipeline")

WEATHER_TABLE = os.getenv("WEATHER_TABLE", "weatherreport")
# TWITTER_TABLE = os.getenv("TWITTER_TABLE", "twitterdata")  # Commented if unused


# Common function to connect to Cassandra
def get_cassandra_session():
    cluster = Cluster([CASSANDRA_HOST]) if isinstance(CASSANDRA_HOST, str) else Cluster(CASSANDRA_HOST)
    return cluster.connect(CASSANDRA_KEYSPACE)


# Generalized save function
def save_data(dfrecords, table_name, insert_query):
    session = get_cassandra_session()
    counter = 0
    total_count = 0

    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    insert = session.prepare(insert_query)
    batches = []

    for _, record in dfrecords.iterrows():
        batch.add(insert, tuple(record))
        counter += 1
        if counter >= 100:
            print(f"Inserting {counter} records...")
            total_count += counter
            counter = 0
            batches.append(batch)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    
    if counter != 0:
        batches.append(batch)
        total_count += counter

    [session.execute(b) for b in batches]
    print(f"Inserted {total_count} rows in total.")


# Save weather data
def save_weather_data(dfrecords):
    cql_sentence = f"""
        INSERT INTO {WEATHER_TABLE} 
        (forecastdate, location, description, temp, feels_like, temp_min, temp_max, 
         pressure, humidity, wind, sunrise, sunset)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    save_data(dfrecords, WEATHER_TABLE, cql_sentence)


# Save Twitter data (if still needed)
# def save_twitter_data(dfrecords):
#     cql_sentence = f"""
#         INSERT INTO {TWITTER_TABLE} 
#         (tweet_date, location, tweet, classification)
#         VALUES (?, ?, ?, ?)
#     """
#     save_data(dfrecords, TWITTER_TABLE, cql_sentence)


# Generalized load function
def load_df_to_table(file_path, target):
    if target == 'weather':
        column_names = [
            'description', 'temp', 'feels_like', 'temp_min', 'temp_max', 
            'pressure', 'humidity', 'wind', 'sunrise', 'sunset', 'location', 'report_time'
        ]
        df_data = pd.read_csv(file_path, header=None, names=column_names)
        df_data['report_time'] = pd.to_datetime(df_data['report_time'])
        save_weather_data(df_data)

    # elif target == 'twitter':  # Commented out unless Twitter is still needed
    #     column_names = ['tweet', 'datetime', 'location', 'classification']
    #     df_data = pd.read_csv(file_path, header=None, names=column_names)
    #     df_data['datetime'] = pd.to_datetime(df_data['datetime'])
    #     save_twitter_data(df_data)


# Generalized data retrieval function
def get_data_as_dataframe(table_name):
    session = get_cassandra_session()
    session.row_factory = dict_factory

    if table_name not in (WEATHER_TABLE,):  # Add TWITTER_TABLE if needed
        print(f"Invalid table name: {table_name}")
        return None

    query = f"SELECT * FROM {table_name};"
    rows = session.execute(query)
    return pd.DataFrame(rows)


# Wrapper for weather data retrieval
def get_weather_data():
    return get_data_as_dataframe(WEATHER_TABLE)


# Wrapper for Twitter data retrieval (if still needed)
# def get_twitter_data():
#     return get_data_as_dataframe(TWITTER_TABLE)


# Entry point for CLI-based operations
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python cassandra_utils.py <action> <target> <file_path>")
        sys.exit(1)

    action = sys.argv[1]
    target = sys.argv[2]
    file_path = sys.argv[3] if len(sys.argv) > 3 else None

    if action == "save":
        if not file_path:
            print("File path required for saving data.")
            sys.exit(1)
        load_df_to_table(file_path, target)
    elif action == "get":
        if target == "weather":
            print(get_weather_data())
        # elif target == "twitter":  # Commented out unless needed
        #     print(get_twitter_data())
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
