# Sieber-etal-2026_NCOMMS

Scripts used for the analysis in Sieber et al., 2026: "Climate response to Nature Future scenarios in a regional Earth System Model"

## Scripts for analysis and plotting
1_analysis-LC-climate.ipynb: analysis of land cover differences and climate response.   
Produces Figs. 3-4, parts of Figs. 2 and 5, and Supplementary figures and tables   

2_summary-tables.ipynb: statistics of climate response over Europe and in subregions.   
Produces Supplementary Data 3    

3_sensitivity.ipynb: sensitivity of the climate response to the level of PFT perturbation.   
Produces Fig. 6 and Supplementary Fig. 5   

4_T-decomposition.ipynb: decomposes the surface temperature response into contributions of surface energy balance components.     
Produces Fig. 7 and supplementary Figs. 6-8    

5_PFT-transitions_Ridge.ipynb: decomposes the surface/air temperature response into contributions of land cover transitions.   
Produces Fig. 8 and supplementary Figs. 10-14    
       
## Settings and input data
settings.py: sets the path to input data   
dataset_contents.txt: file overview
dataset_README.txt: dataset description

The dataset can be obtained from the ETH research collection.   

## Helpers
plotting.py: plotting style   
func_calc.py: functions for calculations   
func_plots.py: functions for plotting   
func_stats.py: functions for significance testing   
