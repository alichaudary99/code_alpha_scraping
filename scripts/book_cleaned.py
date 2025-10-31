import pandas as pd
import matplotlib.pyplot as plt

# ✅ Step 2: Read the scraped CSV file
# Make sure books_scraped_data.csv exists in the same folder
df = pd.read_csv("books_scraped_data.csv")

# ✅ Step 3: Clean the price column
df["price_cleaned"] = (
    df["price"]
    .str.replace("£", "", regex=False)
    .str.replace("Â", "", regex=False)
    .astype(float)
)

# ✅ Step 4: Display basic info
print("\n🔹 Dataset Info:")
print(df.info())

print("\n🔹 First 5 rows:")
print(df.head())

# ✅ Step 5: Basic statistics
print("\n🔹 Summary Statistics:")
print(df["price_cleaned"].describe())

# ✅ Step 6: Plot price distribution
plt.figure(figsize=(8, 5))
plt.hist(df["price_cleaned"], bins=10, edgecolor="black")
plt.title("Distribution of Book Prices")
plt.xlabel("Price (£)")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()

# ✅ Step 7: Save cleaned dataset
df.to_csv("books_cleaned.csv", index=False)
print("\n✅ Cleaned data saved as 'books_cleaned.csv'")
