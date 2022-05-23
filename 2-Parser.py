# -*- coding: utf-8 -*-

import os
from bs4 import BeautifulSoup



def cleanString(string):
    #unicode(str(tmp), "utf-8")
    string = string.replace('\"', "")
    string = string.replace("</div>", "")
    string = string.replace("&uuml;", u"ü").replace("&auml;", u"ä").replace("&ouml;", u"ö").replace("&szlig;", u"ß").replace("&Auml;", u"Ä").replace("&Ouml;", u"Ö").replace("&Uuml;", u"Ü")
    string = string.replace("&#252;", u"ü").replace("&#228;", u"ä").replace("&#246;", u"ö").replace("&#223;", u"ß").replace("&#196;", u"Ä").replace("&#214;", u"Ö").replace("&#220;", u"Ü")
    string = string.replace("&nbsp;", " ").replace("&amp;",u"&").replace("&#38;",u"&").replace("&quot;", "")
    string = string.replace("\xa0", " ")
    string = string.replace(";", ",")
    string = string.replace("\t", " ")
    string = string.replace("\n", " ")
    string = string.replace("\r", " ")
    string = string.replace(",,", ",")
    string = string.replace(" ,", ",")
    string = string.replace("Keine Angabe", "")
    if len(string) > 0 and string[0] == "-":
        string = string[1:]
    while string.find("  ") != -1:
            string = string.replace("  ", " ").strip()
    string = string.strip()
    if string == "-":
        string = ""
    return string



directory = "1-Suche/"
outputFile ="uro_portal.csv"

if not os.path.isfile(outputFile):
    header = u"Name;long;lat;Adresse;PLZ;Stadt;Telefon;Fax;Email;Website;Dateiname\n"
    f = open(outputFile,'w+')
    f.write(header)
    f.close()
else:
    pass
f = open(outputFile,'a+')


for filename in os.listdir(u""+directory):
    #if not  filename.startswith("agne"): continue
    print(filename)
    with open(directory + filename,'r+',encoding="utf-8") as f1:
        html = f1.read()
    soup = BeautifulSoup(html, "html.parser")

    for div in soup.find_all("div", attrs ={"class":"gd-eintrag map-location"}):
        name = ""
        address = ""
        zipcode = ""
        town = ""
        phone =""
        fax = ""
        email = ""
        website = ""
        longitude = ""
        latitude = ""

        div1 = div.find("div", class_="gd-name")
        if div1:
            print(cleanString(div1.strong.text))



        data = ""
        data += name
        data += ";"
        data += longitude
        data += ";"
        data += latitude
        data += ";"
        data += address
        data += ";"
        data += zipcode
        data += ";"
        data += town
        data += ";"
        data += phone
        data += ";"
        data += fax
        data += ";"
        data += email
        data += ";"
        data += website
        data += ";"
        data += filename
        data += "\n"
        f.write(data)
f.close()
