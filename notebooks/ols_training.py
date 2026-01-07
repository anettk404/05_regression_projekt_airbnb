import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, LassoCV, RidgeCV
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error

def get_preprocessor(cat_features):
    """Hilfsfunktion für den einheitlichen Preprocessor."""
    return ColumnTransformer([
        ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), cat_features)
    ], remainder='passthrough')

def run_ols(X_train, X_val, y_train, y_val, cat_features):
    pipeline = Pipeline([
        ('preprocessor', get_preprocessor(cat_features)),
        ('regressor', LinearRegression())
    ])
    pipeline.fit(X_train, y_train)
    
    metrics = {
        'R2_Train': r2_score(y_train, pipeline.predict(X_train)),
        'R2_Val': r2_score(y_val, pipeline.predict(X_val))
    }
    return pipeline, metrics

def run_lasso_cv(X_train, X_val, y_train, y_val, cat_features):
    # LassoCV wählt das beste Alpha automatisch per Cross-Validation
    pipeline = Pipeline([
        ('preprocessor', get_preprocessor(cat_features)),
        ('regressor', LassoCV(cv=5, random_state=42))
    ])
    pipeline.fit(X_train, y_train)
    
    metrics = {
        'R2_Train': r2_score(y_train, pipeline.predict(X_train)),
        'R2_Val': r2_score(y_val, pipeline.predict(X_val)),
        'Best_Alpha': pipeline.named_steps['regressor'].alpha_
    }
    return pipeline, metrics

def run_ridge_cv(X_train, X_val, y_train, y_val, cat_features):
    # RidgeCV nutzt effiziente Leave-One-Out Cross-Validation (standardmäßig)
    pipeline = Pipeline([
        ('preprocessor', get_preprocessor(cat_features)),
        ('regressor', RidgeCV(cv=5))
    ])
    pipeline.fit(X_train, y_train)
    
    metrics = {
        'R2_Train': r2_score(y_train, pipeline.predict(X_train)),
        'R2_Val': r2_score(y_val, pipeline.predict(X_val)),
        'Best_Alpha': pipeline.named_steps['regressor'].alpha_
    }
    return pipeline, metrics