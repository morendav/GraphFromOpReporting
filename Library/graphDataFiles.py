#######################################
# Graph Data Files
# Date: Aug 2018
# Options:
#       -i  input directory storing files that are to be plotted
#       -f  Data format: row or column format is accepted
#       -s  search term to be searched for in the intake directory
#       -t  graph labels formatted: 'title;xlabel;ylabel'
#
#######################################
#######################################
###     CodeBlock: Modules &  Init Var
#######################################
import os, re, time
from argparse import ArgumentParser

### Read passed arguements from the command line
parser = ArgumentParser()
parser.add_argument("-i", "--inputDir", dest="inDir", help="Directory location of date titled data files.", metavar="DIRECTORY", type=str)
parser.add_argument("-f", "--DataFormat", dest="format", help="the format of the input data passed in the input directory. Accepted Values: 'row' or 'column'", metavar="FORMAT", type=str)
parser.add_argument("-s", "--searchTerm", dest="strm", help="The header term identifying the data that we wish to plot, only required if data is row oriented and has a header", metavar="STRING", type=str)
parser.add_argument("-t", "--PlotTitle", dest="labels", help="The chart title for the plot, x and y labels respectively. Should be either empty or non empty and 3 values delimited by the ';' character. Example: 'Title;XLabel;YLabel' ", metavar="STRING", type=str)
args = parser.parse_args()
inputDirectory=args.inDir
searchTerms=args.strm
subTitles=args.labels
format=args.format

### Checks on passed arguments
# If inputDirectory is not passed then exit on critical error
if inputDirectory is None or (format is "row" and searchTerms is None):
    print("\nOption missing from call, use option -h for help. \nExit on Error.\n")
    exit()
if subTitles is None :
    subTitles = ["","",""]
else:
    subTitles=subTitles.split(";")

### Init Variables
currentDirectory = os.getcwd() + '/'
os.chdir(inputDirectory)
listOfFiles=os.listdir()                # find all files in input directory
dataDict={}                             # data dictionary initialization
searchTermsList=[]
Title = searchTerms +  ", " + subTitles[0]   # chart title concat

### if all checks pass, import matlab plot module
import matplotlib.pyplot as plt

#######################################
###     CodeBlock: define fucntions
#######################################
### Intake File parser equation - column format data, example: Excel file with column header
def rowDataIntake (fileObj,searchAtt,delim):
    ### Function (open_File_Object, Search Attribute)
    ###     takes in the open file object,
    ###     if iteration is first then find index in header of the search Attribute
    ###     Then take that index, and build output dataset of index for each row in file object
    it=1
    output=[]
    for line in fileObj:
        line=(line.strip("\n")).split(delim)
        ### only run on the first iteration through the intake file, match index to header for search attribute in config
        if it ==1:
            ind=line.index(searchAtt)
            it=0
            continue
        output.append(line[ind])
    return output
### Intake File parser equations - row format data
def columnDataIntake (fileObj,searchAtt,delim):
    ### Function (open_File_Object, Search Attribute)
    ###     takes in the open file object,
    ###     proceeds through intake file, if current line begins with the regex = search term then append to output array
    ###         File examples: LDIF files
    output=[]
    for line in fileObj:
        if re.search(searchAtt,line):
            line=(line.strip("\n")).split(delim)
            output.append(line[1]) ### Assumption: the data is always seperated by carriage return, and the second string is the value we want
    return output

#######################################
###     CodeBlock: For each file in list, strip date and count data
#######################################
for file in sorted(listOfFiles):            # sort before iterating on date, ascending
    if re.match(r'^\.', file):
        continue
    else:
        with open (file, 'r') as openFileObj:
            ### Assumes the files are named by date, with index 0 = date, and index 1 = file format (e.g. 0901.txt)
            dateString=file.split(".")[0]
            ### Dependings on format of data read the file and parse it accordingly
            if format in ('row'):
                searchTermsList=rowDataIntake(openFileObj, searchTerms, ",")
            elif format in ('column'):
                searchTermsList=columnDataIntake (openFileObj,searchTerms,"=")
            else:
                print("\nNo Format match, exit on error. Use -h for help using utility")
                exit()
            # print("Completed processing data for file " + file)
            dataDict[dateString]=[len(searchTermsList)]

#######################################
###     CodeBlock: prepare arrays and plot
#######################################
x_datesArray  = list(dataDict) #x value, date range
y_dataArray = list(dataDict.values()) #y value, data to plot

plt.scatter(x_datesArray, y_dataArray)
plt.suptitle(Title)
plt.xlabel(subTitles[1])
plt.xticks(rotation=90)
plt.ylabel(subTitles[2])
plt.savefig(currentDirectory + subTitles[0] + '.png',bbox_inches='tight')
# plt.show()
time.sleep(0.5)
print('completed with intake' + inputDirectory)
