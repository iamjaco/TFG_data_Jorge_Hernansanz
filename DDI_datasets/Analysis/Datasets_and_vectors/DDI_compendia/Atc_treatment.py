import sys
cont = 0
vector_DDI = open(sys.argv[1],"w")
with open(sys.argv[2],"r+") as ATC:
    for pair in ATC.readlines():
        pair_list = pair.split(',')
        pair_list[1] = pair_list[1].strip()
        print(pair_list)
        if pair_list[0] > pair_list[1]:
            pair_join = pair_list[1] + '_' + pair_list[0]
        else:
            pair_join = pair_list[0]+ '_' + pair_list[1]
        pair_join = pair_join.replace('"','')
        vector_DDI.write(pair_join +'\n')
        print(cont)
        cont +=1
#Then use unique() in R and save the filtered vector. It is already done at 'Code_for_upsetR.Rmd'.
