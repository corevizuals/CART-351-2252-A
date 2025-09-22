# Student Names: John Compuesto + William Nguyen-Luu
# Date: Sept 22, 2025
# Professor Sabine


import requests 
token = "6e40e99cd28a98b8a5783356d6d2a3a2cc0810e0"
url = "https://api.waqi.info/search/"
response = requests.get(url, params={"token": token, "keyword": "montreal"})
results = response.json()
print("Type of 'results':", type(results))  

#print the keys of the 'results' dictionary
print("Keys of 'results':", results.keys()) 

#accessing the 'data' key from the results and store in responseData
responseData = results['data']
print("Type of 'responseData':", type(responseData)) 

#Print all items (stations) in the responseData list
print("Printing each item in responseData:")
for item in responseData:
    print(item)
print("Type of each item in responseData:", type(responseData[0])) 

#Print the keys of one item (station info)
print("Keys of one item:", responseData[0].keys())

#Print the name of each station
print("\nStation Names:")
for item in responseData:
    print("Station name:", item['station']['name'])

#geolocations of each station
print("\nGeolocations of stations:")
for item in responseData:
    geo = item['station']['geo']
    print(f"lat: {geo[0]}")
    print(f"long: {geo[1]}")

#AQI and UID of each station
print("\nAir Quality Index and UID for each station:")
for item in responseData:
    print("Station:", item['station']['name'])
    print(f"  AQI : {item['aqi']}")
    print(f"  UID : {item['uid']}")
    print("-" * 40)

#Use the feed endpoint to get more details about one station using UID
url_feed = "https://api.waqi.info/feed/@5468"
response_feed = requests.get(url_feed, params={"token": token})
results_feed = response_feed.json()

print(results_feed)

response_data_feed = results_feed['data']
print("Type of 'response_data_feed':", type(response_data_feed))  
#checking the results from the feed type

#the keys in response_data_feed
print("Keys in 'response_data_feed':", response_data_feed.keys())

#access and print the AQI and dominant pollutant
aqi_value = response_data_feed['aqi']
dominant_pollutant = response_data_feed['dominentpol']
print("AQI:", aqi_value)
print("Dominant Pollutant:", dominant_pollutant)

#access the iaqi field which is a dictionary of pollutants
iaqi_data = response_data_feed['iaqi']
print("IAQI data keys (pollutants):", iaqi_data.keys())

#use the dominentpol value to get the actual pollutant value
dominant_value = iaqi_data[dominant_pollutant]['v']
print(f"Value of dominant pollutant '{dominant_pollutant}':", dominant_value)
#keys in iaqi match the pollutant names


# Theory explaination - How we got the dominant pollutant value from other cities:
# 1. Use the search API to get the list of stations and their UIDs for the city.
# 2. Loop through each UID and make a request to the feed endpoint
# 3. For each feed response, we accessed:
#    - `data['dominentpol']` to get the dominant pollutant name.
#    - `data['iaqi'][dominentpol]['v']` to get the actual pollutant value.
# 4. This gave us the opportunity to get real data from any city.

