

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

import warnings
warnings.filterwarnings('ignore')


# ============================================================================
# VISUALIZATION STYLE
# ============================================================================

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


# ============================================================================
# 1. GENERATE SYNTHETIC STUDENT DATASET
# ============================================================================

def generate_student_dataset(n_students=500, random_state=42):
    """
    Generate a comprehensive student dataset with multiple features.
    """

    np.random.seed(random_state)

    data = {
        'Student_ID': range(1, n_students + 1),

        'Study_Hours_Per_Week':
            np.random.uniform(5, 40, n_students),

        'Attendance_Percentage':
            np.random.uniform(60, 100, n_students),

        'Assignment_Completion_Rate':
            np.random.uniform(40, 100, n_students),

        'Internal_Assessment_Marks':
            np.random.uniform(20, 50, n_students),

        'Class_Participation_Score':
            np.random.uniform(0, 10, n_students),

        'Previous_Semester_GPA':
            np.random.uniform(2.0, 4.0, n_students),

        'Lab_Work_Quality':
            np.random.uniform(0, 10, n_students),

        'Engagement_Index':
            np.random.uniform(0, 100, n_students),
    }

    df = pd.DataFrame(data)

    # Create target variable: Final Academic Performance (0-100)
    df['Final_Performance'] = (
        0.25 * (df['Study_Hours_Per_Week'] / 40 * 100) +
        0.20 * df['Attendance_Percentage'] +
        0.15 * df['Assignment_Completion_Rate'] +
        0.15 * (df['Internal_Assessment_Marks'] / 50 * 100) +
        0.10 * (df['Class_Participation_Score'] / 10 * 100) +
        0.10 * (df['Previous_Semester_GPA'] / 4.0 * 100) +
        0.05 * df['Lab_Work_Quality'] * 10
    )

    # Add random noise
    df['Final_Performance'] += np.random.normal(0, 3, n_students)

    # Keep performance between 0 and 100
    df['Final_Performance'] = df['Final_Performance'].clip(0, 100)

    return df


# ============================================================================
# 2. DATA EXPLORATION AND ANALYSIS
# ============================================================================

def explore_data(df):
    """
    Perform exploratory data analysis.
    """

    print("=" * 80)
    print("DATASET OVERVIEW")
    print("=" * 80)

    print(f"\nDataset Shape: {df.shape}")
    print(f"Number of Students: {df.shape[0]}")
    print(f"Number of Features: {df.shape[1]}")

    print("\n" + "=" * 80)
    print("STATISTICAL SUMMARY")
    print("=" * 80)

    print(df.describe())

    print("\n" + "=" * 80)
    print("MISSING VALUES")
    print("=" * 80)

    print(df.isnull().sum())

    return df.describe()


# ============================================================================
# 3. VISUALIZATION FUNCTIONS
# ============================================================================

def create_correlation_heatmap(df):
    """
    Create correlation heatmap for all features.
    """

    plt.figure(figsize=(14, 10))

    numeric_df = df.select_dtypes(include=[np.number])

    correlation_matrix = numeric_df.corr()

    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8}
    )

    plt.title(
        'Correlation Matrix: Student Performance Features',
        fontsize=14,
        fontweight='bold',
        pad=20
    )

    plt.tight_layout()

    # Fixed Mac-compatible path
    plt.savefig(
        'correlation_heatmap.png',
        dpi=300,
        bbox_inches='tight'
    )

    print("✓ Correlation heatmap saved")

    plt.close()


def create_feature_importance_plot(feature_importance, feature_names):
    """
    Create feature importance visualization.
    """

    plt.figure(figsize=(12, 8))

    indices = np.argsort(feature_importance)[::-1]

    plt.bar(
        range(len(feature_importance)),
        feature_importance[indices],
        color='steelblue',
        alpha=0.8,
        edgecolor='black'
    )

    plt.xticks(
        range(len(feature_importance)),
        [feature_names[i] for i in indices],
        rotation=45,
        ha='right'
    )

    plt.title(
        'Feature Importance in Performance Prediction',
        fontsize=14,
        fontweight='bold',
        pad=20
    )

    plt.ylabel('Importance Score', fontsize=12)
    plt.xlabel('Features', fontsize=12)

    plt.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        'feature_importance.png',
        dpi=300,
        bbox_inches='tight'
    )

    print("✓ Feature importance plot saved")

    plt.close()


