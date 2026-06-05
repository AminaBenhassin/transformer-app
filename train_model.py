import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# =========================
# 1. PATH
# =========================
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "data", "AGD_Donnes_  classification.xlsx")

# =========================
# 2. LOAD DATA
# =========================
df = pd.read_excel(file_path)
df = df.drop(columns=["NM"])

# =========================
# 3. FEATURE ENGINEERING (VERY IMPORTANT 🔥)
# =========================
gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]

# log transform (stabilizes distribution)
df[gases] = np.log1p(df[gases])

# IEC ratios (core knowledge)
df["R1"] = df["C2H2"] / (df["C2H4"] + 1e-6)
df["R2"] = df["CH4"] / (df["H2"] + 1e-6)
df["R3"] = df["C2H4"] / (df["CH4"] + 1e-6)
df["R4"] = df["C2H6"] / (df["CH4"] + 1e-6)

df["TOTAL"] = df[gases].sum(axis=1)

# =========================
# 4. SPLIT
# =========================
X = df.drop("Diagnostic", axis=1)
y = df["Diagnostic"]

encoder = LabelEncoder()
y = encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# 5. SCALING (help tree stability slightly)
# =========================
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# =========================
# 6. STRONG FINE TREE (PRUNED 🔥)
# =========================
model = DecisionTreeClassifier(
    criterion="entropy",
    max_depth=6,                         # مهم جدًا (prevents overfitting)
    min_samples_split=6,
    min_samples_leaf=3,
    random_state=42
)

# =========================
# 7. CROSS VALIDATION (REAL EVALUATION)
# =========================
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="accuracy")

print("\n CROSS VALIDATION")
print("Mean Accuracy:", cv_scores.mean())
print("Std:", cv_scores.std())

# =========================
# 8. TRAIN FINAL MODEL
# =========================
model.fit(X_train, y_train)

# =========================
# 9. PREDICTION
# =========================
y_pred = model.predict(X_test)

# =========================
# 10. EVALUATION
# =========================
print("\n====================")
print("📊 FINAL RESULTS")
print("====================")

print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:\n")
print(confusion_matrix(y_test, y_pred))

# =========================
# 11. SAVE
# =========================
models_dir = os.path.join(base_dir, "models_saved")
os.makedirs(models_dir, exist_ok=True)

joblib.dump(model, os.path.join(models_dir, "fine_tree_real.pkl"))
joblib.dump(scaler, os.path.join(models_dir, "scaler.pkl"))
joblib.dump(encoder, os.path.join(models_dir, "encoder.pkl"))

print("\n✅ Model saved successfully")