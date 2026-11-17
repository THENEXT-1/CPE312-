from pathlib import Path
import joblib
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "model.pkl"

def main():
    data = fetch_california_housing(as_frame=False)
    X_train, _, y_train, _ = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"บันทึกโมเดลเรียบร้อยที่ {MODEL_PATH}")

if __name__ == "__main__":
    main()
