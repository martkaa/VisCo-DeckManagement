# Deck Management Program
This program is a solution to the problem Deck Management of Cargos, which myself and Vetle Chyba Nordstad worked on summer 2021 on behalf of VisCo. The essence of the problem is to place as many cargos to as optimal locations as possible. 

---
## Input and output
The solution has taken form as an independent program which consistes of two files: `dataHand.py`and `placer.py`. `dataHand.py` takes two Excel sheets as input. One containing information about Cargo which are to be loaded on to the platform, and one containing information about LDAs. The program's output is an Excel sheet containing information about placement of each cargo on the platform. 

Examples of input sheets are: 
1. `Temps to be loaded onto ARGOS.xlsx`
2. `LDAs_05m_units.xlsx`

The program is based on the structure of these files, so it is importans that the input files containes the same columns as these sheets.

The output file of results can be ajusted after the users wish, but for now it contains the same information on the cargos as the input file, in addition to the cargo's coordinates onto the LDA.

## How the program works

The program is based on criterias displayed in the diagram `flow_chart_5_phases`. This given to us as a guideline of what the program should take in consideration when placing a cargo on to a LDA.

The placer algorithm and core of the program is called `placeCargosSingleLDA()`. As the name says, the function takes one LDA and a list of several cargos as input. As the 5 phases implies the algorithm has several if-statements that checks if the criteria of placement of the cargo is fulfilled. The algorithm is visualized in the diagram `flowchart_program`.

The program consists of several functions that are stacked to achieve the users desired results. These are marked with arrows in the flowchart.

---
### How to run the program

The program is object oriented and is written in Python with the Anaconda Navigator. To run the program, one need to have either python installed with pip, conda and numpy, or run it from the Anaconda Navigator. 

`dataHand.py` needs correct path to input files in line 70 and 72 using Windows, or 85 and 87 using OS X. 

One first need to run `dataHand.py` to convert input files to objects, and then run `placer.py` to recieve the result file. One can ajust the output filename in the function `writeLocationToFile()` in `placer.py`. 