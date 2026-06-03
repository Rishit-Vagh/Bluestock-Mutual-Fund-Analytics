-- 1. Top 5 funds by AUM
SELECT 
    f.scheme_name, 
    p.aum_crore 
FROM 
    fact_performance p
JOIN 
    dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY 
    p.aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month
SELECT 
    d.year, 
    d.month, 
    AVG(n.nav) AS avg_nav
FROM 
    fact_nav n
JOIN 
    dim_date d ON n.date = d.date
GROUP BY 
    d.year, d.month
ORDER BY 
    d.year, d.month;

-- 3. SIP YoY growth
WITH SIP_Yearly AS (
    SELECT 
        d.year, 
        SUM(t.amount_inr) AS total_sip_amount
    FROM 
        fact_transactions t
    JOIN 
        dim_date d ON t.transaction_date = d.date
    WHERE 
        t.transaction_type = 'SIP'
    GROUP BY 
        d.year
)
SELECT 
    year,
    total_sip_amount,
    LAG(total_sip_amount) OVER (ORDER BY year) AS prev_year_amount,
    (total_sip_amount - LAG(total_sip_amount) OVER (ORDER BY year)) * 100.0 / LAG(total_sip_amount) OVER (ORDER BY year) AS yoy_growth_pct
FROM 
    SIP_Yearly;

-- 4. Transactions by state
SELECT 
    state, 
    COUNT(*) AS total_transactions, 
    SUM(amount_inr) AS total_volume
FROM 
    fact_transactions
GROUP BY 
    state
ORDER BY 
    total_volume DESC;

-- 5. Funds with expense_ratio < 1%
SELECT 
    f.scheme_name, 
    f.expense_ratio_pct
FROM 
    dim_fund f
WHERE 
    f.expense_ratio_pct < 1.0
ORDER BY 
    f.expense_ratio_pct ASC;

-- 6. Total SIPs vs Lumpsums vs Redemptions (Transaction Types distribution)
SELECT 
    transaction_type, 
    COUNT(*) AS total_count, 
    SUM(amount_inr) AS total_amount
FROM 
    fact_transactions
GROUP BY 
    transaction_type;

-- 7. Average Return (1yr, 3yr, 5yr) by Fund Category
SELECT 
    f.category, 
    AVG(p.return_1yr_pct) AS avg_1yr_return,
    AVG(p.return_3yr_pct) AS avg_3yr_return,
    AVG(p.return_5yr_pct) AS avg_5yr_return
FROM 
    fact_performance p
JOIN 
    dim_fund f ON p.amfi_code = f.amfi_code
GROUP BY 
    f.category;

-- 8. Top 5 Funds with the best Sharpe Ratio (Risk-adjusted returns)
SELECT 
    f.scheme_name, 
    f.category, 
    p.sharpe_ratio
FROM 
    fact_performance p
JOIN 
    dim_fund f ON p.amfi_code = f.amfi_code
WHERE 
    p.sharpe_ratio IS NOT NULL
ORDER BY 
    p.sharpe_ratio DESC
LIMIT 5;

-- 9. AUM growth by Fund House over time
SELECT 
    fund_house, 
    d.year, 
    SUM(aum_crore) AS total_aum
FROM 
    fact_aum a
JOIN 
    dim_date d ON a.date = d.date
GROUP BY 
    fund_house, d.year
ORDER BY 
    fund_house, d.year;

-- 10. Investor demographics: Total investment by age group
SELECT 
    age_group, 
    COUNT(DISTINCT investor_id) AS unique_investors, 
    SUM(amount_inr) AS total_invested
FROM 
    fact_transactions
WHERE 
    transaction_type IN ('SIP', 'Lumpsum')
GROUP BY 
    age_group
ORDER BY 
    total_invested DESC;
