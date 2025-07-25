import pandas as pd
from pymongo import MongoClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Step 1: Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["ml_app"]
collection = db["food_dataset"]

# Step 2: Load dataset from MongoDB
data = list(collection.find({}, {"_id": 0}))  # Exclude _id
df = pd.DataFrame(data)

# Step 3: Encode categorical columns using LabelEncoder
label_encoders = {}

# Columns to encode (input features + target)
encode_columns = ["mood", "time_of_day", "diet", "food_prediction"]

for col in encode_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Store encoder for reverse mapping

# Step 4: Prepare features (X) and target (y)
X = df.drop(columns=["food_prediction"])
y = df["food_prediction"]

# Step 5: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Train RandomForest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Step 7: Save the model and encoders
joblib.dump(model, "food_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

# Step 8: Evaluate and print accuracy
accuracy = model.score(X_test, y_test)
print(f"✅ Model trained successfully! Accuracy: {accuracy:.2f}")
