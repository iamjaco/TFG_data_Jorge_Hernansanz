library(KEGGREST)
library(data.table)
library(readr)
library(readr)

Drug_list <- keggList('drug') # Gets a vector of all the drugs in KEGG.
tail(drugSS, n=1)
length(Drug_list)             # We have a total of 11255 drugs. It is also countered the different brands

Drug_list <- as.data.frame(Drug_list)
setDT(Drug_list, keep.rownames = TRUE)[] 
#We are interested in the code name. The name of the new column remains as 'rn'.
#In the most updated version, there last identifier is D11818.

#Small example to test the extraction of interaction
example <- keggGet(c('dr:D00678','dr:D00097'))
names(example[[2]])
View(example[[2]]$INTERACTION)
names(example[[2]])
aa <- setdiff(vector_of_number,Drug_list$rn)
#####################################################################################



list_of_possible_identifers <- sprintf("dr:D%05d", 1:11818) #Check this number at Drug_list
#KEGG identifiers follow a schema like dr:00001, dr:00002..., in a linear way and in some cases there can be
#a jump of more than 1 unit, like dr:D00052, dr:D00054. Then, we select the last identifier of the list, and
#will try to find all the identifiers that can be found in that vector

list_of_identifiers <- setdiff(list_of_possible_identifers, setdiff(list_of_possible_identifers,Drug_list$rn))
    # setdiff(vector_of_number,Drug_list$rn) returns the identifiers that are not in the drug list of KEGG
    # setdiff(vector_of_number, setdiff(vector_of_number,Drug_list$rn)) returns the drugs that only appears in the kegg list.

remove <- c('dr:D01209','dr:D01331','dr:D10246','dr:D11444')  #These give error at KEGG website
list_of_identifiers <- list_of_identifiers[!list_of_identifiers %in% remove] #Remove them from the list of identifiers.


#Code to extract interactions
for (i in list_of_possible_identifers){
  if(i %in% list_of_identifiers){
    KEGG_drug <- keggGet(i)
    if ("INTERACTION" %in% names(KEGG_drug[[1]])){                  #If there is interaction for that drug annotate it.
      print(i)
      reader <- read_delim(sprintf("http://rest.kegg.jp/ddi/%s",i), #Read the website file. If error check KEGG rest for the identifier. If error at API, add to remove variable
                         "\t", col_names = FALSE)
      DDI <- reader[grepl('dr:',reader$X2),]                        #Annotate the real DDI
      no_DDI <- reader[!grepl('dr:',reader$X2),]                    #Annotate fake DDI (Appears at DDI search but doesn't have a relation dr: - dr:)
      write_delim(DDI,"DDIs/KEEG_DDI.txt","\t", col_names = FALSE, append = TRUE)
      write_delim(no_DDI,"DDIs/KEGG_no_DDI.txt","\t", col_names = FALSE, append = TRUE)
      } else{
      print('No interaction')                                       #If the identifier exists but there is no interaction for it.
    }
  } else{
    print('nothing')                                                #If the identifier doesn't exist.
  }
  
}


#DIFFERENT MOLECULES <- c('cpd:','ev:')


