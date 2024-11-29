#!/bin/sh

# OpenWeather Sink
echo "Starting Weather Sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "weathersink",
  "config": {
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",  
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable":"false",
    "tasks.max": "10",
    "topics": "weather",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.weather.kafkapipeline.weatherreport.mapping": "location=value.location, forecastdate=value.report_time, description=value.description, temp=value.temp, feels_like=value.feels_like, temp_min=value.temp_min, temp_max=value.temp_max, pressure=value.pressure, humidity=value.humidity, wind=value.wind, sunrise=value.sunrise, sunset=value.sunset",
    "topic.weather.kafkapipeline.weatherreport.consistencyLevel": "LOCAL_QUORUM"
  }
}'

# FakerAPI Sink
echo "Starting Faker Sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "fakersink",
  "config": {
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",  
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable":"false",
    "tasks.max": "10",
    "topics": "faker",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.faker.kafkapipeline.fakerdata.mapping": "name=value.name, ssn=value.ssn, job=value.job, age=value.age, gender=value.gender, income=value.income, credit_card_provider=value.credit_card_provider, credit_card_number=value.credit_card_number, credit_card_expire=value.credit_card_expire, credit_card_security_code=value.credit_card_security_code, city=value.city, country=value.country, postcode=value.postcode, street_name=value.street_name, monthly_purchases=value.monthly_purchases, avg_purchase_amount=value.avg_purchase_amount",
    "topic.faker.kafkapipeline.fakerdata.consistencyLevel": "LOCAL_QUORUM"
  }
}'

# Mars Weather Sink
echo "Starting Mars Weather Sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "marsweathersink",
  "config": {
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "false",
    "tasks.max": "10",
    "topics": "marsweather",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.marsweather.kafkapipeline.marsweather.mapping": "sol=value.sol, season=value.season, first_utc=value.first_utc, last_utc=value.last_utc, at_avg=value.at_avg, at_min=value.at_min, at_max=value.at_max, hws_avg=value.hws_avg, hws_min=value.hws_min, hws_max=value.hws_max, pre_avg=value.pre_avg, pre_min=value.pre_min, pre_max=value.pre_max, most_common_wind=value.most_common_wind",
    "topic.marsweather.kafkapipeline.marsweather.consistencyLevel": "LOCAL_QUORUM"
  }
}'

echo "Starting NEO Sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "neosink",
  "config": {
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "false",
    "tasks.max": "10",
    "topics": "near_earth_objects",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.near_earth_objects.kafkapipeline.neodata.mapping": "id=value.id, name=value.name, close_approach_date=value.close_approach_date, relative_velocity_kph=value.relative_velocity_kph, miss_distance_km=value.miss_distance_km, estimated_diameter_min_km=value.estimated_diameter_min_km, estimated_diameter_max_km=value.estimated_diameter_max_km, is_potentially_hazardous=value.is_potentially_hazardous, orbiting_body=value.orbiting_body",
    "topic.near_earth_objects.kafkapipeline.neodata.consistencyLevel": "LOCAL_QUORUM"
  }
}'

echo "Done."

