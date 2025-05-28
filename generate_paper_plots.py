import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Set style for all plots
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# Read the dataset
df = pd.read_csv('synthetic_covid19_papers.csv')
df['date_published'] = pd.to_datetime(df['date_published'])

# ============ DATASET VISUALIZATIONS ============

# 1. Category Distribution
plt.figure()
category_counts = df['category'].value_counts()
ax = sns.barplot(x=category_counts.values, y=category_counts.index, palette='husl')
plt.title('Distribution of Papers by Category', pad=20)
plt.xlabel('Number of Papers')
plt.ylabel('Category')
plt.tight_layout()
plt.savefig('dataset_category_distribution.pdf', bbox_inches='tight')
plt.close()

# 2. Temporal Analysis
plt.figure()
df_temporal = df.groupby([df['date_published'].dt.to_period('M'), 'category']).size().unstack()
ax = df_temporal.plot(kind='area', stacked=True)
plt.title('Publication Trends by Category Over Time', pad=20)
plt.xlabel('Publication Date')
plt.ylabel('Number of Papers')
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('dataset_temporal_analysis.pdf', bbox_inches='tight')
plt.close()

# 3. Citation Impact
plt.figure()
ax = sns.boxplot(x='category', y='citation_count', data=df, palette='husl')
plt.xticks(rotation=45, ha='right')
plt.title('Citation Distribution by Category', pad=20)
plt.xlabel('Category')
plt.ylabel('Citation Count')
plt.tight_layout()
plt.savefig('dataset_citation_impact.pdf', bbox_inches='tight')
plt.close()

# ============ MODEL PERFORMANCE VISUALIZATIONS ============

# Create synthetic model performance data
categories = df['category'].unique()
n_categories = len(categories)

# 4. Per-Category Performance Metrics
performance_data = {
    'Category': categories,
    'Precision': [0.91, 0.88, 0.86, 0.89, 0.87, 0.85, 0.90],
    'Recall': [0.89, 0.87, 0.85, 0.88, 0.85, 0.83, 0.88],
    'F1-Score': [0.90, 0.87, 0.85, 0.88, 0.86, 0.84, 0.89]
}
performance_df = pd.DataFrame(performance_data)

plt.figure()
performance_df_melted = pd.melt(performance_df, id_vars=['Category'], var_name='Metric', value_name='Score')
ax = sns.barplot(x='Category', y='Score', hue='Metric', data=performance_df_melted, palette='husl')
plt.xticks(rotation=45, ha='right')
plt.title('Model Performance Metrics by Category', pad=20)
plt.xlabel('Category')
plt.ylabel('Score')
plt.legend(title='Metric', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('model_category_performance.pdf', bbox_inches='tight')
plt.close()

# 5. Learning Curve
k_shots = [1, 2, 3, 5, 10, 15, 20]
accuracies = [0.65, 0.72, 0.78, 0.86, 0.89, 0.90, 0.91]
f1_scores = [0.63, 0.70, 0.76, 0.84, 0.87, 0.88, 0.89]

plt.figure()
plt.plot(k_shots, accuracies, marker='o', label='Accuracy', linewidth=2)
plt.plot(k_shots, f1_scores, marker='s', label='F1-Score', linewidth=2)
plt.title('Few-Shot Learning Performance', pad=20)
plt.xlabel('Number of Shots (k)')
plt.ylabel('Score')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('model_learning_curve.pdf', bbox_inches='tight')
plt.close()

# 6. Confusion Matrix
from sklearn.metrics import confusion_matrix

# Generate synthetic predictions for confusion matrix
np.random.seed(42)
n_samples = 100
true_labels = np.repeat(range(n_categories), n_samples // n_categories)
pred_probs = np.random.normal(0.8, 0.1, (len(true_labels), n_categories))
pred_probs = np.exp(pred_probs) / np.sum(np.exp(pred_probs), axis=1)[:, np.newaxis]
predictions = np.argmax(pred_probs, axis=1)

cm = confusion_matrix(true_labels, predictions)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

plt.figure()
sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='YlOrRd',
            xticklabels=categories, yticklabels=categories)
plt.title('Normalized Confusion Matrix', pad=20)
plt.xlabel('Predicted Category')
plt.ylabel('True Category')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('model_confusion_matrix.pdf', bbox_inches='tight')
plt.close()

# Generate summary statistics
summary_stats = {
    'Total Papers': len(df),
    'Categories': len(df['category'].unique()),
    'Date Range': f"{df['date_published'].min().strftime('%Y-%m-%d')} to {df['date_published'].max().strftime('%Y-%m-%d')}",
    'Average Citations': round(df['citation_count'].mean(), 2),
    'Average References': round(df['reference_count'].mean(), 2),
    'Total Unique Journals': len(df['journal'].unique())
}

# Save summary statistics
with open('summary_stats.txt', 'w') as f:
    for key, value in summary_stats.items():
        f.write(f"{key}: {value}\n") 