def create_performance_distribution(df):
    """
    Create distribution plots for key features.
    """

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    fig.suptitle(
        'Distribution of Key Student Performance Features',
        fontsize=14,
        fontweight='bold'
    )

    features = [
        'Study_Hours_Per_Week',
        'Attendance_Percentage',
        'Assignment_Completion_Rate',
        'Internal_Assessment_Marks',
        'Class_Participation_Score',
        'Final_Performance'
    ]

    for idx, feature in enumerate(features):

        ax = axes[idx // 3, idx % 3]

        ax.hist(
            df[feature],
            bins=30,
            color='steelblue',
            alpha=0.7,
            edgecolor='black'
        )

        ax.set_title(feature, fontweight='bold')
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')

        ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        'feature_distribution.png',
        dpi=300,
        bbox_inches='tight'
    )

    print("✓ Feature distribution plot saved")

    plt.close()


def create_scatter_plots(df):
    """
    Create scatter plots showing relationships with final performance.
    """

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    fig.suptitle(
        'Relationship Between Features and Final Performance',
        fontsize=14,
        fontweight='bold'
    )

    features = [
        'Study_Hours_Per_Week',
        'Attendance_Percentage',
        'Assignment_Completion_Rate',
        'Internal_Assessment_Marks',
        'Class_Participation_Score',
        'Previous_Semester_GPA'
    ]

    for idx, feature in enumerate(features):

        ax = axes[idx // 3, idx % 3]

        ax.scatter(
            df[feature],
            df['Final_Performance'],
            alpha=0.5,
            s=30,
            color='steelblue'
        )

        # Add trend line
        z = np.polyfit(
            df[feature],
            df['Final_Performance'],
            1
        )

        p = np.poly1d(z)

        sorted_values = df[feature].sort_values()

        ax.plot(
            sorted_values,
            p(sorted_values),
            "r--",
            linewidth=2,
            label='Trend'
        )

        ax.set_title(feature, fontweight='bold')
        ax.set_xlabel(feature)
        ax.set_ylabel('Final Performance')

        ax.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        'scatter_relationships.png',
        dpi=300,
        bbox_inches='tight'
    )

    print("✓ Scatter relationship plots saved")

    plt.close()


def create_model_comparison(results):
    """
    Create bar chart comparing model performance.
    """

    models = list(results.keys())

    r2_scores = [
        results[model]['R2']
        for model in models
    ]

    rmse_scores = [
        results[model]['RMSE']
        for model in models
    ]

    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(14, 6)
    )

    # R² Score comparison
    ax1.bar(
        models,
        r2_scores,
        color='steelblue',
        alpha=0.8,
        edgecolor='black'
    )

    ax1.set_title(
        'Model R² Score Comparison',
        fontweight='bold',
        fontsize=12
    )

    ax1.set_ylabel('R² Score')
    ax1.set_ylim([0, 1])

    ax1.grid(axis='y', alpha=0.3)

    for i, v in enumerate(r2_scores):
        ax1.text(
            i,
            v + 0.02,
            f'{v:.3f}',
            ha='center',
            fontweight='bold'
        )

    # RMSE comparison
    ax2.bar(
        models,
        rmse_scores,
        color='coral',
        alpha=0.8,
        edgecolor='black'
    )

    ax2.set_title(
        'Model RMSE Comparison',
        fontweight='bold',
        fontsize=12
    )

    ax2.set_ylabel('RMSE')

    ax2.grid(axis='y', alpha=0.3)

    for i, v in enumerate(rmse_scores):
        ax2.text(
            i,
            v + 0.1,
            f'{v:.2f}',
            ha='center',
            fontweight='bold'
        )

    plt.tight_layout()

    plt.savefig(
        'model_comparison.png',
        dpi=300,
        bbox_inches='tight'
    )

    print("✓ Model comparison plot saved")

    plt.close()


