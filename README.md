# DS5110 Final Project - HVAC 
### Bini Chandra, Brian West, Cody Snow

## The GOAL

The goal of this project is to find out which Terminal Units (TUs) are connected to which Rooftop Units (RTUs) in a building, using data science techniques.

We are given:

   - 3 RTU files (only 2 are connected to TUs)

   - 47 TU files (labeled by letters like A.csv, AA.csv, B.csv, etc.)


##  Work in progress

- /DataExploration_BW.py - Initial exploration of the data to determine viability of clustering, correlation, etc.
- /data/terminalDescription.txt examines measures of central tendancy of the features we'll be studying

### Data files created so far
- data/terminalUnitsCleaned/*.csv – Cleaned TU files (after forward-filling and column dropping)
- data/correlation/*.csv – Correlation files for each TU vs RTUs
- data/TU_RTU_Correlation_Heatmap.png – Heatmap visualizing average correlation between each TU and all 3 RTUs
- /data/terminalDistinctValues.csv
- /data/terminalUnitsCleaned.csv
- /data/terminalUnitsRawData.csv

### Data Directory - Folders containing client data

- /data/roofTopUnits
- /data/terminalUnits

## Important notes about the datasets from the client

- This is a customer building with multiple roof top units but only 2 of them are connected to terminal units. I included data for the 2 that are connected to terminal units and one that is not.  
- There are 47 terminal units in the building. Each of them is connected to one of the two RTUs (not evenly split). I feel like this should give a fair amount of data to build off of and then test. 
- At first I will not give insights into which units are connected but will as we go along to help validate findings.

- I do see a lot of missing setpoints. I think for your analysis on setpoints you can forward fill them as they are fairly static (we can’t ffill sensors)
- The other thing to note is EffSp is the effective setpoint.  This is basically telling you the current setpoint regardless of occupancy or mode.  So, it the machine has it this is the most important but not every machine has it.
