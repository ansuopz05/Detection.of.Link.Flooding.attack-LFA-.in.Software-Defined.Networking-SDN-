
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

print("=" * 50)
print("   LFA DETECTION VISUALIZATION")
print("=" * 50)

csv_files = glob.glob('/home/ansuman/lfa_project/ICMP_ATTACK_DATASET.csv')

if not csv_files:
    print("Dataset not found!")
    exit()

target_file = csv_files[0]

print(f"\n[1] File: {os.path.basename(target_file)}")

df = pd.read_csv(target_file)

df.columns = df.columns.str.strip()

df = df.dropna()

print(f"Shape after removing NaN: {df.shape}")

label_col = df.columns[-1]

df[label_col] = (
    df[label_col]
    .astype(str)
    .str.strip()
)

df[label_col] = df[label_col].replace({
    'DDOS': 'LFA Attack',
    'NORMAL': 'Normal Traffic'
})

print("\n[2] Label distribution:")
print(df[label_col].value_counts())

plt.figure(figsize=(7, 5))

counts = df[label_col].value_counts()

colors = [
    'red' if 'Attack' in str(x)
    else 'steelblue'
    for x in counts.index
]

counts.plot(
    kind='bar',
    color=colors,
    edgecolor='black'
)

plt.title(
    'Normal Traffic vs LFA Attack\nDetection Count',
    fontsize=13
)

plt.ylabel('Number of Samples')
plt.xlabel('Traffic Type')
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    '/home/ansuman/lfa_project/detection_count.png',
    dpi=150
)

print("\n[3] detection_count.png saved!")

numeric_cols = (
    df.select_dtypes(
        include=['number']
    )
    .columns
    .tolist()[:2]
)

if len(numeric_cols) >= 2:

    scatter_df = df.dropna(
        subset=numeric_cols
    )

    plt.figure(figsize=(10, 5))

    for label in scatter_df[label_col].unique():

        subset = (
            scatter_df[
                scatter_df[label_col] == label
            ]
        )

        color = (
            'red'
            if 'Attack' in str(label)
            else 'steelblue'
        )

        plt.scatter(
            subset[numeric_cols[0]],
            subset[numeric_cols[1]],
            s=5,
            alpha=0.4,
            color=color,
            label=label
        )

    plt.xlabel(numeric_cols[0])
    plt.ylabel(numeric_cols[1])

    plt.title(
        'Traffic Scatter — Normal vs LFA Attack'
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        '/home/ansuman/lfa_project/traffic_scatter.png',
        dpi=150
    )

    print("[4] traffic_scatter.png saved!")

plt.figure(figsize=(8, 5))

df[label_col].value_counts().plot(
    kind='pie',
    autopct='%1.1f%%',
    colors=['steelblue', 'red'],
    startangle=90
)

plt.title(
    'Traffic Distribution — LFA Dataset'
)

plt.ylabel('')

plt.tight_layout()

plt.savefig(
    '/home/ansuman/lfa_project/traffic_pie.png',
    dpi=150
)

print("[5] traffic_pie.png saved!")

print("\n=== ALL DONE ===")
print("Files saved:")
print("detection_count.png")-
print("traffic_pie.png")
