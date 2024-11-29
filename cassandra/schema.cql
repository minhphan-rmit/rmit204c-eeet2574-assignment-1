USE kafkapipeline;

CREATE TABLE IF NOT EXISTS kafkapipeline.weatherreport (
  forecastdate TIMESTAMP,
  location TEXT,
  description TEXT,
  temp FLOAT,
  feels_like FLOAT,
  temp_min FLOAT,
  temp_max FLOAT,
  pressure FLOAT,
  humidity FLOAT,
  wind FLOAT,
  sunrise BIGINT,
  sunset BIGINT,
  PRIMARY KEY (location, forecastdate)
);

CREATE TABLE IF NOT EXISTS kafkapipeline.fakerdata (
  name TEXT,                      -- Name of the person
  ssn TEXT,                       -- Social Security Number
  job TEXT,                       -- Job title
  age INT,                        -- Age of the person
  gender TEXT,                    -- Gender
  income FLOAT,                   -- Annual income in USD
  credit_card_provider TEXT,      -- Credit card provider
  credit_card_number TEXT,        -- Credit card number
  credit_card_expire TEXT,        -- Credit card expiration date
  credit_card_security_code TEXT, -- Credit card security code
  city TEXT,                      -- City
  country TEXT,                   -- Country
  postcode TEXT,                  -- Postcode
  street_name TEXT,               -- Street name
  monthly_purchases INT,          -- Number of purchases per month
  avg_purchase_amount FLOAT,      -- Average purchase amount in USD
  PRIMARY KEY (name)              -- Use name as the partition key
);

CREATE TABLE IF NOT EXISTS kafkapipeline.marsweather (
  sol INT,                  -- Martian Sol (day)
  season TEXT,              -- Martian season (winter, spring, summer, fall)
  first_utc TIMESTAMP,      -- First recorded timestamp (Earth time)
  last_utc TIMESTAMP,       -- Last recorded timestamp (Earth time)
  at_avg FLOAT,             -- Average atmospheric temperature (°C)
  at_min FLOAT,             -- Minimum atmospheric temperature (°C)
  at_max FLOAT,             -- Maximum atmospheric temperature (°C)
  hws_avg FLOAT,            -- Average horizontal wind speed (m/s)
  hws_min FLOAT,            -- Minimum horizontal wind speed (m/s)
  hws_max FLOAT,            -- Maximum horizontal wind speed (m/s)
  pre_avg FLOAT,            -- Average atmospheric pressure (Pa)
  pre_min FLOAT,            -- Minimum atmospheric pressure (Pa)
  pre_max FLOAT,            -- Maximum atmospheric pressure (Pa)
  most_common_wind TEXT,    -- Most common wind direction (e.g., N, ESE)
  PRIMARY KEY (sol)         -- Use Sol as the partition key
);

CREATE TABLE IF NOT EXISTS kafkapipeline.neodata (
  id TEXT,                        
  name TEXT,                      
  close_approach_date DATE,       
  relative_velocity_kph DOUBLE,    
  miss_distance_km DOUBLE,         
  estimated_diameter_min_km DOUBLE,
  estimated_diameter_max_km DOUBLE,
  is_potentially_hazardous BOOLEAN,
  orbiting_body TEXT,             
  PRIMARY KEY (id)
);
