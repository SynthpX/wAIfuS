from transformers import pipeline


class EmotionRecognizer:
    def __init__(self):
        self.emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
    def recognize_emotions(self, texts):
        if not isinstance(texts, list):
            texts = [texts]
        emotion_labels = self.emotion_pipeline(texts)
        return emotion_labels

if __name__ == '__main__':
    emotion_recognizer = EmotionRecognizer()

    texts = [
        "I dont want to go with you",
        "I'm so happy today!",
        "This is very frustrating."
    ]

    try:
        emotion_labels = emotion_recognizer.recognize_emotions(texts)
        for text, label in zip(texts, emotion_labels):
            print(f"Text: {text}\nRecognized emotions: {label}\n")
    except Exception as e:
        print("Error occurred while processing the text:", e)