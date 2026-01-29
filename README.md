# Customer Churn Prediction Project

## 📊 Overview
This project focuses on predicting customer churn for a telecommunications company using machine learning techniques. The dataset contains customer information and usage patterns to identify factors that influence customer retention.

## 🎯 Business Objective
- Predict which customers are likely to churn (leave the service)
- Identify key factors contributing to customer churn
- Provide actionable insights for customer retention strategies

## 📁 Dataset
**Source**: WA_Fn-UseC_-Telco-Customer-Churn.csv
- **Size**: 7,043 customers
- **Features**: 20 customer attributes
- **Target**: Churn (Yes/No)

### Key Features:
- **Demographics**: gender, SeniorCitizen, Partner, Dependents
- **Services**: PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies
- **Billing**: Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges
- **Customer Tenure**: tenure (months as customer)

## 🛠️ Technologies Used
- **Python** 3.x
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Machine Learning**: Scikit-learn, XGBoost, Imbalanced-learn
- **Model Persistence**: Pickle

## 📋 Project Structure
```
customer_churn/
├── Custurmer_Churn.ipynb    # Main analysis notebook
├── WA_Fn-UseC_-Telco-Customer-Churn.csv  # Dataset
├── customer_churn_model.pkl  # Trained model
├── encoders.pkl             # Label encoders
└── README.md                # This file
```

## 🔍 Analysis Pipeline

### 1. Data Loading & Inspection
- Loaded 7,043 records with 21 columns
- Removed customerID (identifier column)
- Identified and handled missing values in TotalCharges
- Converted TotalCharges from string to float

### 2. Exploratory Data Analysis (EDA)
- **Numerical Features**: Analyzed tenure, MonthlyCharges, TotalCharges distributions
- **Categorical Features**: Examined distribution across 17 categorical variables
- **Correlation Analysis**: Heatmap showing relationships between numerical features
- **Target Distribution**: Identified class imbalance (73.5% No Churn, 26.5% Churn)

### 3. Data Preprocessing
- **Label Encoding**: Applied to all categorical features
- **Target Encoding**: Churn (Yes→1, No→0)
- **Train-Test Split**: 80-20 split with random_state=42
- **Class Imbalance Handling**: Applied SMOTE for oversampling minority class

### 4. Model Training
**Models Compared**:
- Decision Tree Classifier
- Random Forest Classifier
- XGBoost Classifier

**Cross-Validation**: 5-fold CV with accuracy scoring

### 5. Model Evaluation
**Best Model**: Random Forest (CV Accuracy: 0.84)
**Test Performance**:
- Accuracy: 77.86%
- Precision (Churn): 58%
- Recall (Churn): 59%
- F1-Score (Churn): 58%

## 🚀 Model Deployment
The trained model is saved as `customer_churn_model.pkl` with:
- RandomForestClassifier model
- Feature names for prediction
- Label encoders saved separately as `encoders.pkl`

### Prediction System
```python
# Load model and encoders
with open("customer_churn_model.pkl", "rb") as file:
    model_data = pickle.load(file)

with open("encoders.pkl", "rb") as file:
    encoders = pickle.load(file)

# Make predictions
prediction = loaded_model.predict(input_data)
probability = loaded_model.predict_proba(input_data)
```

## 📈 Key Findings

### Customer Churn Insights:
1. **Class Imbalance**: 26.5% of customers churn - significant business impact
2. **Tenure Impact**: Customers with shorter tenure more likely to churn
3. **Service Usage**: Customers without additional services (security, backup, etc.) show higher churn rates
4. **Contract Type**: Month-to-month contracts associated with higher churn

### Model Performance:
- Random Forest outperformed other models
- Good overall accuracy but room for improvement in churn prediction precision
- SMOTE helped address class imbalance effectively

## 🔧 Future Improvements

### Model Enhancements:
- [ ] **Hyperparameter Tuning**: GridSearchCV or RandomizedSearchCV
- [ ] **Feature Engineering**: Create new features from existing ones
- [ ] **Advanced Models**: Try LightGBM, CatBoost, or Neural Networks
- [ ] **Ensemble Methods**: Voting classifiers or stacking

### Data Improvements:
- [ ] **Feature Selection**: Remove irrelevant features
- [ ] **Advanced Sampling**: Try different oversampling/undersampling techniques
- [ ] **Cross-Validation**: Use stratified K-fold with different fold numbers

### Business Applications:
- [ ] **Customer Segmentation**: Cluster customers for targeted retention
- [ ] **Churn Risk Scoring**: Create risk tiers for different customer groups
- [ ] **A/B Testing**: Test retention strategies based on model insights

## 📊 Model Metrics Summary

| Model | CV Accuracy | Test Accuracy | Precision (Churn) | Recall (Churn) | F1-Score (Churn) |
|-------|-------------|---------------|-------------------|----------------|------------------|
| Decision Tree | 0.78 | - | - | - | - |
| Random Forest | 0.84 | 0.78 | 0.58 | 0.59 | 0.58 |
| XGBoost | 0.83 | - | - | - | - |

## 🤝 Contributing
Feel free to contribute improvements, suggest new features, or report issues. Key areas for contribution:
- Model optimization techniques
- Additional visualization methods
- Business insight generation
- Code refactoring and documentation

## 📝 Notes
- The notebook contains comprehensive EDA with visualizations
- All preprocessing steps are reproducible
- Model artifacts are saved for deployment
- Code includes error handling and best practices

## 📚 References
- [SMOTE for Imbalanced Classification](https://arxiv.org/abs/1106.1813)
- [Random Forest for Classification](https://link.springer.com/article/10.1023/A:1010933404324)
- [Customer Churn Prediction Best Practices](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
