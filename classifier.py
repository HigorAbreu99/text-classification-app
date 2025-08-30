from transformers import pipeline

classifier = pipeline("sentiment-analysis")

text = "We are very happy to show you the 🤗 Transformers library."

result = classifier(text)

print(result)