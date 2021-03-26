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
    """The front page, where users can view measurements

    Returns:
        str: the generated page
    """
    return redirect(f"{__CONFIG['prefix']}/measurements")

@app.route("/measurements", methods=["GET"])
def measurements() -> str:
    return render_template("index.html", list=db.ten_measurements(), 
                            maxtemp=db.max_temp()[0], mintemp=db.min_temp()[0], 
                            maxhum=db.max_hum()[0], minhum=db.min_hum()[0], 
                            maxpres=db.max_pres()[0], minpres=db.min_pres()[0])

@app.route("/allmeasurements/<int:paged>", methods=["GET"])
def allmeasurements(paged) -> str:
    return render_template("records.html", list=db.all_measurements(paged))

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
        if "pres" in payload:
            db.store_measurement(payload["temp"], payload["hum"], payload["pres"])
            print("new measure!")

def handler(signal_received, frame):
    # Handle any cleanup here
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    mqtt.unsubscribe_all()
    exit(0)

if __name__ == "__main__":
    signal(SIGINT, handler)
    app.run(
        debug=__CONFIG["debug"], 
        port=__CONFIG["port"],
        use_reloader=False)