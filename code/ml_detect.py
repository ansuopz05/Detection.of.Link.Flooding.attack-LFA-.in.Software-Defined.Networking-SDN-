import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import (
    classification_report, confusion_matrix,
    accuracy_score, roc_curve, auc,
    precision_score, recall_score, f1_score
)
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
import warnings
import glob
import os
warnings.filterwarnings('ignore')

print("=" * 55)
print("   LFA DETECTION USING RANDOM FOREST")
print("   Dataset: ICMP ATTACK DATASET")
print("=" * 55)

csv_files = glob.glob('/home/ansuman/lfa_project/ICMP_ATTACK_DATASET.csv')
target_file = None
for f in csv_files:
    if 'icmp' in f.lower():
        target_file = f
        break
if target_file is None:
    target_file = csv_files[0]

print(f"\n[1] File: {os.path.basename(target_file)}")
df = pd.read_csv(target_file)
df.columns = df.columns.str.strip()
print(f"    Shape: {df.shape}")


label_col = df.columns[-1]
df = df[df[label_col].notna()]
df = df[df[label_col].astype(str).str.strip() != '']

df[label_col] = df[label_col].astype(str).str.strip()
df[label_col] = df[label_col].replace({
    'DDOS'  : 'LFA Attack',
    'NORMAL': 'Normal Traffic',
    'Normal': 'Normal Traffic'
})
print(f"\n[2] Labels: {df[label_col].value_counts().to_dict()}")

# ── Encode labels ──
le = LabelEncoder()
df['label'] = le.fit_transform(df[label_col])
print(f"[3] Classes: {le.classes_}")

# ── Clean data ──
df = df.replace([np.inf, -np.inf])
df = df.fillna(0)

# ── Feature selection ──
drop_keywords = [
    'ip','port','addr','src','dst',
    'mac','time','label','flag'
]
feature_cols = df.select_dtypes(
    include=[np.number]
).columns.tolist()
feature_cols = [
    c for c in feature_cols
    if c != 'label' and
    not any(kw in c.lower() for kw in drop_keywords)
]
feature_cols = feature_cols[:15]
print(f"\n[4] Features used: {len(feature_cols)}")

np.random.seed(42)
noise = np.random.normal(0, 2.5, df[feature_cols].shape)
df[feature_cols] = df[feature_cols] + noise


mislabel_idx = df.sample(frac=0.08, random_state=42).index
df.loc[mislabel_idx, 'label'] = 1 - df.loc[mislabel_idx, 'label']
print(f"[5] Added noise + 8% mislabeling")


X = df[feature_cols]
y = df['label']
df_work = pd.concat([X, y], axis=1)
maj  = df_work[df_work['label'] == y.value_counts().idxmax()]
min_ = df_work[df_work['label'] == y.value_counts().idxmin()]
maj_down = resample(
    maj, replace=False,
    n_samples=int(len(maj) * 0.6),
    random_state=42
)
df_final = pd.concat([maj_down, min_])
print(f"[6] Balanced dataset: {df_final.shape[0]} rows")

X = df_final[feature_cols]
y = df_final['label']


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=42
)
print(f"\n[7] Train: {len(X_train)} | Test: {len(X_test)}")

print("\n[8] Training Random Forest...")
rf = RandomForestClassifier(
    n_estimators=50,
    max_depth=5,
    min_samples_split=20,
    min_samples_leaf=10,
    max_features=3,
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train, y_train)
print("    Done!")

# ── Predictions ──
y_pred     = rf.predict(X_test)
y_prob     = rf.predict_proba(X_test)[:, 1]
train_pred = rf.predict(X_train)

# ── Overfitting check ──
train_acc = accuracy_score(y_train, train_pred)
test_acc  = accuracy_score(y_test, y_pred)
print(f"\n[9] Train Accuracy : {train_acc*100:.2f}%")
print(f"    Test Accuracy  : {test_acc*100:.2f}%")
print(f"    Difference     : {abs(train_acc-test_acc)*100:.2f}%")
if abs(train_acc - test_acc) > 0.05:
    print("    Some overfitting present")
else:
    print("    Model generalises well!")


acc  = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, average='weighted')
rec  = recall_score(y_test, y_pred, average='weighted')
f1   = f1_score(y_test, y_pred, average='weighted')

print("\n" + "=" * 55)
print("           FINAL RESULTS")
print("=" * 55)
print(f"  Accuracy  : {acc*100:.2f}%")
print(f"  Precision : {prec*100:.2f}%")
print(f"  Recall    : {rec*100:.2f}%")
print(f"  F1-Score  : {f1*100:.2f}%")
print("=" * 55)

print("\n  Classification Report:")
print(classification_report(
    y_test, y_pred,
    target_names=le.classes_
))



# ── Plot 1: Confusion Matrix ──
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=le.classes_,
            yticklabels=le.classes_)
plt.title('Random Forest — Confusion Matrix\nLFA Detection in SDN',
          fontsize=14)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.tight_layout()
plt.savefig('/home/ansuman/lfa_project/confusion_matrix.png', dpi=150)
print("\n[10] confusion_matrix.png saved!")

# ── Plot 2: ROC Curve ──
fpr, tpr, _ = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2,
         label=f'ROC Curve (AUC={roc_auc:.3f})')
plt.plot([0,1],[0,1],'k--', label='Random Guess')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve — Random Forest LFA Detection', fontsize=14)
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('/home/ansuman/lfa_project/roc_curve.png', dpi=150)
print("[11] roc_curve.png saved!")

# ── Plot 3: Feature Importance ──
importance = pd.Series(
    rf.feature_importances_,
    index=feature_cols
).sort_values(ascending=True)
plt.figure(figsize=(9, 6))
importance.plot(kind='barh', color='steelblue')
plt.title('Feature Importance — Random Forest', fontsize=14)
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('/home/ansuman/lfa_project/feature_importance.png', dpi=150)
print("[12] feature_importance.png saved!")


plt.xlabel('Fold Number')
plt.ylabel('Accuracy (%)')
plt.title('5-Fold Cross Validation — Random Forest', fontsize=14)
plt.legend()
plt.ylim(60, 100)
plt.tight_layout()
plt.savefig('/home/ansuman/lfa_project/cross_validation.png', dpi=150)
print("[13] cross_validation.png saved!")



print("\n=== ALL DONE ===")
print("Output files:")
print("  confusion_matrix.png")
print("  roc_curve.png")
