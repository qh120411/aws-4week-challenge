from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split

base_dir = Path(__file__).resolve().parent
data_path = base_dir / "data" / "intents.csv"
model_path = base_dir / "model" / "model.joblib"

def main():
    #Load dataset
    df = pd.read_csv(data_path)
    df = df.dropna(subset=["text", "intent"])

    df["text"] = df["text"].astype(str).str.strip()
    df["intent"] = df["intent"].astype(str).str.strip()
    
    df = df[(df["text"] != "") & (df["intent"] != "")]
    
    # check trunng
    conflicts = df.groupby("text")["intent"].nunique()
    if (conflicts > 1).any():
        raise ValueError("Có câu giống nhưng mang nhiều nhãn."
                         " Kiểm tra lại dữ liệu đầu vào.")
        
    # Loai trùng các dữ liệu
    df = df.drop_duplicates(subset=["text"])
    
    #dem truong hop intent
    count = df["intent"].value_counts()
    print("Số lượng intent: ", len(count))
    
    if len(count) < 2:
        raise ValueError("Số lượng intent phải lớn hơn 1 để phân loại.")
    
    if count.min() < 5:
        raise ValueError("Mỗi intent cần ít nhất 5 mẫu để phân loại.")
    
    #chia train/test
    test_size = max(len(count), round(len(df) * 0.2))
    
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"],
        df["intent"],
        test_size=test_size,
        random_state=42,
        stratify=df["intent"],
    )
    
    #ghép chuyển vb và phân loại
    model = Pipeline([('tfidf', TfidfVectorizer(ngram_range = (1,2), lowercase = True)),
                      ('classifier', LogisticRegression(C = 30, max_iter = 1000)), ])
    
    #start
    model.fit(X_train, y_train)
    
    
    #đánh giá
    predictions = model.predict(X_test)
    print("Accuracy: ", accuracy_score(y_test, predictions))
    print(classification_report(y_test, predictions, zero_division=0))
    
    #lưu model
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    
    print("Model đã được lưu tại: ", model_path)


if __name__ == "__main__":
    main()
    
    
                     
    