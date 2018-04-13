# Appointments schedule
This Web service is using python flask

## Running
docker-compose build

docker-compose up -d

## Database parameters
"AK","Name","Surname","Date", "Time", "ID"

## Possible operations

1) GET all schedules:

curl -i http://localhost:80/visits/schedules

2) GET appointments by any parameter

curl -curl -i http://localhost:80/visits/schedules/<parameter>

2) DELETE appointment

curl -i -X DELETE http://localhost:80/visits/<ID>

3) POST create a new appointment

curl -i -X POST -H "Content-Type: application/json" -d '{ "AK": "<new_AK>, "Name": "<new_Name>, "Surname": "<new_Surname>, "Date": "<new_Date>" "Time": "<new_Time>}' http://localhost:80/visits/schedules

4) PUT change Date and Time for an appointment

curl -i -H "Content-type: application/json" -X PUT -d '{"Date": "<new_Date>", "Time": "<new_Time>"}' http://localhost:80/visits/schedules/<ID>
