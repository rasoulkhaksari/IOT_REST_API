# **IOT RSET API**
## **IOT data aggregator using Django Rest Framework and PostgreSQL**

**This is a sample IOT data aggregator server which receives IOT devices data continually and stores them in a PostgreSQL RDBMS database engine. 
Furthermore, it serves statistically analysed aggregated data according to needed user timeframes.**   
<br>
**Sample Input Data**
```
[{
    "timestamp": "2022-01-21T10:56:18.950901",
    "reading": 0.63,
    "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
    "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
},
{
    "timestamp": "2022-01-21T10:57:18.950901",
    "reading": 0.9,
    "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
    "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
},
{
    "timestamp": "2022-01-21T10:58:18.950901",
    "reading": 0.9,
    "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
    "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
}]
```  
<br>  

**Sample Output Data**
```
{
    "data": [
        {
            "device_id": "UUIDv4 string",
            "customer_id": "UUIDv4 string",
            "from": "2021-01-01T00:00:00+00:00",
            "to": "2021-01-01T00:20:00+00:00",
            "aggregation_size_minutes": 10,
            "aggregated_values": [
                {
                    "from": "2021-01-01T00:00:00+00:00",
                    "value": 5.5
                },
                {
                    "from": "2021-01-01T00:10:00+00:00",
                    "value": 15.5
                }
            ]
        },
        ...
    ]
}
```
<br><br>

## **How to run the code** 
You need Docker tool and docker-compose tool to run this code
1. Download this repo (as a zip file)
2. Unzip the zip file in your desired path
3. Open up OS Terminal in this path
4. Build project required docker images
```
$ docker-compose build
```
5. Setup and run project docker containers
```
$ docker-compose up
```
6. Visit project admin web page in your web prowser: http://localhost:8008/admin/ , use "admin" for username and "1234" for password to login.
7. Create two user in user management section. Create two new user as two sample customer, fill their customer ID field with these two sample ID
```
[Customer1]
username: customer1
password: User1@1234
customer id: b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df

[Customer2]
username: customer2
password: User2@1234
customer id: 09a96248-2a72-4288-ac9b-02f2779161e3

```
8. now application is initialized and ready to test using Postman tool
9. open Postman and login to application with Customer 1 credentials, then you will receive Authenctication token like below
```
[Request]
curl --location --request POST 'http://localhost:8000/api/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "customer1",
    "password": "User1@1234"
}'

[Response]
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0Mjg0MzY2MCwiaWF0IjoxNjQyNzU3MjYwLCJqdGkiOiJmMmU2ZWNkMTUxNDE0ZTYyYmZlYjJlZTUyN2VhY2IyOCIsInVzZXJfaWQiOjJ9.nqJ4BzmyROlPw0UrChLGyBbgVbbAPA8hJ-hcU3IFA-4",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQyNzU3NTYwLCJpYXQiOjE2NDI3NTcyNjAsImp0aSI6IjdmZWI3MDc4ZDNkZDQ1YWM4NDI3NDY2OTgxMDk2NjhhIiwidXNlcl9pZCI6Mn0.jAykboda6xxOA4lnmHDamwTivoLvVtG-35tnamTvp7E"
}
```  
10. Add customer 1 sample data (available in sample_data.json file) to application using Postman. use customer 1  access token in previous step for authentication.
```
[Request]
curl --location --request POST 'http://localhost:8000/api/device/create/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQyNzU3NTYwLCJpYXQiOjE2NDI3NTcyNjAsImp0aSI6IjdmZWI3MDc4ZDNkZDQ1YWM4NDI3NDY2OTgxMDk2NjhhIiwidXNlcl9pZCI6Mn0.jAykboda6xxOA4lnmHDamwTivoLvVtG-35tnamTvp7E' \
--header 'Content-Type: application/json' \
--data-raw '[
    {
        "timestamp": "2022-01-21T10:56:18.950901",
        "reading": 0.63,
        "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
        "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
    },
    {
        "timestamp": "2022-01-21T10:57:18.950901",
        "reading": 0.9,
        "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
        "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
    },
    {
        "timestamp": "2022-01-21T10:58:18.950901",
        "reading": 0.9,
        "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
        "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
    },
    {
        "timestamp": "2022-01-21T10:59:18.950901",
        "reading": 0.32,
        "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
        "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
    },
    {
        "timestamp": "2022-01-21T11:00:18.950901",
        "reading": 0.96,
        "device_id": "1cf67335-0793-42ad-80f3-3156cabc9da9",
        "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
    },
    {
        "timestamp": "2022-01-21T11:01:18.950901",
        "reading": 0.45,
        "device_id": "1cf67335-0793-42ad-80f3-3156cabc9da9",
        "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
    },
    {
        "timestamp": "2022-01-21T11:02:18.950901",
        "reading": 0.55,
        "device_id": "1cf67335-0793-42ad-80f3-3156cabc9da9",
        "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
    },
    {
        "timestamp": "2022-01-21T11:03:18.950901",
        "reading": 0.94,
        "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
        "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
    },
    {
        "timestamp": "2022-01-21T11:04:18.950901",
        "reading": 0.61,
        "device_id": "94324014-0b4c-4b7e-840c-ff82f5304b06",
        "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
    },
    {
        "timestamp": "2022-01-21T11:05:18.950901",
        "reading": 0.09,
        "device_id": "71bf19cb-e7e7-4334-af31-5ebba56a655d",
        "customer_id": "b0c2bda5-0d6d-4c6a-86d4-76489ea2b9df"
    }
]'
```
11. Add customer 2 sample data (available in sample_data.json file) to application using Postman. use customer 2 access token in previous step for authentication.(same operation for every new customer)
12. now every customer can see its own data aggegated (mean) values for every 5 minute. Although a customer can filter required data report using 3 parameter: Start time, End time, Aggregation size (in minutes)  
**Note:** administrator can see all customers data.
```
[Request]
curl --location --request GET 'http://localhost:8000/api/devices' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQyNzU4NDg4LCJpYXQiOjE2NDI3NTgxODgsImp0aSI6ImRiNzkxNWU1YmE3NjRmYjhiYTEwNTYzZGE2MmQxZjk2IiwidXNlcl9pZCI6MX0.25pKWxOnI-dMHc5eoYwwbkildLrCDwcAGZ9cn-YAY3U'
```
13.  Grafana Panel  
Grafana is ..., web can watch device logs in Grafana through below steps:  
- Open up http://localhost:8009/ url in web browser 
- To login use "admin" as username and "admin" as password, and then you can reset admin password.
- After login, go to Configuration > data sources, http://localhost:8009/datasources
- Click on "Add data source" and select PostgreSQL
- Set PostgreSQL Connection settings as below:
  - Host:       db:5432
  - Database:   iotdb
  - User:       iot
  - Password:   pwd@iotdb
  - TLS/SSL Mode:   disable
- Click on "Save & test"
- After Data source setup, goto Dashborads manager, http://localhost:8009/dashboards
-  Click on "New Dashboard" > "Add an empty panel ()"
-  In Query Builder write below Query:
```
SELECT
  floor(extract(epoch from "timestamp")/300)*300 AS "time",
  avg(reading) AS "reading"
FROM "IOTdevice"
GROUP BY 1
ORDER BY 1
```
![fig1](fig1.jpg)

14. There are some unit tests in Django application tests.py module which run on appication deployment initialization phase, such as:
- test_login 
- test_JWT
- test_append_device_data
- test_get_device_data
