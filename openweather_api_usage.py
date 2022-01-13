import os
import csv
import json
import requests

str_req = r"http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}"
csvForm = { "City name": [],
            "Country code": [],
            "Latitude and longitude": [],
            "Temp": [],
            "Wind speed": [],
            "Wind direction": []}

def readCities(filePath):
    cityList = list()
    with open(filePath, "r", encoding="utf-8") as city_file:
        for line in city_file:
            cityList.append(line)
    city_file.close()
    return cityList

def getWeatherInfo(cities):
    api_key = "key to here"
    for city in cities:
        response = requests.get(str_req.format(city, api_key))
        my_weather = response.json()
        if "main" not in my_weather:
            print("Error while getting city information, city: "+ city)
        else:
            print(city + "information is succesfully gotten")
            csvForm["City name"].append(my_weather["name"])
            csvForm["Country code"].append(my_weather["sys"]["country"])
            csvForm["Latitude and longitude"].append(str(my_weather["coord"]["lat"]) + " "+ str(my_weather["coord"]["lon"]))
            csvForm["Temp"].append(float(my_weather["main"]["temp"]) - 273)
            csvForm["Wind speed"].append(my_weather["wind"]["speed"])
            csvForm["Wind direction"].append(my_weather["wind"]["deg"])

def writeToCsv(filePath):
    with open(filePath, "w", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvForm.keys())
        writer.writeheader()
        for index in range(len(csvForm["City name"])):
            writer.writerow({"City name":csvForm["City name"][index],"Country code": csvForm["Country code"][index],
                             "Latitude and longitude": csvForm["Latitude and longitude"][index],
                             "Temp": csvForm["Temp"][index],
                             "Wind speed": csvForm["Wind speed"][index],
                             "Wind direction": csvForm["Wind direction"][index]})
    csvfile.close()

def mainFunction():
    filePath = ""
    currentDir = os.getcwd()
    while not os.path.exists(filePath):
        cityPath = input("Please enter file name with extension to read cities ( file must be in same path with python file ) :")
        filePath = currentDir + "\\" + cityPath
        if not os.path.exists(filePath):
            print("Entered file is not exist")
    cities = readCities(filePath)
    getWeatherInfo(cities)
    writePath = input("Please enter a name for output file: ")
    csvFile = currentDir+ "\\"+writePath + ".csv"
    if open(csvFile, "a"):
        writeToCsv(csvFile)
        print("City weather information file in .csv format is created, path: " + csvFile)
    else:
        print("Could not create csv file.")


mainFunction()





