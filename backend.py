
def latloncsv(file):
    import pandas as pd
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="stewart12334@aol.com")
    df=pd.read_csv(file)

    df.columns = map(str.capitalize, df.columns)

    if "Address" in df.columns:
        df1=df["Address"]
        listlat=[]
        listlon=[]
        for address in df1:
            try:
                location = geolocator.geocode(address)
                listlat.append(location.latitude)
                listlon.append(location.longitude)
            except AttributeError:
                listlat.append(None)
                listlon.append(None)
        df["Latitude"]=listlat
        df["Longitute"]=listlon
        print(type(file))
        df.to_csv("updated.csv")
    else:
        print("There is no Address column in your data")
