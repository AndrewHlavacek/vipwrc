import pandas as pd

# Read the CSV file

# FILTER SO THERE ARE NO PITCHERS
df = pd.read_csv('/Users/andrewhlavacek/Downloads/vipwrc+/wrc.csv')

# Display basic info about the dataset
print("Dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

# ------------------------------------------------------------


# League averages (these would typically be calculated from the full dataset)
# For demonstration, using sample values - in practice, calculate these from your data

# League weighted on base average
lgWOBA = 0.378

# woba scale use this website https://rfrey22.medium.com/collegiate-linear-weights-f0237cf40451
lgWOBA_scale = 1.2

# League Runs per PA
lgRPPA = 0.173


# ------------------------------------------------------------


print(f"\nLeague averages:")
print(f"League wOBA: {lgWOBA}")
print(f"League wOBA Scale: {lgWOBA_scale}")
print(f"League Runs per PA: {lgRPPA}")

# Calculate wRC (Weighted Runs Created)
# Formula: wRC = ((wOBA - lgwOBA) / wOBAScale + lgRPPA) * PA
# ------------------------------------------------------------

print("\nCalculating wRC...")
df['wRC'] = ((df['wOBA'] - lgWOBA) / lgWOBA_scale + lgRPPA) * df['PA']

# ------------------------------------------------------------

print("\nCalculating Ballpark Factor...")
# Read ballpark games and compute ballpark factor
games_csv_path = '/Users/leozheng/Projects/VIP/vipwrc/GT Baseball Ballpark - Sheet1.csv'

try:
    games_df = pd.read_csv(games_csv_path)

    # Identify home games by Location containing "Atlanta" (case-insensitive)
    games_df['is_home'] = games_df['Location'].astype(str).str.lower().str.contains('atlanta')

    # Extract total runs scored in the game from Time/Result, e.g., "W 11-4 (7 Inn)" -> 11 + 4 = 15
    score_pairs = games_df['Time/Result'].astype(str).str.extract(r'(\d+)\s*-\s*(\d+)')
    score_pairs = score_pairs.apply(pd.to_numeric, errors='coerce')
    games_df['total_runs'] = score_pairs.sum(axis=1)

    home_total_runs = games_df.loc[games_df['is_home'], 'total_runs'].sum(min_count=1)
    away_total_runs = games_df.loc[~games_df['is_home'], 'total_runs'].sum(min_count=1)

    if pd.isna(home_total_runs) or pd.isna(away_total_runs) or away_total_runs == 0:
        ballparkFactor = float('nan')
    else:
        ballparkFactor = (home_total_runs / 37) / (away_total_runs / 25)

    print(f"Ballpark Factor (home total runs / away total runs): {ballparkFactor}")
except FileNotFoundError:
    print("Ballpark games CSV file not found. Using default ballpark factor of 1.0")
    ballparkFactor = 1.0

# Calculate league average wRC for wRC+ calculation
# wRC+ = [(wRAA per PA + lgRPPA) + ((lgRPPA - ballparkFactor * lgRPPA) / lgWRC_per_PA_no_pitchers)] * 100


print("Calculating league averages...")
total_wRC = df['wRC'].sum()
total_PA = df['PA'].sum()
lg_wRC_per_PA = total_wRC / total_PA


print(f"League wRC per PA: {lg_wRC_per_PA:.6f}")


# ------------------------------------------------------------

# Calculate wRC+ (Weighted Runs Created Plus)
# wRC+ = [(wRAA per PA + lgRPPA) + ((lgRPPA - ballparkFactor * lgRPPA) / lgWRC_per_PA_no_pitchers)] * 100]

print("\nCalculating wRC+...")
df['wRC_per_PA'] = df['wRC'] / df['PA']


df['wRC_plus'] = (((df['wRAA'] / df['PA']) + lgRPPA) + ((lgRPPA - (ballparkFactor * lgRPPA)) / lg_wRC_per_PA)) * 100


# ------------------------------------------------------------

# Display results
print("\nResults:")
print(df[['playerFullName', 'PA', 'wRAA', 'wRC', 'wRC_per_PA', 'wRC_plus']].head(10))

# ------------------------------------------------------------



# Summary statistics
print(f"\nSummary Statistics:")
print(f"wRC+ Mean: {df['wRC_plus'].mean():.1f}")
print(f"wRC+ Median: {df['wRC_plus'].median():.1f}")
print(f"wRC+ Std Dev: {df['wRC_plus'].std():.1f}")


# ------------------------------------------------------------



# Save results to new CSV
output_file = '/Users/andrewhlavacek/Downloads/vipwrc+/wrc.csv'
df.to_csv(output_file, index=False)
print(f"\nResults saved to: {output_file}")