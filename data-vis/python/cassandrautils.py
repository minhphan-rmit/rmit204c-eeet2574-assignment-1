import os
import sys
import pandas as pd
from cassandra.cluster import BatchStatement, Cluster, ConsistencyLevel
from cassandra.query import dict_factory

# Cassandra configuration
CASSANDRA_HOST = os.environ.get("CASSANDRA_HOST", "localhost")
CASSANDRA_KEYSPACE = os.environ.get("CASSANDRA_KEYSPACE", "kafkapipeline")

# Table names
WEATHER_TABLE = os.environ.get("WEATHER_TABLE", "weatherreport")
FAKER_TABLE = os.environ.get("FAKER_TABLE", "fakerdata")
MARSWEATHER_TABLE = os.environ.get("MARSWEATHER_TABLE", "marsweather")
NEO_TABLE = os.environ.get("NEO_TABLE", "neodata")

def saveData(dfrecords, tablename, cqlsentence):
    """
    Generic function to save a DataFrame to Cassandra.
    """
    cluster = Cluster([CASSANDRA_HOST])
    session = cluster.connect(CASSANDRA_KEYSPACE)
    session.set_keyspace(CASSANDRA_KEYSPACE)

    counter = 0
    totalcount = 0
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    insert = session.prepare(cqlsentence)
    batches = []

    for idx, val in dfrecords.iterrows():
        batch.add(insert, tuple(val))
        counter += 1
        if counter >= 100:
            print(f"Inserting {counter} records into {tablename}")
            totalcount += counter
            counter = 0
            batches.append(batch)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

    if counter != 0:
        batches.append(batch)
        totalcount += counter

    [session.execute(b, trace=True) for b in batches]
    print(f"Inserted {totalcount} rows into {tablename}")


def loadDF(targetfile, target):
    """
    Load a CSV file and save it to the appropriate Cassandra table.
    """
    if target == 'weather':
        colsnames = ['forecastdate', 'location', 'description', 'temp', 'feels_like', 'temp_min',
                     'temp_max', 'pressure', 'humidity', 'wind', 'sunrise', 'sunset']
        cqlsentence = f"INSERT INTO {WEATHER_TABLE} (forecastdate, location, description, temp, feels_like, temp_min, temp_max, pressure, humidity, wind, sunrise, sunset) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    elif target == 'faker':
        colsnames = ['name', 'ssn', 'job', 'age', 'gender', 'income', 'credit_card_provider',
                     'credit_card_number', 'credit_card_expire', 'credit_card_security_code',
                     'city', 'country', 'postcode', 'street_name', 'monthly_purchases', 'avg_purchase_amount']
        cqlsentence = f"INSERT INTO {FAKER_TABLE} (name, ssn, job, age, gender, income, credit_card_provider, credit_card_number, credit_card_expire, credit_card_security_code, city, country, postcode, street_name, monthly_purchases, avg_purchase_amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    elif target == 'marsweather':
        colsnames = ['sol', 'season', 'first_utc', 'last_utc', 'at_avg', 'at_min', 'at_max',
                     'hws_avg', 'hws_min', 'hws_max', 'pre_avg', 'pre_min', 'pre_max', 'most_common_wind']
        cqlsentence = f"INSERT INTO {MARSWEATHER_TABLE} (sol, season, first_utc, last_utc, at_avg, at_min, at_max, hws_avg, hws_min, hws_max, pre_avg, pre_min, pre_max, most_common_wind) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    elif target == 'near_earth_objects':
        # Updated column names for simplified neodata table
        colsnames = ['id', 'name', 'close_approach_date', 'relative_velocity_kph', 'miss_distance_km',
                     'estimated_diameter_min_km', 'estimated_diameter_max_km', 'is_potentially_hazardous', 'orbiting_body']
        
        # Updated CQL for the neodata table
        cqlsentence = f"INSERT INTO {NEO_TABLE} (id, name, close_approach_date, relative_velocity_kph, miss_distance_km, estimated_diameter_min_km, estimated_diameter_max_km, is_potentially_hazardous, orbiting_body) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    else:
        print(f"Unsupported target: {target}")
        return

    dfData = pd.read_csv(targetfile, header=None, names=colsnames)
    saveData(dfData, target, cqlsentence)


def getDF(source_table):
    """
    Retrieve data from a Cassandra table and return it as a Pandas DataFrame.
    """
    cluster = Cluster([CASSANDRA_HOST])
    session = cluster.connect(CASSANDRA_KEYSPACE)
    session.row_factory = dict_factory

    if source_table not in (WEATHER_TABLE, FAKER_TABLE, MARSWEATHER_TABLE, NEO_TABLE):
        print(f"Unsupported table: {source_table}")
        return None

    cqlquery = f"SELECT * FROM {source_table};"
    rows = session.execute(cqlquery)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    action = sys.argv[1]
    target = sys.argv[2]
    targetfile = sys.argv[3] if len(sys.argv) > 3 else None

    if action == "save" and targetfile:
        loadDF(targetfile, target)
    elif action == "get":
        df = getDF(target)
        print(df.head())
    else:
        print("Usage: python cassandrautils.py <save|get> <target> [targetfile]")
