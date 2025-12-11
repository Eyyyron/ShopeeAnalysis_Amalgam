import pandas as pd
import numpy as np
from collections import defaultdict

# Load the consolidated data
print("Loading data...")
df = pd.read_csv('consolidated_file_cleaned_v2.csv')

# Season mappings
month_to_season = {
    '01': "Valentine's Season",  # Jan - Start of year
    '02': "Valentine's Season",
    '03': "Holy Week / Lent Season",
    '04': "Holy Week / Lent Season",
    '05': "Summer Season",
    '06': "Back-to-School Season",
    '07': "Back-to-School Season",
    '08': "Back-to-School Season",
    '09': "Back-to-School Season",
    '10': "Halloween / Undas Season",
    '11': "Halloween / Undas Season",
    '12': "Christmas Season"
}

# Also add to Rainy and Summer
month_to_seasons_multi = {
    '01': ["Valentine's Season"],
    '02': ["Valentine's Season"],
    '03': ["Holy Week / Lent Season", "Summer Season"],
    '04': ["Holy Week / Lent Season", "Summer Season"],
    '05': ["Summer Season"],
    '06': ["Summer Season", "Back-to-School Season", "Rainy Season"],
    '07': ["Back-to-School Season", "Rainy Season"],
    '08': ["Back-to-School Season", "Rainy Season"],
    '09': ["Back-to-School Season", "Rainy Season"],
    '10': ["Halloween / Undas Season", "Rainy Season"],
    '11': ["Halloween / Undas Season", "Rainy Season", "Christmas Season"],
    '12': ["Christmas Season"]
}

# Extract month from time column (format YYYY-MM-DD)
df['time'] = pd.to_datetime(df['time'])
df['month'] = df['time'].dt.strftime('%m')

# Also rename columns to match our expectations
df.rename(columns={'top-level_category': 'top_level_category', 
                    'second-level_category': 'second_level_category'}, inplace=True)

# List of categories currently marked as "Others"
others_categories = [
    ("Audio", "Amplifiers & Mixers"),
    ("Audio", "Media Players"),
    ("Audio", "Microphones"),
    ("Audio", "Others"),
    ("Automobiles", "Automobile Spare Parts"),
    ("Automobiles", "Automotive Care"),
    ("Automobiles", "Automotive Keychains & Key Covers"),
    ("Baby & Kids Fashion", "Baby Clothes"),
    ("Baby & Kids Fashion", "Baby Mittens & Footwear"),
    ("Baby & Kids Fashion", "Boy Clothes"),
    ("Baby & Kids Fashion", "Boy Shoes"),
    ("Baby & Kids Fashion", "Girl Clothes"),
    ("Baby & Kids Fashion", "Girl Shoes"),
    ("Beauty", "Beauty Tools"),
    ("Beauty", "Men's Care"),
    ("Cameras & Drones", "Camera Care"),
    ("Cameras & Drones", "Lenses"),
    ("Cameras & Drones", "Security Cameras & Systems"),
    ("Computers & Accessories", "Desktop & Laptop Components"),
    ("Computers & Accessories", "Desktop Computers"),
    ("Computers & Accessories", "Network Components"),
    ("Computers & Accessories", "Softwares"),
    ("Fashion Accessories", "Anklets"),
    ("Fashion Accessories", "Gloves"),
    ("Fashion Accessories", "Investment Precious Metals"),
    ("Fashion Accessories", "Neckties, Bow Ties & Cravats"),
    ("Food & Beverages", "Breakfast Cereals & Spread"),
    ("Food & Beverages", "Food Staples"),
    ("Gaming & Consoles", "Console Machines"),
    ("Gaming & Consoles", "Video Games"),
    ("Health", "Sexual Wellness"),
    ("Hobbies & Collections", "CD, DVD & Bluray"),
    ("Hobbies & Collections", "Needlework"),
    ("Home & Living", "Bathrooms"),
    ("Home & Living", "Dinnerware"),
    ("Home & Living", "Furniture"),
    ("Home & Living", "Gardening"),
    ("Home & Living", "Hand Warmers, Hot Water Bags & Ice Bags"),
    ("Home Appliances", "Batteries"),
    ("Home Appliances", "Large Household Appliances"),
    ("Home Appliances", "Remote Controls"),
    ("Men Bags", "Briefcases"),
    ("Men Bags", "Waist Bags & Chest Bags"),
    ("Men Clothes", "Innerwear & Underwear"),
    ("Men Clothes", "Jeans"),
    ("Men Clothes", "Occupational Attire"),
    ("Men Clothes", "Suits"),
    ("Men Shoes", "Loafers & Boat Shoes"),
    ("Men Shoes", "Oxfords & Lace"),
    ("Mobile & Gadgets", "Sim Cards"),
    ("Mobile & Gadgets", "Walkie Talkies"),
    ("Mom & Baby", "Baby Safety"),
    ("Mom & Baby", "Diapering & Potty"),
    ("Mom & Baby", "Feeding Essentials"),
    ("Mom & Baby", "Maternity Healthcare"),
    ("Mom & Baby", "Milk Formula & Baby Food"),
    ("Motorcycles", "Motorcycle Spare Parts"),
    ("Muslim Fashion", "Men Muslim Wear"),
    ("Muslim Fashion", "Prayer Attire & Equipment"),
    ("Muslim Fashion", "Women Muslim Wear"),
    ("Pets", "Litter & Toilet"),
    ("Pets", "Pet Food"),
    ("Stationery", "Letters & Envelopes"),
    ("Tickets, Vouchers & Services", "Events & Attractions"),
    ("Tickets, Vouchers & Services", "Services"),
    ("Tickets, Vouchers & Services", "Shopping"),
    ("Tickets, Vouchers & Services", "Telco"),
    ("Tickets, Vouchers & Services", "Utilities"),
    ("Women Clothes", "Fabric"),
    ("Women Clothes", "Jumpsuits, Playsuits & Overalls"),
    ("Women Clothes", "Lingerie & Underwear"),
    ("Women Clothes", "Maternity Wear"),
    ("Women Shoes", "Heels"),
]

