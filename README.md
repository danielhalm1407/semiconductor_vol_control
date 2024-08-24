# EconProjects

A collection of pet/passion projects in economic and financial theory, policy and transit modelling.

**Author:** **[danielhalm1407](https://github.com/danielhalm1407/)**

### Sub-Projects

#### Project 1: UBI_Test

- Modelling the Effect of a Universal Basic Income Transfer on Income Distribution Throughout time.

#### Project 2: [Investment_Theory](subpages_1/investment_theory.md)

- Predicting the returns of equities throughout time and attributing them to income and capital appreciation components.

- Predicting the returns of equities based on historic earnings growth, using a geometric series to predict the multiple the market will price in, and hence project price returns. Use this to create a rules-based 'select' index/rules based portfolio.

- **In future:** Aim to use past data to make prediction model stochastic: fit the distribution of the P/E multiple and in turn find the probability distribution of the (dependent) price returns.

- **In future:** Turn into a script that continuously queries the Bloomberg API and rebalances the portfolio. To do this monthly, likely need a cloud tool of some kind.

#### Project 3: Transit Fantasy

- Import existing Google MyMaps transit fantasy maps (as KML Files) and take them even further. Purely for fun.

###  🗂️ Directory Structure
```plaintext
.
├── README.md
├── credentials.json (used to acess the OpenAQ data)
├── data
│   ├── Bloomberg_Rankings.xlsx (The Index Universe Filtered from Bloomberg Data and Ranked by Past Performance)
│   ├── Top_Stocks.xlsx (The final selection of the equal-weighted top-50 forecast performance eligible stocks)
│   ├── UBI Test.xlsx (The original experimentation with the UBI Concept in Excel)
│   └── econ.db (Our Database for future data queries and related tables (E.g. multiples data and EPS Growth Data))
├── docs (webpages)
│   ├── subpages_1
│       ├── Images placed on these subpages
│       └── investment_theory.md (Some findings from the First Parts of the Investment_Theory sub-project)
│   └── index.md (Contents/Home Page of our Website)
├── notebooks
│   ├── Investment_Theory
│       ├── NB01_Investment_Theory_1.ipynb
│       ├── NB02_Investment_Theory_2.ipynb
│       └── NB03_Total_Return_Predictor
│   └── UBI_Test    
│       └── NB05_UBI_Test.ipynb
├── shared_data (early exchanging data between group members)
├── src
│   └── econ_utils (our Python package)
│       ├── inv_theory.ipynb (Functions needed for the Investment_Theory sub-project)
│       └── ubi_test.py (Functions needed for the UBI_Test sub-project)
│   └── scripts (runnable Python scripts)
│       ├── nb04.py (runs NB04 notebook as a script)
│       └── sql_in.py (saves the excel files into a database as tables)
├── Transit Fantasy
│   ├── Caracas Metro Google Maps Layers
│   ├── LA Metro Google Maps Layers
│   └── Toronto Uber-Improved Transport Google Maps Layers
└── requirements.txt (set of packages to install onto the virtual environment)

```
### 📚 How to get this to work

If you want to replicate the analysis in this notebook, you will need to:

1. Clone this repository to your computer
    ```bash
    git clone git@github.com:danielhalm1407/EconProjects.git
    ```
2. Add it to your VS Code workspace
3. Set up your conda environment on conda's 3.11 version of python:

    ```bash
    conda create -n venv-econ python=3.11 ipython
    conda activate venv-econ
    ```
4. Make sure `pip` is installed inside that environment:

    ```bash
    conda install pip
    ```

5. Now use that pip to install the packages:

    ```bash
    python -m pip install -r requirements.txt
    ```

6. Run the scripts

    If you want to run these separately,
    type 
    ```bash
    cd /src/scripts
    ```
    and then 
    ```bash
    python nb03.py
    ```

    If you want to run these all in one go
    type 
    ```bash
    bash run_all.sh
    ```
7. Alternatively, Run the notebooks

    Run all the notebooks NB01-NB06 in order, selecting the venv-econ [3.11] kernel