import xml.etree.ElementTree as ET
import re
import os, sys 
import time
start = time.process_time()


Terminologies = open("C:\\Users\\Jorge_TEMP\\Desktop\\Thesis_Bibliography\\DDI_datasets\\NDF-RT\\NDFRT_2014_07_07.txt","r+") # Will be used to map normal drug names to identifiers
DDI_dataframe = open("C:\\Users\\Jorge_TEMP\\Desktop\\Thesis_Bibliography\\DDI_datasets\\NDF-RT\\NDFRT_DDI","w") 

tree = ET.parse("C:\\Users\\Jorge_TEMP\\Desktop\\Thesis_Bibliography\\DDI_datasets\\NDF-RT\\NDFRT_Public_2014.07.07_TDE.xml") #Used to read the xml file of NDF-RT
root = tree.getroot()

#Columns that will store dataframe, and another releveant information
Triple_DDI = 0
Tetra_DDI = 0
Mapped_drugs = 0
Not_mapped_drugs = []
Not_well_parsed_drugs = []


count = 0  #Will count the number of interactions
for line in root.iter('conceptDef'):
    if line.find('./properties/property/value').text == 'Significant' or line.find('./properties/property/value').text == 'Critical':   #Identifies the rows that are DDI
        name = line.findall('./properties/property/value')      #Name is used to find the drug pair 
        for i in name:
            if '/' in i.text:               # Detects the interaction string
                #print(i.text)
                i = str(i.text)                  # Needed so as re.split receives a normal string
                names_pair = re.split(r'[/]',i)  # Will obtain the diferrent drugs, as the pair is separated by an '/'.
                #print(names)
                break
       
        value = line.find('./properties/property/value').text   #Value return the consition of the DDI; Significant or Critical
        #print(value)

        if len(names_pair) == 2:             # Making sure that we just are defining JUST two drugs with ONE condition

        # The below commented chunck of code 'fixes' the exceptions mentioned at the bottom part of this file
            # for i in range(len(names_pair)):
            #     if names_pair[i] == 'HYPERICUM PERFORATUM':
            #         names_pair[i] == 'HYPERICUM PERFORATUM (ST. JOHNS WORT)'
            #     if names_pair[i] == 'MAGNESIUM ACETATE':
            #         names_pair[i] == 'MAGNESIUM ACETATE TETRAHYDRATE'
            #print(names_pair)
            
            D1 = False
            D2 = False
            Terminologies.seek(0)                     # Always starting to read from line 0 ()
            for line in Terminologies.readlines():      # This loop accounts for searching the identifiers of drugs
                line = re.split("\t",line)              # Separate different components and obtain a list 
                         
                if line[1].rstrip() == names_pair[0]: # Changing first drug
                    Drug_1 = names_pair[0]
                    names_pair[0] = line[0]
                    D1 = True
                    #print(line[0])
                if line[1].rstrip() == names_pair[1]: # Changing second drug
                    Drug_2 = names_pair[1]
                    names_pair[1] = line[0]
                    D2 = True
                    #print(line[0])
                if D1 == True and D2 ==True:          # If the two drugs are mapped to an identifier
                    Mapped_drugs +=1
                    print(Mapped_drugs)
                    DDI_dataframe.write(Drug_1 + '\t' + names_pair[0] + '\t' + Drug_2 + '\t' + names_pair[1] + '\t'+ value + '\n')
                    break  
            if D1 == False or D2 == False:            # If tricky drug name or missing identifier 
                Not_mapped_drugs.append(names_pair)

        elif len(names_pair) == 3:       # Checking if we face three drugs in an interaction
            Triple_DDI += 1
        elif len(names_pair) == 4:       # The same but with four.
            Tetra_DDI += 1
        else:
            Not_well_parsed_drugs.append(i)
        count += 1
        #break

Terminologies.close()
DDI_dataframe.close()


print("There are {} drug interactions".format(count))
print("I have mapped {} DDIs with their identifiers".format(Mapped_drugs))

print("There are {} triple drug inteactions".format(Triple_DDI))
print("There are {} tetra drug inteactions".format(Tetra_DDI))

if len(Not_well_parsed_drugs) == 0:
    print("All drugs localized")
else:
    print("There is still some rugs not identified")

print(Not_mapped_drugs)

print(time.process_time() - start)    #Time used to do the loop # 22 minutes



'''
At the moment, two special cases
    - HYPERICUM PERFORATUM
    - MAGNESIUM ACETATE

It has to be revised by the supervisors if what is proposed below is correct:
    - The first one will take the same identifier as HYPERICUM PERFORATUM (ST JOHN'S WORT). 13 Cases
    - MAGNESIUM ACETATE takes the same identifier than MAGNESIUM ACETATE TETRAHYDRATE. 1 Case
'''   