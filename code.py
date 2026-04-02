import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── 1. LOAD ──────────────────────────────────────────────────────────────────
internet = pd.read_csv(r"C:\Users\abdel\Downloads\internet_access_cleaned.csv")
gdp      = pd.read_csv(r"C:\Users\abdel\OneDrive\Desktop\BS\africa15_gdp.csv")
turnout  = pd.read_csv(r"C:\Users\abdel\OneDrive\Desktop\BS\africa15_voter_turnout.csv")

# ── 2. PREVIEW ───────────────────────────────────────────────────────────────
print("=== Internet ==="); print(internet.head()); print(internet.columns.tolist())
print("=== GDP ===");      print(gdp.head());      print(gdp.columns.tolist())
print("=== Turnout ===");  print(turnout.head());  print(turnout.columns.tolist())

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── 1. LOAD ───────────────────────────────────────────────────────────────────
internet = pd.read_csv(r"C:\Users\abdel\Downloads\internet_access_cleaned.csv")
gdp      = pd.read_csv(r"C:\Users\abdel\OneDrive\Desktop\BS\africa15_gdp.csv")
turnout  = pd.read_csv(r"C:\Users\abdel\OneDrive\Desktop\BS\africa15_voter_turnout.csv")

# ── 2. STANDARDISE COLUMN NAMES ───────────────────────────────────────────────
internet = internet.rename(columns={
    "Country Name":       "country",
    "Country Code":       "code",
    "Year":               "year",
    "Internet_Users_Pct": "internet_pct",
    "Region":             "region",
    "IncomeGroup":        "income_group"
})

gdp = gdp.rename(columns={
    "Country Name":              "country",
    "Country Code":              "code",
    "Region":                    "region",
    "IncomeGroup":               "income_group",
    "GDP_per_capita_USD_2023":   "gdp_per_capita",
    "GDP_total_billion_USD_2023":"gdp_total",
    "GDP_growth_pct_2023":       "gdp_growth",
    "Year":                      "year"
})

turnout = turnout.rename(columns={
    "Country Name":       "country",
    "Country Code":       "code",
    "Region":             "region",
    "Election_Type":      "election_type",
    "Election_Year":      "year",
    "Registered_Voters_M":"registered_voters",
    "Voter_Turnout_Pct":  "turnout_pct"
})

# ── 3. MERGE ──────────────────────────────────────────────────────────────────
# Internet has yearly data — get the value closest to each election year
# Merge internet + turnout on country & year
df = turnout.merge(internet[["country", "code", "year", "internet_pct"]],
                   on=["country", "code", "year"], how="left")

# GDP is 2023-only snapshot — merge on country/code only (no year)
df = df.merge(gdp[["country", "code", "gdp_per_capita", "gdp_total", "gdp_growth"]],
              on=["country", "code"], how="left")

print(f"\nMerged shape: {df.shape}")
print(df.head(10))

# ── 4. CLEAN ──────────────────────────────────────────────────────────────────
print("\n--- Missing values before cleaning ---")
print(df.isnull().sum())

# If internet_pct is missing for election year, fill with nearest available year
for idx, row in df[df["internet_pct"].isna()].iterrows():
    country_data = internet[internet["code"] == row["code"]].copy()
    if not country_data.empty:
        closest = country_data.iloc[(country_data["year"] - row["year"]).abs().argsort()[:1]]
        df.at[idx, "internet_pct"] = closest["internet_pct"].values[0]

# Drop rows still missing key variables
df = df.dropna(subset=["internet_pct", "turnout_pct"])

# Keep percentages in valid range
df = df[(df["internet_pct"].between(0, 100)) &
        (df["turnout_pct"].between(0, 100))]

print("\n--- Missing values after cleaning ---")
print(df.isnull().sum())
print(f"\nClean dataset: {df.shape[0]} rows")
print(df[["country", "year", "internet_pct", "turnout_pct"]].to_string())

# ── 5. VISUALISE ──────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid")

# 5a. Scatter: internet access vs voter turnout
fig, ax = plt.subplots(figsize=(9, 6))
for _, row in df.iterrows():
    ax.scatter(row["internet_pct"], row["turnout_pct"], s=80,
               alpha=0.8, edgecolors="k", linewidths=0.4)
    ax.annotate(row["country"], (row["internet_pct"], row["turnout_pct"]),
                fontsize=7, ha="left", va="bottom")