def create_prediction_accuracy_plot(y_test, y_pred, model_name):
    """
    Create actual vs predicted plot.
    """

    plt.figure(figsize=(10, 8))

    plt.scatter(
        y_test,
        y_pred,
        alpha=0.5,
        s=30,
        color='steelblue'
    )

    min_val = min(
        y_test.min(),
        y_pred.min()
    )

    max_val = max(
        y_test.max(),
        y_pred.max()
    )

    plt.plot(
        [min_val, max_val],
        [min_val, max_val],
        'r--',
        linewidth=2,
        label='Perfect Prediction'
    )

    plt.xlabel(
        'Actual Performance',
        fontsize=12
    )

    plt.ylabel(
        'Predicted Performance',
        fontsize=12
    )

    plt.title(
        f'Actual vs Predicted Performance - {model_name}',
        fontsize=14,
        fontweight='bold'
    )

    plt.legend()

    plt.grid(alpha=0.3)

    plt.tight_layout()

    filename = (
        f'prediction_accuracy_'
        f'{model_name.lower().replace(" ", "_")}.png'
    )

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches='tight'
    )

    print(
        f"✓ Prediction accuracy plot for "
        f"{model_name} saved"
    )

    plt.close()


def create_residual_plot(y_test, y_pred, model_name):
    """
    Create residual plot for model analysis.
    """

    residuals = y_test - y_pred

    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(14, 6)
    )

    # Residuals vs Predicted
    ax1.scatter(
        y_pred,
        residuals,
        alpha=0.5,
        s=30,
        color='steelblue'
    )

    ax1.axhline(
        y=0,
        color='r',
        linestyle='--',
        linewidth=2
    )

    ax1.set_xlabel('Predicted Performance')
    ax1.set_ylabel('Residuals')

    ax1.set_title(
        'Residuals vs Predicted Values',
        fontweight='bold'
    )

    ax1.grid(alpha=0.3)

    # Residual distribution
    ax2.hist(
        residuals,
        bins=30,
        color='steelblue',
        alpha=0.7,
        edgecolor='black'
    )

    ax2.set_xlabel('Residuals')
    ax2.set_ylabel('Frequency')

    ax2.set_title(
        'Distribution of Residuals',
        fontweight='bold'
    )

    ax2.grid(axis='y', alpha=0.3)

    plt.suptitle(
        f'Residual Analysis - {model_name}',
        fontsize=14,
        fontweight='bold'
    )

    plt.tight_layout()

    filename = (
        f'residual_analysis_'
        f'{model_name.lower().replace(" ", "_")}.png'
    )

    plt.savefig(
        filename,
        dpi=300,
        bbox_inches='tight'
    )

    print(
        f"✓ Residual analysis plot for "
        f"{model_name} saved"
    )

    plt.close()


def create_risk_classification_plot(df, predictions):
    """
    Create visualization of student risk classification.
    """

    risk_categories = []

    for pred in predictions:

        if pred >= 80:
            risk_categories.append('Excellent')

        elif pred >= 70:
            risk_categories.append('Good')

        elif pred >= 60:
            risk_categories.append('Average')

        elif pred >= 50:
            risk_categories.append('At Risk')

        else:
            risk_categories.append('Critical Risk')

    risk_df = pd.DataFrame({
        'Risk_Category': risk_categories
    })

    risk_counts = (
        risk_df['Risk_Category']
        .value_counts()
    )

    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(14, 6)
    )

    # Bar chart
    colors = [
        'green',
        'lightgreen',
        'yellow',
        'orange',
        'red'
    ]

    ax1.bar(
        risk_counts.index,
        risk_counts.values,
        color=colors,
        alpha=0.8,
        edgecolor='black'
    )

    ax1.set_title(
        'Student Distribution by Risk Category',
        fontweight='bold',
        fontsize=12
    )

    ax1.set_ylabel('Number of Students')

    ax1.grid(axis='y', alpha=0.3)

    for i, v in enumerate(risk_counts.values):

        ax1.text(
            i,
            v + 5,
            str(v),
            ha='center',
            fontweight='bold'
        )

    # Pie chart
    ax2.pie(
        risk_counts.values,
        labels=risk_counts.index,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )

    ax2.set_title(
        'Percentage Distribution of Risk Categories',
        fontweight='bold',
        fontsize=12
    )

    plt.suptitle(
        'Student Academic Risk Classification',
        fontsize=14,
        fontweight='bold'
    )

    plt.tight_layout()

    plt.savefig(
        'risk_classification.png',
        dpi=300,
        bbox_inches='tight'
    )

    print("✓ Risk classification plot saved")

    plt.close()


# ============================================================================
# 4. MACHINE LEARNING MODEL TRAINING AND EVALUATION
# ============================================================================

