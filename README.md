# Semiconductor Volatility Control

Backtesting a variety of volatility control strategies on an underlying semiconductor index ETF.

Given the growing demand and high internal rate of return in the semiconductor sector due to high margins and turnover, this thematic strategy has some of the highest annualised returns over 10 years (most semiconductor ETFs see 15% to 21% annualised returns).

However, the cyclical nature of the semiconductor sector and heavy weighting towards high-profile companies such as Nvidia leads to high volatility. Nonetheless, the cyclical nature of this volatility may mean we may be able to predict downturns in the market and reduce our market participation accordingly.

## DISCLAIMER:

I have used Open AI's Chat GPT 3.5 and GPT 4 to assist with syntax and structuring across various coding aspects of this project.

Please refer to the saved chat log [here](https://chatgpt.com/share/66f6ef1b-d8a4-800f-8df6-c69a5ea35283).

###  🗂️ Directory Structure
```plaintext
.
├── README.md
├── credentials.json (used to acess market data)
├── data
│   ├── ^SOX.xlsx (The Underlying Index Sourced from Yahoo Finance)
│   └── semi.db (Database for efficient market derived data storage)
├── docs (webpages)
│   ├── subpages_1
│       ├── Images and figures placed on the overview webpage.
│   └── index.html (Project overview web page)
├── notebooks
│   ├── NB01_Get_Data.ipynb
│   ├── NB02.1_Backtest_1.ipynb
│   └── NB02.2_Backtest_2.ipynb
├── src
│   ├── semi_utils (our Python package)
│       └── sql_queries.py (Functions needed for database interaction)
│   └── scripts (runnable Python scripts)
│       └── sql_in.py (saves the excel files into a database as tables)
└── requirements.txt (set of packages to install onto the virtual environment)

```
### 📚 How to get this to work

If you want to replicate the analysis in this notebook, you will need to:

1. Clone this repository to your computer
    ```bash
    git clone git@github.com:danielhalm1407/semiconductor_vol_control.git
    ```
2. Add it to your VS Code workspace
3. Set up your conda environment on conda's 3.11 version of python:

    ```bash
    conda create -n venv-semi python=3.11 ipython
    conda activate venv-semi
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

    Run all the notebooks in order, selecting the venv-semi [3.11] kernel