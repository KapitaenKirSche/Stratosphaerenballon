import MPU9250

import csv
import time
import datetime
import os

# Zielordner: /home/benjamin/data
data_folder = "/home/benjamin/data"
os.makedirs(data_folder, exist_ok=True)

filenumber = 0
def get_new_filename():
    # Generiere einen neuen Dateinamen
    global filenumber
    filenumber += 1
    return os.path.join(data_folder, f"sensor_data_{filenumber}.csv")

# Initiale CSV-Datei und Erstellungszeit festlegen
filename = "innit"
start_time = time.time()
file_creation_time = time.time()
running = True

def create_new_csv():
    """Erstellt eine neue CSV-Datei mit Header."""
    global filename, file_creation_time
    filename = get_new_filename()
    file_creation_time = time.time()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'timestamp',
            'acc_x', 'acc_y', 'acc_z',
            'gyro_x', 'gyro_y', 'gyro_z',
            'mag_x', 'mag_y', 'mag_z'
        ])

def logSensorData():
    #Alle 5 Minuten
    if time.time() - file_creation_time >= 5 * 60:
        # Erstelle eine neue Datei und aktualisiere den Zeitstempel
        create_new_csv()

    #Get Data
    mpu = MPU9250.pullData()
    accelerometer = mpu[0]
    gyroscope = mpu[1]
    magnetometer = mpu[2]

    timestamp = datetime.datetime.now().isoformat()
    # Zeile mit Sensordaten erstellen
    row = [timestamp] + accelerometer + gyroscope + magnetometer

    # Daten in die aktuelle CSV-Datei schreiben
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

    print(f"Gespeichert in {filename}: {row}")

create_new_csv()

next_call = time.time()
next_call = next_call - (next_call % 1) + 1 #Volle nächste Sekunde
while running:
    now = time.time()
    if now >= next_call:
        logSensorData()
        next_call += 1
    if now-start_time >= 60:
        running = False