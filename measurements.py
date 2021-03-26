"""Creates a simpleminded measurements web site based on a SQLite db"""
from flask import Flask, render_template, redirect, url_for, request, escape
from flask.wrappers import Response
from signal import signal, SIGINT
from sys import exit
from flask_mqtt import Mqtt
import json
import measurements_db as db
import itwot
import re
import platform
import argparse
import time

__CONFIG = itwot.config()
app = Flask(__name__)
app.config["MQTT_BROKER_URL"] = "itwot.cs.au.dk"
app.config["MQTT_BROKER_PORT"] = 1883

mqtt = Mqtt(app)

__PORTS = {
    "w07": 3000,
    "w08": 3500,
    "w09": 4000,
    "w10": 4500,
    "w11": 5000,
    "w12": 5500,
    "opg3": 6000,
    "opg4a": 6500,
    "opg4b": 7000,
}


@app.route("/")
def index() -> str:
    """The front page, where users can enter a measurement

    Returns:
        str: the generated page
    """
    return redirect(f"{__CONFIG['prefix']}/measurements")


@app.route("/measurements/<int:rowid>", methods=["GET", "DELETE"])
def measurement(rowid: int) -> str:
    """Generates a specific measurement

    Args:
        rowid (int): the id of the desired measurement in the DB

    Returns:
        str: the generated page
    """
    if request.method == "DELETE":
        if db.delete_measurement(rowid):
            return Response(status=200)
        return Response(status=404)
    return render_template("measurement.html", row=db.get_measurement(rowid))

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("connected to MQTT broker...", end="")
    mqtt.subscribe("au602716/#")
    print("subscribed")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    if topic.endswith("/json"):
        payload = json.loads(payload)
        print("yay")
        if "pres" in payload:
            db.store_measurement(payload["temp"], payload["hum"], payload["pres"])
            print(f"Received MQTT on {topic}: {payload}")
    

@app.route("/measurements", methods=["GET", "POST"])
def measurements() -> str:
    """If invoked with POST, stores the supplied measurement in the DB, and redirect to the measurements.
    If invoked with GET, generates the measurements

    Returns:
        str: the generated page
    """
    if request.method == "POST":
        if "temperature" in request.form and "humidity" in request.form and "pressure" in request.form:
            db.store_measurement(
                escape(request.form["temperature"]), escape(request.form["humidity"]), escape(request.form["pressure"])
            )
        return redirect(f"{__CONFIG['prefix']}/measurements")
    return render_template("index.html", list=db.ten_measurements(), maxtemp=db.max_temp()[0], mintemp=db.min_temp()[0], maxhum=db.max_hum()[0], minhum=db.min_hum()[0], maxpres=db.max_pres()[0], minpres=db.min_pres()[0])

@app.route("/allmeasurements", methods=["GET"])
def allmeasurements() -> str:
    """If invoked with POST, stores the supplied measurement in the DB, and redirect to the measurements.
    If invoked with GET, generates the measurements

    Returns:
        str: the generated page
    """
    return render_template("records.html", list=db.all_measurements())

@app.route("/maxtemp", methods=["GET"])
def maxtemp() -> str:
    return render_template("index.html", list=db.max_temp())

@app.route("/mintemp", methods=["GET"])
def mintemp() -> str:
    return render_template("index.html", list=db.min_temp())

@app.route("/maxhum", methods=["GET"])
def maxhum() -> str:
    return render_template("index.html", list=db.max_hum())

@app.route("/minhum", methods=["GET"])
def minhum() -> str:
    return render_template("index.html", list=db.min_hum())

@app.route("/maxpres", methods=["GET"])
def maxpres() -> str:
    return render_template("index.html", list=db.max_pres())

@app.route("/minpres", methods=["GET"])
def minpres() -> str:
    return render_template("index.html", list=db.min_pres())

def handler(signal_received, frame):
    # Handle any cleanup here
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    mqtt.unsubscribe_all()
    exit(0)

if __name__ == "__main__":
    signal(SIGINT, handler)
    app.run(
        debug=__CONFIG["debug"], 
        port=__CONFIG["port"])