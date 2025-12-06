from viral_predictor import load_model_and_tokenizer, predict_viral, predict_viral_simple, predict_viral_score

print(" Инициализация модели...")
load_model_and_tokenizer(
    model_path='models/complete_model.keras',
    tokenizer_path='tokenizers/tokenizer.pkl'
)

text1 = "A phase-locked loop or phase lock loop (PLL) is a control system that generates an output signal whose phase is fixed relative to the phase of an input signal."
result1 = predict_viral(text1)
print("\n Пример 1 (полный результат):")
print(f"   Текст: {result1['text_sample']}")
print(f"   Вероятность: {result1['probability']:.3f}")
print(f"   Виральный? {result1['viral']}")
print(f"   Сообщение: {result1['message']}")

text2 = "This life hack will change your life"
result2 = predict_viral(text2)
print("\n Пример 1 (полный результат):")
print(f"   Текст: {result2['text_sample']}")
print(f"   Вероятность: {result2['probability']:.3f}")
print(f"   Виральный? {result2['viral']}")
print(f"   Сообщение: {result2['message']}")
