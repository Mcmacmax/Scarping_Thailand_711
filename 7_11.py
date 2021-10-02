import requests
import urllib
import pandas as pd
import time
import random

#Loc-711
def get_loc_711 (lat:float,long:float):
    url = "https://7eleven-api-prod.jenosize.tech/v1/Store/GetStoreByCurrentLocation"
    data = {"latitude": lat,"longitude": long}
    headers = {'Accept': 'application/json, text/plain, */*'}
    response = requests.post(url,headers=headers,data=data)
    json_data = response.json()
    return json_data
##################################################################
#LAT,LONG INPUT FOR Loc7-11
def get_loc_tambon_thailand ():
    url = 'https://opend.data.go.th/get-ckan/datastore_search?resource_id=48039a2a-2f01-448c-b2a2-bb0d541dedcd&limit=10000'  
    headers = {'api-key': 'ระบุ Key API'} #ให้ไปสมัครที่ เวป https://opend.data.go.th/register_api/signup.php?
    response = requests.get(url,headers=headers)
    json_data = response.json()
    df_province = pd.DataFrame(columns= ['ID','Province', 'Aumphoe', 'Tambon', 'LAT', 'LONG'])
    count = 1
    for i in json_data["result"]["records"]:
        newrow = {'ID': i['_id'],'Province': i['CHANGWAT_T'], 'Aumphoe': i['AMPHOE_T'], 'Tambon': i['TAMBON_T'], 'LAT': i['LAT'], 'LONG' : i['LONG']}
        df_province = df_province.append(newrow , ignore_index=True)
        print(count)
        count += 1 
    return df_province

#DF_Thailand_Lat_long
df_Lat_Long = get_loc_tambon_thailand()
#Set Output DataFrame Columms
df_711 = pd.DataFrame(columns= ['ID_711','Name_Branch','Address','Lat', 'Long','Province','Aumphoe','Tambon'])\

#Input Lat,Long from DF_Thailand_Lat_long
for a in df_Lat_Long.values :
    count = 1
    print('Lat: ', a[4] ,'Long: ', a[5])
    location_711 = get_loc_711(a[4],a[5])
    print(count,' : จำนวน 7-11 จาก LatLong: ',len(location_711['data']))
    #Write ร้าน 7-11 ลง DataFrame
    for i in location_711['data']:
        newrow = {'ID_711': i['id'],'Name_Branch': i['name'],'Address': i['address'],'Lat': i['lat']\
            , 'Long' :i['lng'],'Province' : i['province'],'Aumphoe' : i['district'], 'Tambon': i['subdistrict']}
        df_711 = df_711.append(newrow , ignore_index=True)
        print(df_711)
    print(df_711)
    time.sleep(random.randint(90,150)) #ตั้งค่า Sleep เพื่อไม่ให้เกิดการ Rest API บ่อยเกินไปจนถูก Block
    count += 1

df_711.to_excel("Location_711.xlsx")