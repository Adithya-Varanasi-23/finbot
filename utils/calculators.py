def calculate_emi(principal, rate_annual, tenure_months):
    """
    Calculates the Equated Monthly Installment (EMI).
    Formula: EMI = [P x R x (1+R)^N]/[(1+R)^N-1]
    R is monthly interest rate.
    """
    if principal == 0 or tenure_months == 0:
        return 0, 0, 0
        
    rate_monthly = (rate_annual / 12) / 100
    if rate_monthly == 0:
        emi = principal / tenure_months
        total_payment = principal
        total_interest = 0
    else:
        emi = (principal * rate_monthly * ((1 + rate_monthly) ** tenure_months)) / (((1 + rate_monthly) ** tenure_months) - 1)
        total_payment = emi * tenure_months
        total_interest = total_payment - principal
        
    return emi, total_interest, total_payment

def calculate_sip(monthly_investment, rate_annual, tenure_years):
    """
    Calculates the Future Value of a Systematic Investment Plan (SIP).
    Formula: FV = P × ({[1 + i]n - 1} / i) × (1 + i).
    """
    if monthly_investment == 0 or tenure_years == 0:
        return 0, 0, 0
        
    rate_monthly = (rate_annual / 12) / 100
    months = tenure_years * 12
    
    if rate_monthly == 0:
        total_invested = monthly_investment * months
        returns = 0
        total_value = total_invested
    else:
        total_value = monthly_investment * (((1 + rate_monthly) ** months - 1) / rate_monthly) * (1 + rate_monthly)
        total_invested = monthly_investment * months
        returns = total_value - total_invested
        
    return total_invested, returns, total_value

def calculate_fd(principal, rate_annual, tenure_years, compounding_frequency=4):
    """
    Calculates Fixed Deposit Maturity value.
    compounding_frequency: 4 for Quarterly, 1 for Yearly.
    A = P (1 + r/n)^(nt)
    """
    if principal == 0 or tenure_years == 0:
        return principal, 0, principal
        
    rate_decimal = rate_annual / 100
    
    maturity_value = principal * ((1 + (rate_decimal / compounding_frequency)) ** (compounding_frequency * tenure_years))
    wealth_gained = maturity_value - principal
    
    return principal, wealth_gained, maturity_value
