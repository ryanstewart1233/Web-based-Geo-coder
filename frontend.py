from flask import Flask, render_template, url_for, request, send_file
import pandas as pd
from geopy.geocoders import Nominatim

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/success", methods=["POST"])
def success():
    if request.method == "POST":
        global file
        file = request.files["filename"]
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
            #can incorperate datetime to generate unique filenames. (but we didn't come up with that bit)
            df.to_csv("uploads/updated" + file.filename, index=None)
            return render_template("home.html", text=df.to_html(index=None), btn ="download.html")
        else:
            return render_template("home.html", text="This file does not have an address column, please try a different file")

@app.route("/download-file/")
def download():
    return send_file("uploads/updated" + file.filename, attachment_filename="geocodedfile.csv", mimetype="csv",  as_attachment=False)
    #figure out a way to fix this damn download thing!!!

if __name__ == ("__main__"):
    app.run(debug = True)
