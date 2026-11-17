import pandas as pd
import numpy as np

# 1. Load raw dataset
df = pd.read_csv('games.csv')

# 2. Data Cleaning & Filtering
# Drop rows with missing essential values
df = df.dropna(subset=['Name', 'Price', 'Estimated owners'])

# Convert Release date to datetime and extract Year
df['Release date'] = pd.to_datetime(df['Release date'], errors='coerce')
df['release_year'] = df['Release date'].dt.year

# 3. Feature Engineering
# Extract midpoint of estimated owners range (e.g., "20000 - 50000" -> 35000)
def parse_owners(val):
    try:
        parts = str(val).split('-')
        return (int(parts[0].strip()) + int(parts[1].strip())) / 2
    except:
        return 0

df['est_owners_mid'] = df['Estimated owners'].apply(parse_owners)

# Calculate Estimated Revenue
df['est_revenue'] = df['Price'] * df['est_owners_mid']

# Create Free vs. Paid flag
df['is_free'] = np.where(df['Price'] == 0, 'Free-to-Play', 'Paid')

# Create Price Categories
conditions = [
    (df['Price'] == 0),
    (df['Price'] < 10),
    (df['Price'] < 20),
    (df['Price'] < 50),
    (df['Price'] >= 50)
]
choices = ['Free', 'Under 10€', '10€-20€', '20€-50€', '50€+']
df['price_category'] = np.select(conditions, choices, default='Other')

# Calculate Positive Review Percentage
total_reviews = df['Positive'] + df['Negative']
df['pct_pos_total'] = np.where(total_reviews > 0, (df['Positive'] / total_reviews) * 100, 0)

# 4. Export cleaned dataset for Power BI
df.to_csv('steam_cleaned.csv', index=False)
print("Data cleaning complete! Exported to steam_cleaned.csv")