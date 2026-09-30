# 🎓 Student Academic Performance Prediction System

A machine learning project that predicts student academic performance using demographic, academic, attendance, and behavioral features.

The system generates synthetic student data, performs exploratory data analysis, trains multiple machine learning models, evaluates their performance, and automatically identifies the best-performing model.

## 🚀 Project Overview

The **Student Academic Performance Prediction System** demonstrates an end-to-end machine learning workflow:

**Data Generation → Data Exploration → Visualization → Model Training → Model Evaluation → Prediction → Risk Classification**

The project is designed as an academic AIML project to demonstrate practical applications of machine learning in education analytics.

## ✨ Features

* Generate synthetic student academic datasets
* Perform exploratory data analysis
* Analyze relationships between student features
* Train multiple regression models
* Compare model performance
* Calculate:

  * R² Score
  * RMSE
  * MAE
* Automatically select the best-performing model
* Generate prediction accuracy visualizations
* Perform residual analysis
* Classify students based on academic risk
* Generate visual reports

## 🤖 Machine Learning Models

The project uses three regression algorithms:

1. **Linear Regression**
2. **Random Forest Regressor**
3. **Gradient Boosting Regressor**

The models are evaluated using R², RMSE, and MAE.

### Model Results

| Model             | R² Score |   RMSE |    MAE |
| ----------------- | -------: | -----: | -----: |
| Linear Regression |   0.8924 | 2.9667 | 2.3353 |
| Random Forest     |   0.8082 | 3.9607 | 3.2661 |
| Gradient Boosting |   0.8253 | 3.7797 | 3.0503 |

The results shown above are from the project's current execution.

## 📊 Visualizations

The project generates the following visualizations:

* Correlation Heatmap
* Feature Distribution
* Scatter Relationships
* Model Comparison
* Prediction Accuracy
* Residual Analysis
* Risk Classification

## 🛠️ Technologies Used

* **Python**
* **NumPy**
* **Pandas**
* **Matplotlib**
* **Seaborn**
* **Scikit-learn**

## 📁 Project Structure

```text
aiml-project/
│
├── student_performance_system.py
├── generate_word_report.py
├── requirements.txt
├── report_style_notes.txt
├── toc_style_notes.txt
├── README.md
│
├── correlation_heatmap.png
├── feature_distribution.png
├── scatter_relationships.png
├── model_comparison.png
├── prediction_accuracy_linear_regression.png
├── residual_analysis_linear_regression.png
└── risk_classification.png
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/ashishdhanala/aiml-project.git
```

Move into the project directory:

```bash
cd aiml-project
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Project

Run:

```bash
python student_performance_system.py
```

The program will generate the dataset, train the machine learning models, evaluate them, and create the visualization files.

## 📈 Output

The system produces:

* Model performance metrics
* Student performance predictions
* Academic risk classification
* Data analysis visualizations
* Model comparison results
* Prediction accuracy plots
* Residual analysis

## 🎯 Learning Objectives

This project demonstrates practical understanding of:

* Python programming
* Data preprocessing
* Exploratory Data Analysis
* Data visualization
* Regression
* Machine learning model training
* Model evaluation
* Feature analysis
* Academic performance prediction

## 👨‍💻 Author

**Ashish Dhanala**

B.Tech Computer Science Engineering

GitHub: [ashishdhanala](https://github.com/ashishdhanala)

---

⭐ If you find this project useful, feel free to explore the repository.
