![image](https://github.com/user-attachments/assets/bd0eb635-e45f-48bd-94bd-12734124bd25)# 🎭 Hateful Memes Detection Project

Welcome to the Hateful Memes Detection Project! This repository contains the code and resources for developing deep learning models to classify memes as hateful or not hateful. The project is divided into three tasks: image-only detection, text-only detection, and multimodal detection (combining both image and text). Let's dive in! 🕵️‍♂️

## 📁 Dataset

The dataset for this project consists of hateful and non-hateful memes. You can download it from [here](https://hatefulmemeschallenge.com/#download) after filling out the form. The dataset is organized as follows:
- **Train**: `train.jsonl`
- **Validation**: `dev_seen.jsonl`
- **Test**: `test_seen.jsonl` (use this for performance comparison as it has labels)

For more details, check out:
- [Hateful Memes Challenge by Facebook](https://ai.facebook.com/blog/hateful-memes-challenge-and-data-set/)
- [Research Paper](https://aclanthology.org/2022.findings-naacl.118.pdf)

## 🛠️ Setup

Before running the code, ensure you have the required libraries installed. You can install the dependencies using: pip install -r requirements.txt

## 🖼️ Task I: Image-Only Hateful Meme Detection [20 marks]

### Objective

Develop an image-only detection system to classify memes as hateful or not hateful.

### Steps

1. **Pre-process Images**: Convert images to the appropriate format, normalize, and apply techniques like gray-scaling.
2. **Model Development**: Implement an image classification model using deep learning (e.g., VGG, Vision Transformer, ResNet).
3. **Generate Plots**: Create plots for training/validation loss and accuracy.
4. **Report Metrics**: Report overall accuracy, precision, recall, F1 score, and class-wise metrics for the test set.

# 📝 Task II: Text-Only Hateful Meme Detection [20 marks]

### Objective
Develop a text-only detection system to classify memes as hateful or not hateful.

### Steps
1. **Data Preparation**: Clean, tokenize, and convert text into a suitable format for deep learning models.
2. **Model Development**: Implement a text classification model using deep learning (e.g., BERT, LSTM, XLNet).
3. **Generate Plots**: Create plots for training/validation loss and accuracy.
4. **Report Metrics**: Report overall accuracy, precision, recall, F1 score, and class-wise metrics for the test set.

# 🖼️ + 📝 Task III: Multimodal (Image + Text) Hateful Meme Detection [30 marks]

### Objective
Develop a multimodal detection system to classify memes as hateful or not hateful by combining image and text data.

### Steps
1. **Model Development**: Select and implement a deep learning model architecture for joint image and text classification. Explain the architecture and provide a figure.
2. **Generate Plots**: Create plots for training/validation loss and accuracy.
3. **Report Metrics**: Report overall accuracy, precision, recall, F1 score, and class-wise metrics for the test set.
4. **T-SNE Visualization**: Visualize high-dimensional features into lower-dimensional space for hateful/not hateful classification using T-SNE plots.

# 📊 Evaluation
- **Accuracy**: Measure the overall correctness of the model.
- **Precision**: Measure the accuracy of the positive predictions.
- **Recall**: Measure the ability of the model to capture all positive instances.
- **F1 Score**: Harmonic mean of precision and recall.

# 📈 Plots

### Loss and Accuracy Plots


### T-SNE Plots

![image](https://github.com/user-attachments/assets/f9bf49ed-64ba-43f7-9b06-fa9298830d75)

![image](https://github.com/user-attachments/assets/dbd14900-c8f5-429b-9a58-c7fd7807b853)

![image](https://github.com/user-attachments/assets/5010320e-f48a-4ea8-9066-1524fd595cd2)


