import pandas as pd

def process_expense_csv(file):
    """
    Reads a CSV file containing transactions and returns a processed DataFrame.
    Expects standard bank CSV format (Date, Description, Amount).
    """
    try:
        # Read the file
        df = pd.read_csv(file)
        
        # Normalize columns (lowercase, strip whitespace)
        df.columns = df.columns.str.strip().str.lower()
        
        # Basic mapping of common bank column names
        column_mapping = {
            'date': 'Date',
            'transaction date': 'Date',
            'valuedate': 'Date',
            'description': 'Description',
            'narration': 'Description',
            'particulars': 'Description',
            'details': 'Description',
            'amount': 'Amount',
            'withdrawal': 'Withdrawal',
            'dr': 'Withdrawal',
            'deposit': 'Deposit',
            'cr': 'Deposit'
        }
        
        # Rename identified columns
        df.rename(columns={col: column_mapping.get(col, col.title()) for col in df.columns}, inplace=True)
        
        # If 'Amount' column doesn't exist, calculate it from Withdrawals
        if 'Amount' not in df.columns and 'Withdrawal' in df.columns:
            # We want to analyze expenses, so focus on withdrawals
            df['Amount'] = pd.to_numeric(df['Withdrawal'].astype(str).str.replace(',', ''), errors='coerce')
        elif 'Amount' in df.columns:
            df['Amount'] = pd.to_numeric(df['Amount'].astype(str).str.replace(',', ''), errors='coerce')
        
        # Drop rows where 'Amount' is NaN or negative (assuming negative might mean deposits in some formats, or vice versa)
        # For simplicity, we assume we just want to look at positive expense values.
        # User might need to adapt this depending on their bank.
        df = df.dropna(subset=['Amount'])
        df = df[df['Amount'] > 0] 
        
        # Auto-categorize based on description keywords
        df['Category'] = df['Description'].apply(categorize_transaction)
        
        return df
    except Exception as e:
        return pd.DataFrame() # Return empty df on error

def categorize_transaction(description):
    """Simple keyword-based categorizer for expenses."""
    if not isinstance(description, str):
        return 'Other'
        
    desc = description.lower()
    
    categories = {
        'Food & Dining': ['restaurant', 'cafe', 'swiggy', 'zomato', 'food', 'mcdonalds', 'kfc', 'starbucks', 'dominos'],
        'Groceries': ['supermarket', 'grocery', 'mart', 'bazaar', 'spencers', 'reliance fresh', 'blinkit', 'zepto', 'instamart'],
        'Transportation': ['uber', 'ola', 'taxi', 'fuel', 'petrol', 'diesel', 'bharat petroleum', 'shell', 'irctc', 'flight', 'bus'],
        'Utilities & Bills': ['electricity', 'water', 'gas', 'internet', 'broadband', 'mobile', 'recharge', 'airtel', 'jio', 'vi'],
        'Shopping': ['amazon', 'flipkart', 'myntra', 'ajio', 'shopping', 'store', 'mall'],
        'Entertainment': ['netflix', 'spotify', 'prime', 'hotstar', 'cinema', 'movie', 'bookmyshow', 'pvr'],
        'Health & Fitness': ['pharmacy', 'hospital', 'clinic', 'gym', 'health', 'apollo', 'netmeds'],
        'Rent & Housing': ['rent', 'maintenance', 'society']
    }
    
    for category, keywords in categories.items():
        if any(keyword in desc for keyword in keywords):
            return category
            
    return 'Other'

def get_spending_summary(df):
    """Groups dataframe by category and calculates total amount."""
    if df.empty or 'Category' not in df.columns or 'Amount' not in df.columns:
        return pd.DataFrame()
        
    summary = df.groupby('Category')['Amount'].sum().reset_index()
    summary = summary.sort_values(by='Amount', ascending=False)
    # create a percentage column
    total = summary['Amount'].sum()
    summary['Percentage'] = (summary['Amount'] / total * 100).round(1)
    
    return summary
