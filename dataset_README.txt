This file was generated on 2026-02-06 by Petra Sieber

Sieber et al. 2026 - Climate response to Nature Future scenarios in a regional Earth System Model

Dataset DOI: https://doi.org/10.3929/ethz-c-000795598

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

This dataset contains post-processed output of the regional Earth System Model COSMO-CLM2 (CCLM2) run over the EURO-CORDEX domain at 12.5 km resolution (EUR11).
The data is used for analyses in the manuscript "Climate response to Nature Future scenarios in a regional Earth System Model".

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
CODE
---------------

The code used to analyse the data and create figues is available from github: https://github.com/pesieber/Sieber-etal-2026_NCOMMS.git,
published under https://doi.org/10.5281/zenodo.18511015.


---------------
FILE OVERVIEW
---------------

data_ETH-research-collection
    └── data.zip  (12.0 GB)
    📁 15years
        ├── eunis_mask_repr.nc  (27.2 KB)
        ├── regionmask_2D_Dou.nc  (29.0 KB)
        └── regionmask_3D_Dou.nc  (25.6 KB)
        📁 cclm2_EUR11_FB_2015
            └── surf.nc  (736.4 MB)
        📁 cclm2_EUR11_FB_hist
            ├── cclm2_annual-climatology.nc  (35.3 MB)
            ├── cclm2_annual-series.nc  (351.2 MB)
            ├── cclm2_seasonal-climatology.nc  (138.5 MB)
            ├── cclm2_seasonal-series.nc  (648.7 MB)
            ├── cosmo_T2m-max-climatology.nc  (763.3 KB)
            ├── cosmo_T2m-max-series.nc  (6.5 MB)
            └── surf.nc  (725.2 MB)
        📁 cclm2_EUR11_FB_nac
            ├── cclm2_T2m-max-sig-change.nc  (29.7 KB)
            ├── cclm2_annual-climatology.nc  (35.4 MB)
            ├── cclm2_annual-series.nc  (526.7 MB)
            ├── cclm2_annual-sig-change.nc  (110.7 KB)
            ├── cclm2_seasonal-climatology.nc  (140.6 MB)
            ├── cclm2_seasonal-drivers-sig-change.nc  (424.3 KB)
            ├── cclm2_seasonal-series.nc  (966.4 MB)
            ├── cclm2_seasonal-sig-change.nc  (428.8 KB)
            ├── cosmo_T2m-max-climatology.nc  (775.0 KB)
            ├── cosmo_T2m-max-series.nc  (9.7 MB)
            └── surf.nc  (737.0 MB)
        📁 cclm2_EUR11_FB_nfn
            ├── cclm2_T2m-max-sig-change.nc  (22.7 KB)
            ├── cclm2_annual-climatology.nc  (35.4 MB)
            ├── cclm2_annual-series.nc  (526.7 MB)
            ├── cclm2_annual-sig-change.nc  (107.0 KB)
            ├── cclm2_seasonal-climatology.nc  (140.7 MB)
            ├── cclm2_seasonal-drivers-sig-change.nc  (345.2 KB)
            ├── cclm2_seasonal-series.nc  (966.6 MB)
            ├── cclm2_seasonal-sig-change.nc  (339.1 KB)
            ├── cosmo_T2m-max-climatology.nc  (776.4 KB)
            ├── cosmo_T2m-max-series.nc  (9.8 MB)
            └── surf.nc  (736.8 MB)
        📁 cclm2_EUR11_FB_nfs
            ├── cclm2_T2m-max-sig-change.nc  (22.7 KB)
            ├── cclm2_annual-climatology.nc  (35.4 MB)
            ├── cclm2_annual-series.nc  (526.7 MB)
            ├── cclm2_annual-sig-change.nc  (109.6 KB)
            ├── cclm2_seasonal-climatology.nc  (140.6 MB)
            ├── cclm2_seasonal-drivers-sig-change.nc  (350.0 KB)
            ├── cclm2_seasonal-series.nc  (966.5 MB)
            ├── cclm2_seasonal-sig-change.nc  (344.0 KB)
            ├── cosmo_T2m-max-climatology.nc  (775.7 KB)
            ├── cosmo_T2m-max-series.nc  (9.8 MB)
            └── surf.nc  (736.8 MB)
        📁 cclm2_EUR11_FB_ssp1
            ├── cclm2_T2m-max-sig-change.nc  (45.1 KB)
            ├── cclm2_annual-climatology.nc  (35.4 MB)
            ├── cclm2_annual-series.nc  (526.7 MB)
            ├── cclm2_annual-sig-change.nc  (115.0 KB)
            ├── cclm2_seasonal-climatology.nc  (140.6 MB)
            ├── cclm2_seasonal-drivers-sig-change.nc  (627.8 KB)
            ├── cclm2_seasonal-series.nc  (966.5 MB)
            ├── cclm2_seasonal-sig-change.nc  (424.3 KB)
            ├── cosmo_T2m-max-climatology.nc  (775.7 KB)
            ├── cosmo_T2m-max-series.nc  (9.8 MB)
            └── surf.nc  (736.3 MB)
    📁 luc_evaluation
        ├── Dou-et-al_scenarios_4reg.nc  (39.5 KB)
        ├── EUNIS_scenarios_4reg.nc  (42.9 KB)
        └── PFT_scenarios_4reg.nc  (46.1 KB)
