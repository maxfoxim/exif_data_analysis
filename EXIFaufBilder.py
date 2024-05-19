# -*- coding: utf-8 -*-
"""
@author: stephan.fuchs
Auswertung und Analyse aller EXIF-Daten
"""

#pip install exifread

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import exifread


#Ordner wo Bilder liegen
Ordner="/Users/stephan/Desktop/2024/TEST"
Ordner="/Users/stephan/Desktop/2024/Hochzeit Karsten Rebecca"


Mit_UnterOrdner=False

def belichtungszeit(zeit):
    if zeit<1:
        zeit=int(1/zeit)
        zeit="1/"+str(zeit)
    return zeit


def komma_werte(wert):
    if wert.find("/")!=-1:
        kehrwert=wert.split("/")[1]
        return 1/int(kehrwert)
    else:
        return int(wert)

def blendenwert(wert):
    if wert.find("/")!=-1:
        kehrwert=wert.split("/")[1]
        zaehler=wert.split("/")[0]
        return round(int(zaehler)/int(kehrwert),2)
    else:
        return int(str(wert))

if Mit_UnterOrdner:
    JPG_Dateien=[]
    for sub_ordner in os.listdir(Ordner):
        print (sub_ordner)
        zwi=(os.listdir(Ordner+"/"+sub_ordner))
        for Dateien in zwi:
            JPG_Dateien.append(sub_ordner+"/"+Dateien)
    print(JPG_Dateien)

else:

    #Liste alle Dateien im Ordner aus
    JPG_Dateien=os.listdir(Ordner)
    #JPG_Dateien.sort()
    print("Alle Dateien im Ordner:",JPG_Dateien)
    #auf Macs gibst eine ds_store Datei die vorher gelöscht werden muss
    #JPG_Dateien=[i for i in JPG_Dateien if i[-2:]!="re"] #ds_store Datei rauslöschen

JPG_Dateien=[i for i in JPG_Dateien if i.find("DS_Store")<0] #ds_store Datei rauslöschen
JPG_Dateien=[i for i in JPG_Dateien if i.find("Thumbs.db")<0] #Thumbs.db Datei rauslöschen


data_exif={
    "Name":[],
    "ISO":[],
    "Blende":[],
    "Brennweite":[],
    "Belichtungszeit":[],
    "Belichtungszeit_value":[]
}

for image in JPG_Dateien:
    #ausgabe=get_exif(Ordner+"/"+image)
     
    #print("----------------")
    #print(image)
    f = open(Ordner+"/"+image, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)

    #print(tag["EXIF ISOSpeedRatings"])
    #for tag in tags.keys():
    #    print(tag,tags[tag])

    data_exif["ISO"].append(int(str(tags["EXIF ISOSpeedRatings"])))
    data_exif["Name"].append(Ordner+"/"+image)
    data_exif["Belichtungszeit"].append(tags["EXIF ExposureTime"])
    data_exif["Brennweite"].append(int(round(int(str(tags["EXIF FocalLengthIn35mmFilm"]))/1.5)))

    Blende=blendenwert(str(tags["EXIF ApertureValue"]))
    data_exif["Blende"].append(Blende)

    wert=komma_werte(str(tags["EXIF ExposureTime"]))
    data_exif["Belichtungszeit_value"].append(wert)

    #print(int(str(tags["EXIF FocalLengthIn35mmFilm"]))/1.5   ,  tags["EXIF FocalLengthIn35mmFilm"] )

df = pd.DataFrame(data_exif, columns=['Name','ISO', 'Blende',"Brennweite","Belichtungszeit","Belichtungszeit_value"])
print(df)

fig, ax = plt.subplots()

ax.scatter(df["Belichtungszeit_value"], df["ISO"], s=df["Blende"]*10,c=df["Blende"],alpha=0.5)
ax.set_xlabel('Belichtungszeit', fontsize=15)
ax.set_ylabel('ISO', fontsize=15)
ax.set_title('Lichtstärke')
ax.grid(True)
fig.tight_layout()
plt.show()


print(df)





    
    



