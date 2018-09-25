# Graphing Iteratively Over Time - From OPs Report Files

Bash shell script & python script that
1) take in set (1+) files in a downloads folder (parameterized)
2) sort the files into respective 'types' (hard coded)
3) build report from past data + new data, graph and save the graphData

Used to read from a common ops report location, graph relevant persons counts in certain populations, graph and export graph data to a slack channel for ops monitoring.


## Getting Started

There are 2 support scripts (located in the library folder), and 1 main script that runs the support scripts.
The ./example folder contains an example of the common reporting directory that was used in production containing a daily reproduced report of as set of operations.

To deploy this script, modify the reportingScript.sh shell script in the following locations:

Update to reflect the deployment directories (ie example data = the common reporting directory, sortedData = the feed data for graphing, sorted by date for internal use, type1 = sorted type1 data directory for internal use, etc)
```
### Direcotry Ops
curDir=$(pwd)
exampleData="$curDir/examples"
sortedData="$exampleData/SortedReports"
libraryDir="$curDir/Library"
type1="$sortedData/type1/"
type2="$sortedData/type2/"
```

Update to reflect the type of operations being reported; paramter -t is the 'Title,XAxis,YAxis' respectively. -i input sorted directory (i.e sorted/type1, sorted/type2), -f is data format. Row would be like an LDIF file, where multiple rows might represent different attributes of teh same object (a single user). Column being like excel, where each attribute is separated by column for a single object.
>> For more info refer to the documentation in the py file in library
```
python3 $libraryDir/graphDataFiles.py -i $type1 -f 'row' -s 'person' -t 'Persons Reported in Type 1;Date(mmdd);Occurence'
python3 $libraryDir/graphDataFiles.py -i $type2 -f 'column' -s 'cn' -t 'Persons Reported in Type 2;Date(mmdd);Occurence'
```


### Options & Parameters

Run the reportingScript.sh shell script with the following paramters:

> -f              dirctory of the downloads folder containing the latest operations reports

> -d              date of the reports were generated (email timestamp)

> -help           Utility help and usage info


### Example: Using the provided examples

Run the rerportingScript.sh shell script from the command line like follows:

> ./reportingScript.sh -f 'examples/dn/' -d '0910am'

where -d '0910am' would plot the last point for data recorded on Sept 10, in the morning.

./examples/dn/ is representative of a shared reporting directory where some external process is producing a report at some regularly scheduled cadence.

therefore this parameter may be hard coded in a scheduled deployment where the only dynamic parameter would then be the time and its format (e.g. 0910am in this example)



### Prerequisites

Python 3 Modules:
  + os
  + json
  + re
  + sys
  + time
  + argparse


## Releases
### Version 1.1
    - functional and tested with large data set
    - first push to repo
    - updated example data sets
