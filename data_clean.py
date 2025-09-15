import pandas as pd

# Read the CSV file
df = pd.read_csv('/Users/andrewhlavacek/Downloads/vip_wrc+/wrc.csv')

# Display basic info about the dataset
print("Dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

# ------------------------------------------------------------


# League averages (these would typically be calculated from the full dataset)
# For demonstration, using sample values - in practice, calculate these from your data
lgWOBA = 0.378
lgWOBA_scale = 1.2
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
df['wRC'] = ((df['wOBA'] - lgWOBA) / lgWOBA + lgRPPA) * df['PA']

# ------------------------------------------------------------



# Calculate league average wRC for wRC+ calculation
# wRC+ = [(wRAA per PA + lgRPPA) + ((lgRPPA - ballparkFactor * lgRPPA) / lgWRC_per_PA_no_pitchers)] * 100


print("Calculating league averages...")
total_wRC = df['wRC'].sum()
total_PA = df['PA'].sum()
lg_wRC_per_PA = total_wRC / total_PA


print(f"League wRC per PA: {lg_wRC_per_PA:.6f}")


# ------------------------------------------------------------

# Calculate wRC+ (Weighted Runs Created Plus)
# wRC+ = (wRC / PA) / (lgwRC / lgPA) * 100
print("\nCalculating wRC+...")
df['wRC_per_PA'] = df['wRC'] / df['PA']
df['wRC_plus'] = (((df['wRAA'] / df['PA']) + lgRPPA) + (lgRPPA - #ballparkFactor * lgRPPA / lgwRC_per_PA)) * 100


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
output_file = '/Users/andrewhlavacek/Downloads/vip_wrc+/wrc_results.csv'
df.to_csv(output_file, index=False)
print(f"\nResults saved to: {output_file}")


