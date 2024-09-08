import pandas as pd
import numpy as np
import sys
import os

__file__ = "inv_theory.py"
current_dir = os.path.dirname(os.path.abspath(__file__))

R = 0.055
b = 1/(1+R)
maturity_g = 0.073
time_frame = 10
start_earnings = 10

def get_start_vals(R_, maturity_g_, time_frame_):
    global R, maturity_g, time_frame
    R = R_
    maturity_g = maturity_g_
    time_frame = time_frame_
    # Recalculate `b` if needed
    b = 1 / (1 + R)


def predict_multiple(growth, t, detail = False, max = 50): 
    growth = growth/100
    maturity_g = 0.065 + 0.1*(growth - 0.065)
    k_vec_m = 1 + maturity_g
    maturity_multiple = (k_vec_m*b*(1-(k_vec_m*b)**time_frame)/(1-b*k_vec_m))
    maturity_multiple   
    b_vec = [b] * t
    k_vec = [1 + growth] * t
    b_vec = np.cumprod(b_vec)[:t]
    k_vec = np.cumprod(k_vec)[:t]
    if detail:
        print(f'Maturity growth rate is assumed to be: {maturity_g}')
        print(f'As a result of the pdv of eps this results in, the maturity multiple is assumed to be: {maturity_multiple}')
        print(f'Pricing in an expected return of {R*100}%, we expect an end of period p/e of...')   
    return float(np.min([sum(k_vec*b_vec) + maturity_multiple*b_vec[-1]*k_vec[-1], max]))

def predict_roi(growth, multiple, fut_multiple, n = 3, payout_rate = 1, detail = False): 
    growth = min([growth/100,0.30])
    fut_price_to_curr_price = ((1+growth)**n)*(fut_multiple/multiple)
    growth_vec = [1+ growth] * n
    cum_growth_vec = np.cumprod(growth_vec)
    cum_income_to_curr_price = (1/multiple)*(np.sum(cum_growth_vec))
    pr = fut_price_to_curr_price
    ir = float(cum_income_to_curr_price)
    tr = pr + ir
    tr_ann = float(tr**(1/n) - 1)
    if detail:
        print(f'Estimated geometric average annual eps growth in the period: {growth*100}%')
        print(f'Cumulative eps growth in the period: {(cum_growth_vec[-1]-1)*100}%')
        print(f'And the P/E is expected to change to: {fut_multiple} from its current {multiple}')
        print(f'Price reaches {(pr)*100}% of the starting price')
        print(f'Cumulative income is {ir*100}% of the starting price')
        print(f'Total Return is {tr*100}%')
        print(f'Annualised to a {n} year period is {tr_ann*100}%')
    return tr_ann 

def clean_and_fill(df):
    """
    Remove rows with NaN values across all specified columns, and fill NaNs in the 
    '5y_geo_growth_diluted_eps' column with the first available non-null value from other columns.

    Parameters:
    - df (DataFrame): The DataFrame to process.

    Returns:
    - DataFrame: The processed DataFrame.
    """
    # Define the columns to check for NaN values
    columns_to_check = [
        'eps_growth', 
        'geo_grow_diluted_eps_cont_ops', 
        'diluted_eps_cont_ops_5yr_avg_gr', 
        '5y_geo_growth_diluted_eps'
    ]
    
    # Drop rows where all specified columns are NaN and create a copy
    df_cleaned = df.dropna(subset=columns_to_check, how='all').copy()
    
    # Fill NaNs in '5y_geo_growth_diluted_eps' with the first available non-null value
    df_cleaned['5y_geo_growth_diluted_eps'] = df_cleaned['5y_geo_growth_diluted_eps'].fillna(
        df_cleaned['diluted_eps_cont_ops_5yr_avg_gr']
    ).fillna(
        df_cleaned['geo_grow_diluted_eps_cont_ops']
    ).fillna(
        df_cleaned['eps_growth']
    )
    
    # Merge the cleaned '5y_geo_growth_diluted_eps' back into the original df
    df_merged = df.merge(
        df_cleaned[['5y_geo_growth_diluted_eps']], 
        left_index=True, 
        right_index=True, 
        how='left', 
        suffixes=('', '_filled')
    )
    
    # Use the filled values to update the original column
    df_merged['5y_geo_growth_diluted_eps'] = df_merged['5y_geo_growth_diluted_eps_filled']

    # Drop the extra column after merging
    df_merged.drop(columns=['5y_geo_growth_diluted_eps_filled'], inplace=True)

    return df_merged

