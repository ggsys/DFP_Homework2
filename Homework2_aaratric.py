"""
Created on Sat Sep 11 11:20:16 2021

@author: aaratrikachakraborty
"""
from tabulate import tabulate   #for displaying in a tabular format

#defining the absolute source and destination file paths
source_path = '/Users/aaratrikachakraborty/Documents/DFP/cme.20210903.c.pa2'
dest_path = '/Users/aaratrikachakraborty/Documents/DFP/CL_expirations_and_settlements.txt'

#initializing and declaring the various display metrics globally 
futures_code=""
contract_mon=""
contract_type=""
fut_exp_date=""
opt_code =""
opt_exp_date=""
strike_price=""
settlement_price=""

#initializing and displaying the result lists for displaying Type B and Type 81 records
typeB_Result=[]    # for Type B 
type81_Result=[]    # for Type 81
#opening the source file in read text format
with open(source_path, 'rt', encoding='utf-8') as source:
    contents = source.readlines()    # storing the content read by lines
    #opening the destination file in write-text format 
    with open(dest_path, 'wt', encoding='utf-8') as destination:
        
        #Parsing through the input file line by line
        for record in contents:
            #filtering fand extracting data for Type B CL Future and Option Types
            if((record[:8] == 'B NYMCL ' or record[:8] == 'B NYMLO ') and int(record[18:25]) >= 202110 and int(record[18:25]) <= 202312):
                contract_mon = record[18:22]+"-"+record[22:24]
                #For extracting the Type B Future Contract Type
                if(record[15:18]=="FUT"):
                    futures_code = record[5:7]
                    contract_type = "Fut"
                    fut_exp_date = record[91:95] +"-"+ record[95:97]+"-"+record[97:99]
                #For extracting the Type B Future Option Type
                elif(record[15:18]=="OOF"):
                    futures_code = record[99:101] 
                    contract_type = "Opt"
                    opt_code = record[5:7]
                    opt_exp_date = record[91:95] +"-"+ record[95:97]+"-"+record[97:99]
                #Appending the type B results onto a list of lists    
                typeB_Result.append([futures_code, contract_mon, contract_type, fut_exp_date,opt_code, opt_exp_date])
            #filtering fand extracting data for Type 81 CL Future and Option Types
            elif((record[:8] == '81NYMCL ' or record[:8] == '81NYMLO ') and int(record[29:35]) >= 202110 and int(record[29:35]) <= 202312):
                contract_mon = record[29:33]+"-"+record[33:35]
                #For extracting the Type 81 Future Contract Type
                if(record[25:28]=="FUT"):
                    futures_code = record[5:7]
                    contract_type = "Fut" 
                    settlement_price = int(record[108:122])/100.0
                #For extracting the Type 81 Future Option Type    
                elif(record[25:28]=="OOF"):
                    futures_code = "CL"
                    if(record[28:29]=='C'):
                        contract_type = "Call"
                    elif(record[28:29]=='P'):
                        contract_type = "Put"
                    strike_price = int(record[47:54])/100
                    settlement_price = int(record[108:122])/100.0 
                #Appending the type 81 results onto a list of lists     
                type81_Result.append([futures_code, contract_mon, contract_type, strike_price, settlement_price])
        #writing the first table  of type B records           
        destination.write(tabulate(typeB_Result, headers=['Futures\nCode','Contract\nMonth','Contract\nType','Futures\nExp Date',
                            'Options\nCode','Options\nExp Date'],floatfmt="0.2f"))
        
        destination.write("\n")
        #writing the second table of type 81 records
        destination.write(tabulate(type81_Result, headers=['Futures\nCode','Contract\nMonth','Contract\nType','Strike\nprice',
                                'Settlement\nPrice'])) 
        #print(len(type81_Result)+len(typeB_Result))
        #total number of lines of text in output file = 13381
