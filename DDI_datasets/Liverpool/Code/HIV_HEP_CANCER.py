from bs4 import BeautifulSoup
import re
import requests
import urllib.request, urllib.parse, urllib.error
import pandas as pd

DATABASES = ['hiv','hep','cancer']
#
#
#
#
for db in DATABASES:
#
# 
# 
#  
    URL = "https://www.{}-druginteractions.org/view_all_interactions/new".format(db)
    content_principal = requests.get(URL).text
    html_principal_source = BeautifulSoup(content_principal, "html.parser")
    #
    #
    #
    #
    list_of_numbers = []
    list_of_names = []
    all_numbers = html_principal_source.find_all("input", class_='check_boxes optional')
    all_names = html_principal_source.find_all("span", class_="checkbox")
    #
    #
    #
    #
    for value in all_numbers:
        list_of_numbers.append(value['value'])
    for value in all_names:
        value = value.get_text()
        value = value.replace("/","_")
        list_of_names.append(value)
    #
    #
    #
    #
    for i in range(len(list_of_numbers)):
        #
        #
        #
        #
        list_drug_1 = []
        list_drug_2 = []
        list_of_level_of_interaction = []
        list_of_quality_of_interaction = []
        list_of_summary = []
        list_of_description = []
        #
        #
        #
        #
        URL = "https://www.{}-druginteractions.org/interactions/{}/all".format(db,list_of_numbers[i])
        content_sec = requests.get(URL).text
        #
        #
        #
        #
        html_source_all = BeautifulSoup(content_sec, "html.parser")
        html_source_all = html_source_all.find_all('div', class_='interaction-table-modal')
        for html_source in html_source_all:
            #
            #
            #
            #
            level_int = html_source.find('p', {'class' : 'interaction-block-header'})
            #
            Qlty_evi = html_source.find('strong', text='Quality of Evidence:')          #Some drugs do not have confidence value. Should record for later
            Has_confidence_Score = False
            if Qlty_evi != None:
                Qlty_evi = Qlty_evi.next_sibling
                Has_confidence_Score = True
            #
            string3 = html_source.find('div', class_="interaction-block-inner").find_all('p')
            #
            string_4_5 = html_source.find_all('div',class_="interaction-info-divide")
            #
            #
            #
            #
            level_int = re.sub(r'[\ \n]{2,}',"",level_int.text)
            list_of_level_of_interaction.append(level_int)
            #
            if Has_confidence_Score:
                Qlty_evi = re.sub(r'[\ \n]{2,}',"",Qlty_evi)
                list_of_quality_of_interaction.append(Qlty_evi)
            else:
                list_of_quality_of_interaction.append("NA")
            #
            interaction_pair = []
            for drug in string3:
                drug = drug.get_text()
                drug = re.sub(r'[\ \n]{2,}',"",drug)
                interaction_pair.append(drug)
            list_drug_1.append(interaction_pair[0])
            list_drug_2.append(interaction_pair[1])
            print("Interaction between {} and {}".format(interaction_pair[0],interaction_pair[1]))
            #
            Summary_and_description = []
            for value in string_4_5:                   #Doing like this as getting error with 'div.strog.p'. Must find a better way.
                value = value.text.replace("\n","")
                Summary_and_description.append(value)
            list_of_summary.append(Summary_and_description[1])
            list_of_description.append(Summary_and_description[2])
            #
            #
            #
            #
            
            # print(len(list_drug_1))
            # print(len(list_drug_2))
            # print(len(list_of_level_of_interaction))
            # print(len(list_of_quality_of_interaction))
            # print(len(list_of_summary))
            # print(len(list_of_description)) 

        dictionary_data_frame = {'Drug_1':list_drug_1,'drug2':list_drug_2, 'Level_of_interaction':list_of_level_of_interaction,
        'Quality_of_interaction':list_of_quality_of_interaction, 'Summary':list_of_summary, 'Description':list_of_description}

        dat = pd.DataFrame(dictionary_data_frame)
        print(dat)
        dat.to_csv("C:\\Users\\Jorge_TEMP\\Desktop\\Thesis_Bibliography\\DDI_datasets\\{}\\DDI_dataframes\\{}_DDIs.csv".format(db,list_of_names[i]))