def gen_returns(df, decr = 0.7, factor = 0.5):
    df["exp_geo_growth_diluted_eps"] = decr*df["5y_geo_growth_diluted_eps"]
    df["exp_pe_ratio"] = df["exp_geo_growth_diluted_eps"].apply(lambda x: predict_multiple(x, 5))
    df["exp_pe_ratio_lb"] = [max([elem, 8]) for elem in factor*df["pe_ratio"]]
    df["exp_ann_trr"] = [predict_roi(df["exp_geo_growth_diluted_eps"][i], df["pe_ratio"][i], df["exp_pe_ratio"][i]) for i in df.index]
    df["exp_ann_trr"] = df["exp_ann_trr"].fillna(decr*df["current_ann_trr_5yr"]/100)
    df["exp_ann_trr_lb"] = [predict_roi(df["exp_geo_growth_diluted_eps"][i], df["pe_ratio"][i], df["exp_pe_ratio_lb"][i]) for i in df.index]
    df["exp_ann_trr_lb"] = df["exp_ann_trr_lb"].fillna(decr*factor*df["current_ann_trr_5yr"]/100)
    return df

def exclude(df, tr_floor=0.08, eps_g_floor=0.05, tr_pctl_floor=5, eps_g_pctl_floor=5, five_yr_ann_eps_g_min=0.05, exp_trr_lb_floor = 0.06):
    """
    Filter DataFrame rows based on conditions applied to columns containing 'trr' or growth-related terms.

    Parameters:
    - df (DataFrame): The DataFrame to filter.
    - tr_floor (float): Minimum threshold for 'trr' columns.
    - eps_g_floor (float): Minimum threshold for EPS growth columns.
    - tr_pctl_floor (float): Percentile threshold for 'trr' columns.
    - eps_g_pctl_floor (float): Percentile threshold for EPS growth columns.
    - five_yr_ann_eps_g_min (float): Not used in this version, reserved for future conditions.

    Returns:
    - DataFrame: The filtered DataFrame.
    """
    
    # Filter columns matching the regex for 'trr'
    trr_cols = df.filter(regex='trr')
    for col in trr_cols.columns:
        # Compute the given percentile for each 'trr' column
        percentile = np.nanpercentile(df[col], tr_pctl_floor)
        
        # Create a mask to filter rows where each 'trr' column is either NaN or meets conditions
        mask = (df[col].isna()) | ((df[col] >= percentile) & (df[col] >= tr_floor))
        
        # Apply the mask to filter the DataFrame for each 'trr' column
        df = df[mask]

    # Filter columns matching the regex for 'eps' or 'earnings' combined with 'gr'
    eps_growth_cols = df.filter(regex='(gr.*eps|eps.*gr|gr.*earnings|earnings.*gr)')
    for col in eps_growth_cols.columns:
        # Compute the given percentile for each growth-related column
        percentile = np.nanpercentile(df[col], eps_g_pctl_floor)

        # Create a mask to filter rows where each column is either NaN or meets conditions
        mask = (df[col].isna()) | ((df[col] >= percentile) & (df[col] >= eps_g_floor))

        # Apply the mask to filter the DataFrame for each column
        df = df[mask]

    # Eliminate stocks that have a chance of performing below a threshold
    mask = (df["exp_ann_trr_lb"].isna()) | (df["exp_ann_trr_lb"] <= exp_trr_lb_floor)
     # Rank by total returns and select up to top 50
    df = df.sort_values(by = "exp_ann_trr", ascending = False)
    
    
    return df.head(50)