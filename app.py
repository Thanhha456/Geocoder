from flask import Flask, render_template, request, send_file
import pandas, datetime
from geopy.geocoders import Nominatim 


app = Flask(__name__)
nom = Nominatim(user_agent="geocoder_app")

@app.route('/')

def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])

def success():
    global filename
    if request.method == "POST":
        file = request.files['file']
        try:
            table = pandas.read_csv(file)       
            if "address" in table.columns.tolist():
                table["Address"] = table["address"]
                table = table.drop("address", 1)
    
            table["Coordinates"] = table["Address"].apply(nom.geocode)
            table["Latitude"] = table["Coordinates"].apply(lambda x: x.latitude if x != None else None)
            table["Longitude"] = table["Coordinates"].apply(lambda x: x.longitude if x != None else None)
            table = table.drop("Coordinates", 1)
            filename = datetime.datetime.now().strftime("uploads/%Y-%m-%d-%H-%M-%S-%f" + ".csv")
            table.to_csv(filename, index=None)

            return render_template("index.html",text=table.to_html(), btn="download.html")
        except:
            return render_template("index.html", text="Please make sure you have an address column in your CSV file!")

@app.route("/download")

def download():
    return send_file(filename, attachment_filename ="geocode.csv", as_attachment=True)

if __name__ == "__main__":
    app.debug = True
    app.run(port=5001)