def train_and_evaluate_models(
    X_train,
    X_test,
    y_train,
    y_test
):
    """
    Train multiple machine learning models
    and evaluate their performance.
    """

    results = {}

    print("\n" + "=" * 80)
    print("MACHINE LEARNING MODEL TRAINING AND EVALUATION")
    print("=" * 80)

    # ------------------------------------------------------------------------
    # 1. LINEAR REGRESSION
    # ------------------------------------------------------------------------

    print("\n[1/3] Training Linear Regression Model...")

    lr_model = LinearRegression()

    lr_model.fit(
        X_train,
        y_train
    )

    y_pred_lr = lr_model.predict(X_test)

    r2_lr = r2_score(
        y_test,
        y_pred_lr
    )

    rmse_lr = np.sqrt(
        mean_squared_error(
            y_test,
            y_pred_lr
        )
    )

    mae_lr = mean_absolute_error(
        y_test,
        y_pred_lr
    )

    results['Linear Regression'] = {
        'Model': lr_model,
        'R2': r2_lr,
        'RMSE': rmse_lr,
        'MAE': mae_lr,
        'Predictions': y_pred_lr
    }

    print(f"   R² Score: {r2_lr:.4f}")
    print(f"   RMSE: {rmse_lr:.4f}")
    print(f"   MAE: {mae_lr:.4f}")

    # ------------------------------------------------------------------------
    # 2. RANDOM FOREST
    # ------------------------------------------------------------------------

    print("\n[2/3] Training Random Forest Regressor...")

    rf_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    rf_model.fit(
        X_train,
        y_train
    )

    y_pred_rf = rf_model.predict(X_test)

    r2_rf = r2_score(
        y_test,
        y_pred_rf
    )

    rmse_rf = np.sqrt(
        mean_squared_error(
            y_test,
            y_pred_rf
        )
    )

    mae_rf = mean_absolute_error(
        y_test,
        y_pred_rf
    )

    results['Random Forest'] = {
        'Model': rf_model,
        'R2': r2_rf,
        'RMSE': rmse_rf,
        'MAE': mae_rf,
        'Predictions': y_pred_rf,
        'Feature_Importance':
            rf_model.feature_importances_
    }

    print(f"   R² Score: {r2_rf:.4f}")
    print(f"   RMSE: {rmse_rf:.4f}")
    print(f"   MAE: {mae_rf:.4f}")

    # ------------------------------------------------------------------------
    # 3. GRADIENT BOOSTING
    # ------------------------------------------------------------------------

    print("\n[3/3] Training Gradient Boosting Regressor...")

    gb_model = GradientBoostingRegressor(
        n_estimators=100,
        random_state=42
    )

    gb_model.fit(
        X_train,
        y_train
    )

    y_pred_gb = gb_model.predict(X_test)

    r2_gb = r2_score(
        y_test,
        y_pred_gb
    )

    rmse_gb = np.sqrt(
        mean_squared_error(
            y_test,
            y_pred_gb
        )
    )

    mae_gb = mean_absolute_error(
        y_test,
        y_pred_gb
    )

    results['Gradient Boosting'] = {
        'Model': gb_model,
        'R2': r2_gb,
        'RMSE': rmse_gb,
        'MAE': mae_gb,
        'Predictions': y_pred_gb,
        'Feature_Importance':
            gb_model.feature_importances_
    }

    print(f"   R² Score: {r2_gb:.4f}")
    print(f"   RMSE: {rmse_gb:.4f}")
    print(f"   MAE: {mae_gb:.4f}")

    # ------------------------------------------------------------------------
    # MODEL SUMMARY
    # ------------------------------------------------------------------------

    print("\n" + "=" * 80)
    print("MODEL PERFORMANCE SUMMARY")
    print("=" * 80)

    summary_df = pd.DataFrame({
        'Model': list(results.keys()),

        'R² Score': [
            results[m]['R2']
            for m in results.keys()
        ],

        'RMSE': [
            results[m]['RMSE']
            for m in results.keys()
        ],

        'MAE': [
            results[m]['MAE']
            for m in results.keys()
        ]
    })

    print(
        summary_df.to_string(index=False)
    )

    # Identify model with highest R²
    best_model_name = max(
        results.keys(),
        key=lambda x: results[x]['R2']
    )

    print(
        f"\n✓ Best Performing Model: "
        f"{best_model_name}"
    )

    print(
        f"  R² Score: "
        f"{results[best_model_name]['R2']:.4f}"
    )

    return results, best_model_name


