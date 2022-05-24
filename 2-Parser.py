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
    header = u"Name;Klinikum;Praxis;long;lat;Adresse;PLZ;Stadt;Telefon;Fax;Email;Website;Dateiname\n"
    f = open(outputFile,'w+')
    f.write(header)
    f.close()
else:
    pass
f = open(outputFile,'a+')

obj= []

for filename in os.listdir(u""+directory):
    #if not  filename.startswith("agne"): continue
    print(filename)
    with open(directory + filename,'r+',encoding="utf-8") as f1:
        html = f1.read()
    soup = BeautifulSoup(html, "html.parser")
    clinic_keywords = ["klinik", "Klinik", "krankenhaus", "Krankenhaus", "KKH","Institut","institut", "Center", "Zentrum", "Centrum","MVZ"]
    for div in soup.find_all("div", attrs ={"class":"gd-eintrag map-location"}):
        name = ""
        praxis = ""
        clinic = ""
        address = ""
        zipcode = ""
        town = ""
        phone =""
        fax = ""
        email = ""
        website = ""
        longitude = ""
        latitude = ""
        geodata =div["data-jmapping"].split("point: {")[1].split(",")
        lng = geodata[0].replace("lng:","").replace(" ", "")
        lat = geodata[1].replace("lat:","").replace(" ", "").replace("}","")

        div1 = div.find("div", class_="gd-name")
        if div1:
            for keyword in clinic_keywords:
                if keyword in cleanString(div1.strong.text):
                    name =""
                    clinic = cleanString(div1.strong.text)
                    break
                else:
                    name = cleanString(div1.strong.text)
                if "Gemeinschaftspraxis mit:" in div1.text:
                    praxis = cleanString(div1.text.split("\n")[-3]).replace("Gemeinschaftspraxis mit:","")
                if "Krankenhaus:" in div1.text:   
                    clinic =cleanString(div1.text.split("\n")[2]).replace("Krankenhaus:","")
        div1 = div.find("div", class_="gd-adresse")

        if lng+lat+name+clinic in obj:
            continue
        else:
            obj.append(lng+lat+name+clinic)

        if div1:
            address = cleanString(div1.text.split("\n")[1])
            span = div1.find("span", class_="jp-plz")
            if span:
                zipcode = cleanString(span.text)
            town = cleanString(div1.text.split("\n")[-4]).replace(zipcode + " ", "")

        span = div.find("span", "gd-telefon")
        if span:
            phone = cleanString(span.a["href"].replace("tel:", ""))
            
        span = div.find("span", "gd-telefax")
        if span:
            fax = cleanString(span.text.replace("Telefax:", ""))
            #print(fax)  

        a = div.find("a",class_="mail")
        if a :
            mail = a.text
            #print(mail)    

        a = div.find("a", class_="external-link")   
        if a:
            website = a["href"] 
            #print(website)



        data = ""
        data += name
        data += ";"
        data += clinic
        data += ";"
        data += praxis
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
