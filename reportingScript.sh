#!/bin/bash
#######################################
### Sort folder and save elsewhere
#
# Options:
#       -f  dirctory of hte downloads folder containing the latest operations reports
#       -d  date of the reports were generated (email timestamp)
#
#######################################
###     CodeBlock: InitVar
#######################################
### Argument Operations
# For Help Option
while getopts ":h:f:d:" opt; do
  case ${opt} in
    h )
      printf "\nusage: sortDownloads.sh -f [downloads directory folder] -d [date formatted mmddam or mmddpm]
      Search Options:
        -f    Directory of the downloads folder containing the Operations reports
        -d    Date to use in labeling the files currently in the downloads folder"
        exit 0
        ;;
    f ) downloadsDirectory=$OPTARG;;
    d ) date=$OPTARG;;
   \? )
     echo "Invalid Option: -$OPTARG. Use Option -help for more information" 1>&2
     exit 1
     ;;
  esac
done
### Error exits with no directory or search term inputs
[ -z "$date" ] && { echo "option -d is empty. Exit on error"; exit;}
[ -z "$downloadsDirectory" ] && { echo "option -f is empty. Exit on error"; exit;}

### Direcotry Ops
curDir=$(pwd)
exampleData="$curDir/examples"
sortedData="$exampleData/SortedReports"
libraryDir="$curDir/Library"
type1="$sortedData/type1/"
type2="$sortedData/type2/"

[ "$(ls -A $downloadsDirectory)" ] && $libraryDir/sortDownloads.sh -f $downloadsDirectory -d $date || echo "Empty Download folder, skipping sort script."

python3 $libraryDir/graphDataFiles.py -i $type1 -f 'row' -s 'person' -t 'Persons Reported in Type 1;Date(mmdd);Occurence'
python3 $libraryDir/graphDataFiles.py -i $type2 -f 'column' -s 'cn' -t 'Persons Reported in Type 2;Date(mmdd);Occurence'