# ============================================================================
# 5. MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function.
    """

    print("\n" + "=" * 80)
    print("STUDENT ACADEMIC PERFORMANCE PREDICTION SYSTEM")
    print("=" * 80)

    # ------------------------------------------------------------------------
    # STEP 1: GENERATE DATASET
    # ------------------------------------------------------------------------

    print("\n[Step 1] Generating Student Dataset...")

    df = generate_student_dataset(
        n_students=500
    )

    print(
        f"✓ Dataset generated with "
        f"{len(df)} students and "
        f"{len(df.columns)} columns"
    )

    # ------------------------------------------------------------------------
    # STEP 2: EXPLORE DATA
    # ------------------------------------------------------------------------

    print("\n[Step 2] Exploring Dataset...")

    explore_data(df)

    # ------------------------------------------------------------------------
    # STEP 3: PREPARE DATA
    # ------------------------------------------------------------------------

    print(
        "\n[Step 3] Preparing Data "
        "for Model Training..."
    )

    feature_columns = [
        'Study_Hours_Per_Week',
        'Attendance_Percentage',
        'Assignment_Completion_Rate',
        'Internal_Assessment_Marks',
        'Class_Participation_Score',
        'Previous_Semester_GPA',
        'Lab_Work_Quality',
        'Engagement_Index'
    ]

    X = df[feature_columns]

    y = df['Final_Performance']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Scale features
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(
        X_train
    )

    X_test_scaled = scaler.transform(
        X_test
    )

    print(
        f"✓ Training set size: "
        f"{len(X_train)}"
    )

    print(
        f"✓ Test set size: "
        f"{len(X_test)}"
    )

    # ------------------------------------------------------------------------
    # STEP 4: TRAIN MODELS
    # ------------------------------------------------------------------------

    print(
        "\n[Step 4] Training "
        "Machine Learning Models..."
    )

    results, best_model_name = train_and_evaluate_models(
        X_train_scaled,
        X_test_scaled,
        y_train,
        y_test
    )

    # ------------------------------------------------------------------------
    # STEP 5: GENERATE VISUALIZATIONS
    # ------------------------------------------------------------------------

    print(
        "\n[Step 5] Generating Visualizations..."
    )

    print(
        "Creating correlation heatmap..."
    )

    create_correlation_heatmap(df)

    print(
        "Creating feature distribution plots..."
    )

    create_performance_distribution(df)

    print(
        "Creating scatter relationship plots..."
    )

    create_scatter_plots(df)

    print(
        "Creating model comparison plot..."
    )

    create_model_comparison(results)

    # Best model plots
    best_model_results = results[
        best_model_name
    ]

    print(
        f"Creating prediction accuracy plot "
        f"for {best_model_name}..."
    )

    create_prediction_accuracy_plot(
        y_test,
        best_model_results['Predictions'],
        best_model_name
    )

    print(
        f"Creating residual analysis plot "
        f"for {best_model_name}..."
    )

    create_residual_plot(
        y_test,
        best_model_results['Predictions'],
        best_model_name
    )

    # Feature importance only for models that support it
    if 'Feature_Importance' in best_model_results:

        print(
            f"Creating feature importance plot "
            f"for {best_model_name}..."
        )

        create_feature_importance_plot(
            best_model_results['Feature_Importance'],
            feature_columns
        )

    print(
        "Creating risk classification plot..."
    )

    create_risk_classification_plot(
        df,
        best_model_results['Predictions']
    )

    # ------------------------------------------------------------------------
    # COMPLETION MESSAGE
    # ------------------------------------------------------------------------

    print("\n" + "=" * 80)
    print("EXECUTION COMPLETED SUCCESSFULLY")
    print("=" * 80)

    print("\nGenerated Visualizations:")

    print("  1. correlation_heatmap.png")
    print("  2. feature_distribution.png")
    print("  3. scatter_relationships.png")
    print("  4. model_comparison.png")
    print(
        f"  5. prediction_accuracy_"
        f"{best_model_name.lower().replace(' ', '_')}.png"
    )
    print(
        f"  6. residual_analysis_"
        f"{best_model_name.lower().replace(' ', '_')}.png"
    )

    if 'Feature_Importance' in best_model_results:
        print("  7. feature_importance.png")
        print("  8. risk_classification.png")
    else:
        print("  7. risk_classification.png")

    return df, results, best_model_name


# ============================================================================
# PROGRAM START
# ============================================================================

if __name__ == "__main__":
    df, results, best_model_name = main()