ax.set_xlabel("Internet Users (%) at Election Year")
ax.set_ylabel("Voter Turnout (%)")
ax.set_title("Internet Access vs Voter Turnout by Country")
plt.tight_layout()
plt.savefig("scatter_internet_turnout.png", dpi=150)
plt.show()

# 5b. Regression trend line
fig, ax = plt.subplots(figsize=(9, 6))
sns.regplot(data=df, x="internet_pct", y="turnout_pct",
            scatter_kws={"alpha": 0.6, "s": 80},
            line_kws={"color": "red"}, ax=ax)
ax.set_xlabel("Internet Users (%) at Election Year")
ax.set_ylabel("Voter Turnout (%)")
ax.set_title("Internet Access vs Voter Turnout — Trend Line")
plt.tight_layout()
plt.savefig("regplot_internet_turnout.png", dpi=150)
plt.show()

# 5c. Horizontal bar chart — turnout ranked by internet access
df_sorted = df.sort_values("internet_pct", ascending=True)
fig, axes = plt.subplots(1, 2, figsize=(14, 7), sharey=True)
axes[0].barh(df_sorted["country"], df_sorted["internet_pct"], color="steelblue")
axes[0].set_xlabel("Internet Users (%)")
axes[0].set_title("Internet Access")
axes[1].barh(df_sorted["country"], df_sorted["turnout_pct"], color="coral")
axes[1].set_xlabel("Voter Turnout (%)")
axes[1].set_title("Voter Turnout")
fig.suptitle("Internet Access vs Voter Turnout by Country", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("bar_by_country.png", dpi=150)
plt.show()

# ── 6. SAVE ───────────────────────────────────────────────────────────────────
df.to_csv(r"C:\Users\abdel\OneDrive\Desktop\BS\merged_internet_turnout.csv", index=False)
print("\n✅ Merged CSV saved.")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

# ── REGRESSION ANALYSIS ───────────────────────────────────────────────────────

# Simple Linear Regression (scipy)
slope, intercept, r_value, p_value, std_err = stats.linregress(
    df["internet_pct"], df["turnout_pct"]
)

print("═══════════════════════════════════════")
print("       LINEAR REGRESSION RESULTS       ")
print("═══════════════════════════════════════")
print(f"  Slope (β1):       {slope:.4f}")
print(f"  Intercept (β0):   {intercept:.4f}")
print(f"  R²:               {r_value**2:.4f}")
print(f"  R (correlation):  {r_value:.4f}")
print(f"  P-value:          {p_value:.4f}")
print(f"  Std Error:        {std_err:.4f}")
print("═══════════════════════════════════════")

# Interpretation
print("\n📊 INTERPRETATION:")
print(f"  → For every 1% increase in internet access,")
print(f"    voter turnout changes by {slope:.2f}%")
print(f"  → R² = {r_value**2:.4f} means internet access explains")
print(f"    {r_value**2 * 100:.1f}% of the variance in voter turnout")
if p_value < 0.05:
    print(f"  → P-value = {p_value:.4f} → relationship is STATISTICALLY SIGNIFICANT ✅")
else:
    print(f"  → P-value = {p_value:.4f} → relationship is NOT significant ❌")

# ── PLOT ──────────────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 6))

# Scatter points with country labels
sns.scatterplot(data=df, x="internet_pct", y="turnout_pct",
                s=100, color="steelblue", edgecolor="k", linewidth=0.5, ax=ax)

# Annotate each country
for _, row in df.iterrows():
    ax.annotate(row["country"],
                xy=(row["internet_pct"], row["turnout_pct"]),
                xytext=(5, 3), textcoords="offset points", fontsize=8)

# Regression line
x_line = np.linspace(df["internet_pct"].min(), df["internet_pct"].max(), 100)
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, color="red", linewidth=2, label="Regression line")

# Confidence interval band
sns.regplot(data=df, x="internet_pct", y="turnout_pct",
            scatter=False, ci=95,
            line_kws={"alpha": 0},
            scatter_kws={"alpha": 0},
            ax=ax)

# Equation & R² on chart
ax.text(0.05, 0.95,
        f"y = {slope:.2f}x + {intercept:.2f}\nR² = {r_value**2:.3f}   p = {p_value:.3f}",
        transform=ax.transAxes, fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

ax.set_xlabel("Internet Users (%) at Election Year", fontsize=12)
ax.set_ylabel("Voter Turnout (%)", fontsize=12)
ax.set_title("Linear Regression: Internet Access vs Voter Turnout", fontsize=13, fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig("regression_analysis.png", dpi=150)
plt.show()