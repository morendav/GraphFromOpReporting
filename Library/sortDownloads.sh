#!/bin/bash
#######################################
### Sort folder and save elsewhere
#
# Options:
#       -f  dirctory of hte downloads folder containing the latest operations repors
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
[ -z "$downloadsDirectory" ] && { echo "option -f is empty. Exit on error"; exit;}
[ -z "$date" ] && { echo "option -d is empty. Exit on error"; exit;}


### Direcotry Ops
curDir=$(pwd)
ProdDir="$curDir/examples"
outFolder="$ProdDir/SortedReports"
type1folder="$outFolder/type1"
type2folder="$outFolder/type2"


### Copy downloaded files as dated files in the correct direcotries for reporting
cp "$downloadsDirectory/type1.txt" "$type1folder/$date.txt"
cp "$downloadsDirectory/type2.txt" "$type2folder/$date.txt"

rm -r $downloadsDirectory
mkdir $downloadsDirectory
echo "files sorted into working directory"
