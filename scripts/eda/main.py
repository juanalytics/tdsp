import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set(style="whitegrid")

# Paths
processed_dir = os.path.join(os.path.dirname(__file__), '../../data/processed')
main_files = [
    'student_consolidated.csv',
    'student_info_clean.csv'
]

# Try to load the most consolidated file
for fname in main_files:
    fpath = os.path.join(processed_dir, fname)
    if os.path.exists(fpath):
        df = pd.read_csv(fpath)
        print(f"Loaded {fname} with shape {df.shape}")
        break
else:
    raise FileNotFoundError("No main processed student file found in data/processed/")

# Print general info
print("\n--- DataFrame Info ---")
df.info()
print("\n--- Head ---")
print(df.head())
print("\n--- Describe ---")
print(df.describe(include='all'))

# Value counts for key columns
key_cols = [
    'gender', 'final_result', 'age_band', 'highest_education', 'region', 'disability'
]
for col in key_cols:
    if col in df.columns:
        print(f"\n--- Value counts for {col} ---")
        print(df[col].value_counts(dropna=False))

# Plot directory
plot_dir = os.path.join(os.path.dirname(__file__), '../../docs/data/eda_plots')
os.makedirs(plot_dir, exist_ok=True)

# Plot categorical distributions
for col in key_cols:
    if col in df.columns:
        plt.figure(figsize=(6,4))
        sns.countplot(data=df, x=col, order=df[col].value_counts().index)
        plt.title(f'Distribution of {col}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(plot_dir, f'{col}_countplot.png'))
        plt.close()

# Plot histogram for numeric columns
num_cols = df.select_dtypes(include='number').columns
for col in num_cols:
    plt.figure(figsize=(6,4))
    sns.histplot(df[col].dropna(), kde=True, bins=30)
    plt.title(f'Distribution of {col}')
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, f'{col}_hist.png'))
    plt.close()

# Correlation heatmap
if len(num_cols) > 1:
    plt.figure(figsize=(10,8))
    corr = df[num_cols].corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', square=True)
    plt.title('Correlation Heatmap (Numeric Features)')
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'correlation_heatmap.png'))
    plt.close()

# Pairplot for selected variables (if not too many rows)
if len(num_cols) > 1 and df.shape[0] <= 2000:
    try:
        sns.pairplot(df[num_cols.union(key_cols)], hue='final_result' if 'final_result' in df.columns else None)
        plt.savefig(os.path.join(plot_dir, 'pairplot.png'))
        plt.close()
    except Exception as e:
        print(f"Pairplot could not be generated: {e}")

# Visualize missing values
try:
    import missingno as msno
    plt.figure()
    msno.matrix(df)
    plt.title('Missing Values Matrix')
    plt.savefig(os.path.join(plot_dir, 'missing_matrix.png'))
    plt.close()
    plt.figure()
    msno.heatmap(df)
    plt.title('Missing Values Heatmap')
    plt.savefig(os.path.join(plot_dir, 'missing_heatmap.png'))
    plt.close()
except ImportError:
    print("missingno not installed, skipping missing value visualizations.")

# Outlier detection (IQR method)
outlier_report = []
for col in num_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)][col]
    outlier_report.append({
        'column': col,
        'num_outliers': outliers.count(),
        'percent_outliers': 100 * outliers.count() / len(df),
        'lower_bound': lower,
        'upper_bound': upper
    })

# Save EDA summary as markdown
eda_report_path = os.path.join(os.path.dirname(__file__), '../../docs/data/eda_summary.md')
with open(eda_report_path, 'w', encoding='utf-8') as f:
    f.write(f"# EDA Summary\n\n")
    f.write(f"## Data Shape\nRows: {df.shape[0]}, Columns: {df.shape[1]}\n\n")
    f.write(f"## Numeric Columns\n{list(num_cols)}\n\n")
    f.write(f"## Categorical Columns\n{[col for col in key_cols if col in df.columns]}\n\n")
    f.write(f"## Outlier Report\n")
    for item in outlier_report:
        f.write(f"- {item['column']}: {item['num_outliers']} outliers ({item['percent_outliers']:.2f}%), bounds=({item['lower_bound']:.2f}, {item['upper_bound']:.2f})\n")
    f.write(f"\n## Plots\n")
    for col in key_cols:
        if col in df.columns:
            f.write(f"- ![Distribution of {col}](eda_plots/{col}_countplot.png)\n")
    for col in num_cols:
        f.write(f"- ![Distribution of {col}](eda_plots/{col}_hist.png)\n")
    if len(num_cols) > 1:
        f.write(f"- ![Correlation Heatmap](eda_plots/correlation_heatmap.png)\n")
    if os.path.exists(os.path.join(plot_dir, 'pairplot.png')):
        f.write(f"- ![Pairplot](eda_plots/pairplot.png)\n")
    if os.path.exists(os.path.join(plot_dir, 'missing_matrix.png')):
        f.write(f"- ![Missing Matrix](eda_plots/missing_matrix.png)\n")
    if os.path.exists(os.path.join(plot_dir, 'missing_heatmap.png')):
        f.write(f"- ![Missing Heatmap](eda_plots/missing_heatmap.png)\n")

print(f"\nEDA plots and summary saved to {plot_dir} and {eda_report_path}")
