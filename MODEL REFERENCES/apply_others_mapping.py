import pandas as pd
import ast

# Load the season mapping from analyze script output
season_mapping = {
    "Audio|Amplifiers & Mixers": "Rainy Season",
    "Audio|Media Players": "Rainy Season",
    "Audio|Microphones": "Back-to-School Season",
    "Audio|Others": "Rainy Season",
    "Automobiles|Automobile Spare Parts": "Rainy Season",
    "Automobiles|Automotive Care": "Holy Week / Lent Season",
    "Automobiles|Automotive Keychains & Key Covers": "Back-to-School Season",
    "Baby & Kids Fashion|Baby Clothes": "Summer Season",
    "Baby & Kids Fashion|Baby Mittens & Footwear": "Halloween / Undas Season",
    "Baby & Kids Fashion|Boy Clothes": "Summer Season",
    "Baby & Kids Fashion|Boy Shoes": "Rainy Season",
    "Baby & Kids Fashion|Girl Clothes": "Summer Season",
    "Baby & Kids Fashion|Girl Shoes": "Back-to-School Season",
    "Beauty|Beauty Tools": "Back-to-School Season",
    "Beauty|Men's Care": "Rainy Season",
    "Cameras & Drones|Camera Care": "Valentine's Season",
    "Cameras & Drones|Lenses": "Back-to-School Season",
    "Cameras & Drones|Security Cameras & Systems": "Holy Week / Lent Season",
    "Computers & Accessories|Desktop & Laptop Components": "Rainy Season",
    "Computers & Accessories|Desktop Computers": "Summer Season",
    "Computers & Accessories|Network Components": "Back-to-School Season",
    "Computers & Accessories|Softwares": "Valentine's Season",
    "Fashion Accessories|Anklets": "Summer Season",
    "Fashion Accessories|Gloves": "Holy Week / Lent Season",
    "Fashion Accessories|Investment Precious Metals": "Rainy Season",
    "Fashion Accessories|Neckties, Bow Ties & Cravats": "Valentine's Season",
    "Food & Beverages|Breakfast Cereals & Spread": "Back-to-School Season",
    "Food & Beverages|Food Staples": "Rainy Season",
    "Gaming & Consoles|Console Machines": "Christmas Season",
    "Gaming & Consoles|Video Games": "Summer Season",
    "Health|Sexual Wellness": "Holy Week / Lent Season",
    "Hobbies & Collections|CD, DVD & Bluray": "Rainy Season",
    "Hobbies & Collections|Needlework": "Summer Season",
    "Home & Living|Bathrooms": "Back-to-School Season",
    "Home & Living|Dinnerware": "Rainy Season",
    "Home & Living|Furniture": "Back-to-School Season",
    "Home & Living|Gardening": "Holy Week / Lent Season",
    "Home & Living|Hand Warmers, Hot Water Bags & Ice Bags": "Summer Season",
    "Home Appliances|Batteries": "Holy Week / Lent Season",
    "Home Appliances|Large Household Appliances": "Summer Season",
    "Home Appliances|Remote Controls": "Back-to-School Season",
    "Men Bags|Briefcases": "Back-to-School Season",
    "Men Bags|Waist Bags & Chest Bags": "Christmas Season",
    "Men Clothes|Innerwear & Underwear": "Summer Season",
    "Men Clothes|Jeans": "Christmas Season",
    "Men Clothes|Occupational Attire": "Rainy Season",
    "Men Clothes|Suits": "Back-to-School Season",
    "Men Shoes|Loafers & Boat Shoes": "Back-to-School Season",
    "Men Shoes|Oxfords & Lace": "Back-to-School Season",
    "Mobile & Gadgets|Sim Cards": "Summer Season",
    "Mobile & Gadgets|Walkie Talkies": "Summer Season",
    "Mom & Baby|Baby Safety": "Back-to-School Season",
    "Mom & Baby|Diapering & Potty": "Summer Season",
    "Mom & Baby|Feeding Essentials": "Summer Season",
    "Mom & Baby|Maternity Healthcare": "Rainy Season",
    "Mom & Baby|Milk Formula & Baby Food": "Summer Season",
    "Motorcycles|Motorcycle Spare Parts": "Rainy Season",
    "Muslim Fashion|Men Muslim Wear": "Valentine's Season",
    "Muslim Fashion|Prayer Attire & Equipment": "Valentine's Season",
    "Muslim Fashion|Women Muslim Wear": "Holy Week / Lent Season",
    "Pets|Litter & Toilet": "Halloween / Undas Season",
    "Pets|Pet Food": "Back-to-School Season",
    "Stationery|Letters & Envelopes": "Summer Season",
    "Tickets, Vouchers & Services|Events & Attractions": "Summer Season",
    "Tickets, Vouchers & Services|Services": "Summer Season",
    "Tickets, Vouchers & Services|Shopping": "Holy Week / Lent Season",
    "Tickets, Vouchers & Services|Telco": "Summer Season",
    "Tickets, Vouchers & Services|Utilities": "Valentine's Season",
    "Women Clothes|Fabric": "Summer Season",
    "Women Clothes|Jumpsuits, Playsuits & Overalls": "Summer Season",
    "Women Clothes|Lingerie & Underwear": "Summer Season",
    "Women Clothes|Maternity Wear": "Summer Season",
    "Women Shoes|Heels": "Summer Season",
}

print("Loading CSV file...")
df = pd.read_csv('hybrid_sarima_lstm_categories_unique_with_seasons.csv')

print(f"Total rows before update: {len(df)}")
print(f"Rows with 'Others' season: {len(df[df['season'] == 'Others'])}")

# Apply mapping to 'Others' entries
def map_season(row):
    if row['season'] == 'Others':
        key = f"{row['top_level_category']}|{row['second_level_category']}"
        return season_mapping.get(key, 'Others')  # Keep 'Others' if not found in mapping
    return row['season']

df['season'] = df.apply(map_season, axis=1)

print(f"Rows with 'Others' season after update: {len(df[df['season'] == 'Others'])}")
print(f"\nSeason distribution after mapping:")
print(df['season'].value_counts().sort_index())

# Save updated CSV
output_file = 'hybrid_sarima_lstm_categories_unique_with_seasons_updated.csv'
df.to_csv(output_file, index=False)
print(f"\n✓ Updated CSV saved to: {output_file}")

# Also create backup of original
df.to_csv('hybrid_sarima_lstm_categories_unique_with_seasons_backup.csv', index=False)
print("✓ Backup saved to: hybrid_sarima_lstm_categories_unique_with_seasons_backup.csv")
