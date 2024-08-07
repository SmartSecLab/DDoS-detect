import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file into a DataFrame
df = pd.read_csv("Data/labeled_db.csv", parse_dates=["Timestamp"])

# Define the desired order of features within each bar group
desired_feature_order = ['Unique-IPs',
                         'Num-sockets', 'Upload-speed', 'Download-speed']

# Ensure the selected features are present in the dataset
features = [feature for feature in desired_feature_order if feature in df.columns]

# Apply a logarithmic scale to the features (adding a small constant to avoid log(0))
df[features] = np.log1p(df[features])

# Define consistent colors for each feature
feature_colors = plt.cm.tab10.colors[:len(features)]

SMALL_SIZE = 16
MEDIUM_SIZE = 18
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels


# Create a grouped bar chart for each feature
fig, ax = plt.subplots(figsize=(10, 8))

bar_width = 0.15
positions = np.arange(len(df['Attack-type'].unique()))

# Iterate over attack types and plot each one side by side for each feature
for i, Attack_type in enumerate(df['Attack-type'].unique()):
    attack_data = df[df['Attack-type'] == Attack_type][features]

    # Plot bars for each feature with consistent colors and desired order
    bars = ax.bar(i + np.arange(len(features)) * bar_width,
                  attack_data[desired_feature_order].mean(), width=bar_width, color=feature_colors, alpha=0.7)

    # Add markers for the 25th and 75th percentiles
    ax.errorbar(i + np.arange(len(features)) * bar_width + bar_width / 2,
                attack_data[desired_feature_order].median(),
                yerr=[attack_data[feature].median() - attack_data[feature].quantile(0.25)
                      for feature in desired_feature_order],
                fmt='o', color='black', markersize=8, capsize=5, label='_nolegend_')

# Create a legend with consistent colors and feature labels
# ax.legend(bars, desired_feature_order, title='Features',
#           loc='best', bbox_to_anchor=(1, 1))
ax.legend(bars, desired_feature_order, loc='upper right')
ax.set_ylabel('Logarithmic Scale of Feature Values')
plt.yscale('log')  # Use logarithmic scale for the Y-axis
plt.xlabel('Traffic Type')
plt.xticks(np.arange(len(df['Attack-type'].unique())) + (bar_width * (
    len(features) - 1) / 2), [att_type for att_type in df['Attack-type'].unique()])
plt.xticks(rotation=45, ha='right')
plt.tight_layout()  # Adjust the subplot layout

fig.savefig('figure/ddos-net.png')
plt.show()
