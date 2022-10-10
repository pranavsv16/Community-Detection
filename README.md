# Graph Data Mining Project 2 
# Overlapping Community Detection

In this Project, we have implemented the Link Aggregate algorithm (LA) and the Improved Iterative Scan algorithm (IS2), which are presented in the paper "Efficient Identification of Overlapping Communities."

## Environment
This project has been tested on a local environment with Python version 3.8 installed.

## Required packages
`networkx`  
This package can be installed using pip using the command, 
```
pip3 install networkx
```
The other inbuilt python packages used are  
`sys`  
`os`

If installation with pip does not work, the `networkx` package can be installed from [https://pypi.org/project/networkx/#files](https://pypi.org/project/networkx/#files)

## Execution
Download the zip file and then unzip using,
```
unzip overlapping-Community-Detection.zip
cd overlapping-Community-Detection
```
After navigating to this directory, the main.py script can be run using the following command. 
```
python main.py <file_path>
```
In this project, the input files are under the datasets directory.
For example, to use the `youtube.graph.small`, please run the following command,
```
python main.py ./datasets/youtube/youtube.graph.small 
```
After the execution of the script, the final communities will be store in `./output_results` directory.

Note that large graphs can take longer to run.  
The output file will contain communities with all the nodes in one line of output belong to the same community.
The output for `youtube.graph.small` data will be like this,
```
2 10 13 16 18 24 25
267 854 862
260 261 829 1505 1506 1507 1508 1509 1510 1511 1512
187 1398 1399
44 57 58 434
```

## Project Members:
Venkata Pranav Singaraju (pvsingar)  
Samson Reddy Mulkur (smulkur)  
Rakesh Muppala (rmuppal)
