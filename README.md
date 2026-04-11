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
  