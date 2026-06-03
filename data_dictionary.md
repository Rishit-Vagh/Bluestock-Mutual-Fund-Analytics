# Data Dictionary: Bluestock Mutual Fund Analytics

This document defines the schemas and data types for the processed mutual fund datasets and the corresponding SQLite database `bluestock_mf.db`.

## 1. dim_fund (`01_fund_master.csv`)
**Source**: Association of Mutual Funds in India (AMFI) Master Data.
**Description**: Dimension table containing details of mutual fund schemes.

| Column | Data Type | Business Definition |
|--------|-----------|---------------------|
| `amfi_code` | INTEGER | Unique scheme code provided by AMFI. (Primary Key) |
| `fund_house` | TEXT | Name of the Asset Management Company (AMC). |
| `scheme_name` | TEXT | Full name of the mutual fund scheme. |
| `category` | TEXT | Broad category of the fund (e.g., Equity, Debt, Hybrid). |
| `sub_category` | TEXT | Specific sub-category (e.g., Large Cap, Mid Cap, Liquid). |
| `plan` | TEXT | Plan type (Direct or Regular). |
| `launch_date` | DATE | Date the fund was launched. |
| `benchmark` | TEXT | The benchmark index against which performance is measured. |
| `expense_ratio_pct` | REAL | Total Expense Ratio (TER) in percentage. |
| `exit_load_pct` | REAL | Exit load percentage applied on early redemption. |
| `min_sip_amount` | REAL | Minimum amount required to start a SIP. |
| `min_lumpsum_amount` | REAL | Minimum amount required for a one-time (lumpsum) investment. |
| `fund_manager` | TEXT | Name of the primary fund manager. |
| `risk_category` | TEXT | General risk level associated with the fund. |
| `sebi_category_code` | TEXT | Code given by SEBI based on the fund's investment objective. |

---

## 2. dim_date (`dim_date.csv` generated)
**Source**: Derived from transactional and NAV dates.
**Description**: Date dimension table for time-series aggregation.

| Column | Data Type | Business Definition |
|--------|-----------|---------------------|
| `date` | DATE | Standard date format (YYYY-MM-DD). (Primary Key) |
| `day` | INTEGER | Day of the month. |
| `month` | INTEGER | Month of the year. |
| `year` | INTEGER | Year. |
| `quarter` | INTEGER | Quarter of the year (1 to 4). |
| `day_of_week` | INTEGER | Day of the week index (0 = Monday, 6 = Sunday). |
| `is_weekend` | BOOLEAN | Indicates whether the date falls on a weekend. |

---

## 3. fact_nav (`02_nav_history.csv`)
**Source**: Historical NAV values fetched from API.
**Description**: Daily Net Asset Value of mutual fund schemes. Missing weekend and holiday NAVs are forward-filled.

| Column | Data Type | Business Definition |
|--------|-----------|---------------------|
| `amfi_code` | INTEGER | Foreign Key linking to `dim_fund`. |
| `date` | DATE | Foreign Key linking to `dim_date`. |
| `nav` | REAL | Net Asset Value (Price) of the mutual fund on the given date. |

---

## 4. fact_transactions (`08_investor_transactions.csv`)
**Source**: Internal investor platform logs.
**Description**: Transaction logs including SIPs, lumpsums, and redemptions by individual investors.

| Column | Data Type | Business Definition |
|--------|-----------|---------------------|
| `transaction_id` | INTEGER | Unique identifier for the transaction (auto-generated). |
| `investor_id` | TEXT | Unique identifier for the investor. |
| `transaction_date` | DATE | Date of transaction. Foreign Key to `dim_date`. |
| `amfi_code` | INTEGER | Foreign Key to `dim_fund`. |
| `transaction_type` | TEXT | Type of transaction (`SIP`, `Lumpsum`, or `Redemption`). |
| `amount_inr` | REAL | Transaction amount in Indian Rupees. |
| `state` | TEXT | Investor's state of residence. |
| `city` | TEXT | Investor's city of residence. |
| `city_tier` | TEXT | Classification of the city tier (e.g., Tier 1, Tier 2). |
| `age_group` | TEXT | Age bracket of the investor. |
| `gender` | TEXT | Gender of the investor. |
| `annual_income_lakh` | REAL | Investor's annual income bracket in lakhs. |
| `payment_mode` | TEXT | Mode of payment used for the transaction. |
| `kyc_status` | TEXT | KYC status of the investor (`Verified` or `Pending`). |

---

## 5. fact_performance (`07_scheme_performance.csv`)
**Source**: Third-party performance aggregators.
**Description**: Various performance and risk metrics associated with schemes.

| Column | Data Type | Business Definition |
|--------|-----------|---------------------|
| `amfi_code` | INTEGER | Foreign Key linking to `dim_fund`. |
| `scheme_name` | TEXT | Full name of the scheme. |
| `fund_house` | TEXT | AMC Name. |
| `category` | TEXT | Category classification. |
| `plan` | TEXT | Plan type. |
| `return_1yr_pct` | REAL | 1-year trailing return in percentage. |
| `return_3yr_pct` | REAL | 3-year trailing return in percentage. |
| `return_5yr_pct` | REAL | 5-year trailing return in percentage. |
| `benchmark_3yr_pct` | REAL | 3-year trailing return of the benchmark index in percentage. |
| `alpha` | REAL | Measure of excess return against benchmark. |
| `beta` | REAL | Measure of scheme volatility relative to the broader market. |
| `sharpe_ratio` | REAL | Risk-adjusted return measure. |
| `sortino_ratio` | REAL | Risk-adjusted return focusing on downside deviation. |
| `std_dev_ann_pct` | REAL | Annualized standard deviation (volatility). |
| `max_drawdown_pct` | REAL | Maximum observed loss from peak to trough. |
| `aum_crore` | REAL | Asset Under Management for the scheme in crores. |
| `expense_ratio_pct` | REAL | Total expense ratio for the scheme. |
| `morningstar_rating` | INTEGER | Rating given by Morningstar (usually 1 to 5). |
| `risk_grade` | TEXT | Risk rating associated with the scheme. |
| `is_anomaly` | BOOLEAN | Custom flag indicating missing values or suspicious data. |

---

## 6. fact_aum (`03_aum_by_fund_house.csv`)
**Source**: AMFI Quarterly disclosures.
**Description**: Total Assets Under Management aggregated at the Fund House level.

| Column | Data Type | Business Definition |
|--------|-----------|---------------------|
| `date` | DATE | Date of AUM reporting. Foreign Key to `dim_date`. |
| `fund_house` | TEXT | Name of the Asset Management Company. |
| `aum_lakh_crore` | REAL | AUM represented in lakhs of crores. |
| `aum_crore` | REAL | AUM represented in crores. |
| `num_schemes` | INTEGER | Total number of schemes offered by the fund house. |
