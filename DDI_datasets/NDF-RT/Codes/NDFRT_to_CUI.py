#Mapping CUI identifiers to NDF-RT identifiers
import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

#Used to create the dataframe of mappings
NDFRT_and_CUI = {}
NDFRT_and_CUI['NDFRT'] = []
NDFRT_and_CUI['CUI'] = []


index = open("C:\\Users\\Jorge_TEMP\\Desktop\\Thesis_Bibliography\\DDI_datasets\\NDF-RT\\Codes\\NDFRT_drug_list.txt","r")
for drug in index.readlines():
    URL = "http://bioportal.bioontology.org/ontologies/NDFRT?p=classes&conceptid={}".format(drug.rstrip())      #Using rstrip() to eliminate \n character
    html_content = requests.get(URL).text                                                                       #Accessing source code of html
    html_to_bs4 = BeautifulSoup(html_content,"html.parser")                                                     #Transform code to be readable by beautifulsoup

    node = html_to_bs4.find_all("tr")
    find_p = False
    for i in node:
        subnode = i.find_all("td")
        for j in subnode:
            if find_p:
                print(j.get_text())
                CUI = j.get_text()
                break
            if j.get_text() == "cui":
                print(j.get_text())
                find_p = True
        if find_p:
            break
            
    NDFRT_and_CUI['NDFRT'].append(drug)
    NDFRT_and_CUI['CUI'].append(CUI)


dataframe = pd.DataFrame(NDFRT_and_CUI)
dataframe.to_csv("C:\\Users\\Jorge_TEMP\\Desktop\\Thesis_Bibliography\\DDI_datasets\\NDF-RT\\Principal_data\\Mappings_NDFRT_CUI.csv")
print(dataframe)
        
'''
Structure to be found:

For the case of N0000147688

<tr>
<td nowrap=''>cui</td>
<td>
<p>C0000946</p>
</td>
</tr>
'''