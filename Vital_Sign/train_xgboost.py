import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# ✅ Load dataset
df = pd.read_csv("/Users/harisatyam/Documents/Vital_Sign_Monitoring_Alert_Notification/human_vital_signs_dataset_2024.csv")  # Ensure this file exists in the same directory
df.dropna(inplace=True)  # Remove missing values

# ✅ Encode categorical labels
label_encoder = LabelEncoder()
df["Risk Category"] = label_encoder.fit_transform(df["Risk Category"])

# ✅ Select features and target variable
X = df[['Heart Rate', 'Respiratory Rate', 'Body Temperature', 'Oxygen Saturation', 'Systolic Blood Pressure', 'Diastolic Blood Pressure']]
y = df["Risk Category"]

# ✅ Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ✅ Split dataset
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ✅ Train XGBoost model
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="mlogloss")
model.fit(X_train, y_train)

# ✅ Save the model in JSON format
model.save_model("app/xgboost_vital_signs_model.json")

# ✅ Save scaler and label encoder
joblib.dump(scaler, "app/scaler.pkl")
joblib.dump(label_encoder, "app/label_encoder.pkl")

print("✅ Model, scaler, and label encoder saved successfully!")