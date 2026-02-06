This file was generated on 2026-02-06 by Petra Sieber

Sieber et al. 2026 - Climate response to Nature Future scenarios in a regional Earth System Model

---------------
AUTHOR
---------------

Name: Petra Sieber
ORCID: https://orcid.org/0000-0003-2626-9502
Institution: ETH Zurich
Address: Universitätstrasse 16, CH-8092 Zürich
Email: petra.sieber@env.ethz.ch

---------------
DATA DESCRIPTION
---------------

This repository contains post-processed output of the regional Earth System Model COSMO-CLM2 (CCLM2) run over the EURO-CORDEX domain at 12.5 km resolution (EUR11).
The data is used for analyses in the manuscript "Climate response to Nature Future scenarios in a regional Earth System Model".

The code used to analyse the data and create figues is also available from github: 

The dataset is organised as follows:

The directory "15years" includes land cover (surf.nc) and climate information (see below) for:
- cclm2_EUR11_FB_ssp1: land cover and simulated climate 2036-2050 under the reference (SSP1)
- cclm2_EUR11_FB_nfn: land cover and simulated climate 2036-2050 under the Nature for Nature (NfN) scenario
- cclm2_EUR11_FB_nfs: land cover and simulated climate 2036-2050 under the Nature for Society (NfS) scenario
- cclm2_EUR11_FB_nac: land cover and simulated climate 2036-2050 under the Nature as Culture (NaC) scenario
- cclm2_EUR11_FB_2015: land cover in 2015 (CLM5 surface dataset produced with our methods)
- cclm2_EUR11_FB_hist: historical land cover (CLM5 original surface dataset) and simulated climate 2011-2015

Climate information includes:
- Climatology (2036-2050 mean) of annual/seasonal climate variables
    cclm2_annual-climatology.nc
    cosmo_T2m-max-climatology.nc
    cclm2_seasonal-climatology.nc
- Timeseries (2036-2050) of annual/seasonal climate variables
    cclm2_annual-series.nc
    cosmo_T2m-max-series.nc
    cclm2_seasonal-series.nc
- Significant differences (1 for P<0.05) relative to SSP1 (for scenarios) or recent historical conditions (for reference)
    cclm2_annual-sig-change.nc
    cclm2_T2m-max-sig-change.nc
    cclm2_seasonal-sig-change.nc
    cclm2_seasonal-drivers-sig-change.nc

The directory "luc_evaluation" includes the land cover composition at 3 levels:
- EUNIS habitats (EUNIS_scenarios_4reg.nc)
- Land systems (Dou-et-al_scenarios_4reg.nc)
- PFTs (PFT_scenarios_4reg.nc)


---------------
FILE OVERVIEW
---------------

data_ETH-research-collection
    └── data.zip  (13.6 GB)
    📁 15years
        ├── eunis_mask_repr.nc  (3.3 MB)
        ├── regionmask_2D_Dou.nc  (3.3 MB)
        └── regionmask_3D_Dou.nc  (1.6 MB)
        📁 cclm2_EUR11_FB_2015
            └── surf.nc  (3.5 GB)
        📁 cclm2_EUR11_FB_hist
            ├── cclm2_annual-climatology.nc  (78.0 MB)
            ├── cclm2_annual-series.nc  (780.1 MB)
            ├── cclm2_seasonal-climatology.nc  (312.1 MB)
            ├── cclm2_seasonal-series.nc  (1.7 GB)
            ├── cosmo_T2m-max-climatology.nc  (1.6 MB)
            ├── cosmo_T2m-max-series.nc  (16.3 MB)
            └── surf.nc  (3.5 GB)
        📁 cclm2_EUR11_FB_nac
            ├── cclm2_T2m-max-sig-change.nc  (3.3 MB)
            ├── cclm2_annual-climatology.nc  (78.0 MB)
            ├── cclm2_annual-series.nc  (1.1 GB)
            ├── cclm2_annual-sig-change.nc  (6.5 MB)
            ├── cclm2_seasonal-climatology.nc  (312.1 MB)
            ├── cclm2_seasonal-drivers-sig-change.nc  (65.0 MB)
            ├── cclm2_seasonal-series.nc  (2.5 GB)
            ├── cclm2_seasonal-sig-change.nc  (65.0 MB)
            ├── cosmo_T2m-max-climatology.nc  (1.6 MB)
            ├── cosmo_T2m-max-series.nc  (24.4 MB)
            └── surf.nc  (3.5 GB)
        📁 cclm2_EUR11_FB_nfn
            ├── cclm2_T2m-max-sig-change.nc  (3.3 MB)
            ├── cclm2_annual-climatology.nc  (78.0 MB)
            ├── cclm2_annual-series.nc  (1.1 GB)
            ├── cclm2_annual-sig-change.nc  (6.5 MB)
            ├── cclm2_seasonal-climatology.nc  (312.1 MB)
            ├── cclm2_seasonal-drivers-sig-change.nc  (65.0 MB)
            ├── cclm2_seasonal-series.nc  (2.5 GB)
            ├── cclm2_seasonal-sig-change.nc  (65.0 MB)
            ├── cosmo_T2m-max-climatology.nc  (1.6 MB)
            ├── cosmo_T2m-max-series.nc  (24.4 MB)
            └── surf.nc  (3.5 GB)
        📁 cclm2_EUR11_FB_nfs
            ├── cclm2_T2m-max-sig-change.nc  (3.3 MB)
            ├── cclm2_annual-climatology.nc  (78.0 MB)
            ├── cclm2_annual-series.nc  (1.1 GB)
            ├── cclm2_annual-sig-change.nc  (6.5 MB)
            ├── cclm2_seasonal-climatology.nc  (312.1 MB)
            ├── cclm2_seasonal-drivers-sig-change.nc  (65.0 MB)
            ├── cclm2_seasonal-series.nc  (2.5 GB)
            ├── cclm2_seasonal-sig-change.nc  (65.0 MB)
            ├── cosmo_T2m-max-climatology.nc  (1.6 MB)
            ├── cosmo_T2m-max-series.nc  (24.4 MB)
            └── surf.nc  (3.5 GB)
        📁 cclm2_EUR11_FB_ssp1
            ├── cclm2_T2m-max-sig-change.nc  (3.3 MB)
            ├── cclm2_annual-climatology.nc  (78.0 MB)
            ├── cclm2_annual-series.nc  (1.1 GB)
            ├── cclm2_annual-sig-change.nc  (6.5 MB)
            ├── cclm2_seasonal-climatology.nc  (312.1 MB)
            ├── cclm2_seasonal-drivers-sig-change.nc  (65.0 MB)
            ├── cclm2_seasonal-series.nc  (2.5 GB)
            ├── cclm2_seasonal-sig-change.nc  (65.0 MB)
            ├── cosmo_T2m-max-climatology.nc  (1.6 MB)
            ├── cosmo_T2m-max-series.nc  (24.4 MB)
            └── surf.nc  (3.5 GB)
    📁 luc_evaluation
        ├── Dou-et-al_scenarios_4reg.nc  (13.4 KB)
        ├── EUNIS_scenarios_4reg.nc  (13.8 KB)
        └── PFT_scenarios_4reg.nc  (14.2 KB)

Summary of unzipped files:
  Total files: 58
  Total size:  41 GB
