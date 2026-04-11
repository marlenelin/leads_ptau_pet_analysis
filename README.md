# Project 
Plasma Phosphorylated Tau 217 In Sporadic Early-onset Alzheimer’s Disease: Associations With Tau And Amyloid PET And Clinical Progression

## Overview
This repository contains analysis code for the project.

The computational environment is reproducible using:

- R (managed with renv)
- Python (managed with requirements.txt)

---

# Environment Setup

## 1. Clone the repository

```bash
git clone https://github.com/marlenelin/leads_ptau_pet_analysis.git
cd leads_ptau_pet_analysis
```



## 2. Python Setup

### Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\Scripts\activate    # Windows
```

### Install dependencies

```bash
pip install -r requirements.txt
pip list #verify installs
```

Notes:
- requirements.txt defines the Python dependencies for this project
- Always activate the virtual environment before running Python code

## 3. R Setup (renv)

### Start R from the project root

```bash
cd leads_ptau_pet_analysis
R
```

## Restore the R environment

```r
install.packages("renv")   # only needed once
renv::restore()
renv::status() # verify, should show no issues found
```
Notes:
- renv.lock contains exact package versions
- renv/ is the project-specific package library
- .Rprofile automatically activates renv when R starts in this folder
 
# File Structure

```
leads_ptau_pet_analysis/
├── data/
│   ├── raw/
│   ├── interim/
│   └── cleaned/
├── notebooks/
├── src/
├── renv/
├── renv.lock
├── .gitignore
├── requirements.txt
├── README.md
```
  
# Baseline analysis 

## Data summary, baseline ptau ROC, T1 (EOAD vs. EOnonAD)
- **File**: baseline_ptau_roc_t1.ipynb

- **Cohort Filtering**
  - Uses baseline subjects with available plasma p-tau217 measurements
  - Restricts analysis to EOAD and EOnonAD groups
  - Summarizes longitudinal follow-up (≥2 visits) for EOAD participants

- **Table 1**
  - Generates baseline descriptive statistics for demographic, clinical, and biomarker variables
  - Reports continuous and categorical variables stratified by cohort (EOAD vs EOnonAD)

- **ROC Analysis**
  - Computes receiver operating characteristic (ROC) curves for plasma p-tau217 and estimates area under the curve (AUC)
  - Calculates 95% confidence intervals for AUC using:
    - DeLong method (primary)
    - Bootstrap resampling (for ROC band visualization)
  - Determines the optimal cutoff using the Youden index
  - Evaluates diagnostic performance at:
    - Youden-optimal cutoff (EOAD/LEADS-derived threshold)
    - NCRAD threshold
  - Reports:
    - Sensitivity and specificity with 95% confidence intervals (Wilson method)
    - Confusion matrix counts (TP, FP, TN, FN)

 