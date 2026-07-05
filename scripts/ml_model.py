"""
ml_model.py
Predicts Layoff Severity (Low / Medium / High) using a Random Forest classifier.
Outputs:
  - visuals/11_feature_importance.png
  - visuals/12_confusion_matrix.png
  - models/rf_model_report.txt
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (classification_report, confusion_matrix,
                              accuracy_score, ConfusionMatrixDisplay)
from sklearn.pipeline import Pipeline
import warnings
import os

warnings.filterwarnings("ignore")
os.makedirs("visuals", exist_ok=True)
os.makedirs("models", exist_ok=True)

# ── Load & Preprocess ─────────────────────────────────────────────────────────
df = pd.read_csv("data/tech_layoffs.csv")

# Fill missing stock impact with 0 (non-public companies)
df["stock_impact_pct"] = df["stock_impact_pct"].fillna(0.0)
df["is_public"] = (df["stage"] == "Public").astype(int)

# Encode categoricals
cat_cols = ["industry", "country", "stage", "reason"]
le_dict = {}
for col in cat_cols:
    le = LabelEncoder()
    df[col + "_enc"] = le.fit_transform(df[col])
    le_dict[col] = le

feature_cols = [
    "industry_enc", "country_enc", "stage_enc", "reason_enc",
    "year", "month", "company_size", "funds_raised_m",
    "stock_impact_pct", "is_public"
]

X = df[feature_cols]
y = df["severity"]

# ── Train/Test Split ──────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Random Forest Model ───────────────────────────────────────────────────────
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    min_samples_split=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
cv_scores = cross_val_score(rf, X, y, cv=StratifiedKFold(5), scoring="accuracy")

print(f"Test Accuracy : {acc:.4f}")
print(f"CV Accuracy   : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
print("\nClassification Report:\n", report)

# ── Save model report ─────────────────────────────────────────────────────────
with open("models/rf_model_report.txt", "w") as f:
    f.write("=" * 60 + "\n")
    f.write("  Tech Layoffs — Random Forest Classifier Report\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Target Variable : Layoff Severity (Low / Medium / High)\n")
    f.write(f"Features Used   : {len(feature_cols)}\n")
    f.write(f"Training Samples: {len(X_train)}\n")
    f.write(f"Test Samples    : {len(X_test)}\n\n")
    f.write(f"Test Accuracy   : {acc:.4f}\n")
    f.write(f"CV Accuracy     : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}\n\n")
    f.write("Classification Report:\n")
    f.write(report)
print("Saved: models/rf_model_report.txt")

# ── Plot Feature Importance ───────────────────────────────────────────────────
feat_imp = pd.Series(rf.feature_importances_, index=feature_cols).sort_values()
readable_labels = {
    "industry_enc": "Industry",
    "country_enc": "Country",
    "stage_enc": "Funding Stage",
    "reason_enc": "Layoff Reason",
    "year": "Year",
    "month": "Month",
    "company_size": "Company Size",
    "funds_raised_m": "Funds Raised (M)",
    "stock_impact_pct": "Stock Impact %",
    "is_public": "Is Public Company"
}
feat_imp.index = [readable_labels.get(i, i) for i in feat_imp.index]

fig, ax = plt.subplots(figsize=(9, 6))
colors = ["#1f4e79" if v == feat_imp.max() else
          "#2e75b6" if v >= feat_imp.quantile(0.75) else "#4da6d9"
          for v in feat_imp.values]
bars = ax.barh(feat_imp.index, feat_imp.values, color=colors)
ax.bar_label(bars, labels=[f"{v:.3f}" for v in feat_imp.values],
             padding=3, fontsize=9)
ax.set_title("Random Forest — Feature Importances\n(Predicting Layoff Severity)",
             fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Importance Score")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("visuals/11_feature_importance.png", dpi=150)
plt.close()
print("Saved: visuals/11_feature_importance.png")

# ── Confusion Matrix ──────────────────────────────────────────────────────────
cm = confusion_matrix(y_test, y_pred, labels=["Low", "Medium", "High"])
fig, ax = plt.subplots(figsize=(7, 6))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Low", "Medium", "High"])
disp.plot(ax=ax, cmap="Blues", colorbar=False)
ax.set_title(f"Confusion Matrix  (Accuracy: {acc:.1%})",
             fontsize=13, fontweight="bold", pad=12)
plt.tight_layout()
plt.savefig("visuals/12_confusion_matrix.png", dpi=150)
plt.close()
print("Saved: visuals/12_confusion_matrix.png")