# Analyze demand for each category
seasonal_mapping = {}

print("\nAnalyzing demand patterns for 'Others' categories...")
for top_cat, sub_cat in others_categories:
    # Filter data for this category
    cat_data = df[(df['top_level_category'] == top_cat) & 
                  (df['second_level_category'] == sub_cat)]
    
    if len(cat_data) == 0:
        print(f"⚠️  No data found for {top_cat} > {sub_cat}")
        continue
    
    # Group by month and sum sales
    monthly_demand = cat_data.groupby('month')['sold'].sum().sort_index()
    
    if len(monthly_demand) == 0:
        print(f"⚠️  No sales data for {top_cat} > {sub_cat}")
        continue
    
    # Find peak months (top 2-3 months)
    top_months = monthly_demand.nlargest(3).index.tolist()
    
    # Map peak months to seasons
    season_scores = defaultdict(int)
    for month in top_months:
        for season in month_to_seasons_multi.get(month, []):
            season_scores[season] += 1
    
    # Select the season with highest score
    if season_scores:
        assigned_season = max(season_scores, key=season_scores.get)
        seasonal_mapping[f"{top_cat}|{sub_cat}"] = assigned_season
        
        print(f"✓ {top_cat} > {sub_cat}")
        print(f"  Peak months: {', '.join(top_months)}")
        print(f"  Assigned to: {assigned_season}")
    else:
        print(f"Could not determine season for {top_cat} > {sub_cat}")

# Print final mapping
print("\n" + "="*80)
print("FINAL SEASON MAPPING FOR 'OTHERS' CATEGORIES:")
print("="*80)
print("\nPython Dictionary Format:")
print("{")
for key, value in sorted(seasonal_mapping.items()):
    print(f'    "{key}": "{value}",')
print("}")

# Save to file
with open('others_season_mapping.txt', 'w') as f:
    f.write("Season Mapping for 'Others' Categories\n")
    f.write("="*80 + "\n\n")
    for key, value in sorted(seasonal_mapping.items()):
        f.write(f"{key}: {value}\n")

print("\n✓ Mapping saved to others_season_mapping.txt")
