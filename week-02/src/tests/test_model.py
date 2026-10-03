from pathlib import Path
import joblib

base_dir = Path(__file__).resolve().parent.parent
model_path = base_dir / "model" / "model.joblib"

def main():
    # Nạp model đã huấn luyện
    model = joblib.load(model_path)

    # Cho phép nhập nhiều câu để thử
    while True:
        text = input("\nNhập câu hỏi (gõ exit để thoát): ").strip()

        if text.lower() == "exit":
            break

        if not text:
            print("Bạn chưa nhập câu hỏi.")
            continue

        probabilities = model.predict_proba([text])[0]
        best_index = probabilities.argmax()
        intent = model.classes_[best_index]
        confidence = probabilities[best_index]

        print(f"Intent dự đoán: {intent} (Độ tin cậy: {confidence:.2f})")
        if confidence < 0.15:
            print("Model chưa thật sự chắc chắn. Bạn có thể thử diễn đạt lại.")


if __name__ == "__main__":
    main()