import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LassoCV, RidgeCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error

# 1. Preprocessing
def get_preprocessor(cat_features, num_features):
    """Hilfsfunktion für den Preprocessor mit Skalierung."""
    return ColumnTransformer([
        ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), cat_features),
        ('num', StandardScaler(), num_features) 
    ], remainder='passthrough')

# 2. ANPASSUNG: num_features muss auch hier als Argument rein
def run_ols(X_train, X_val, y_train, y_val, cat_features, num_features):
    pipeline = Pipeline([
        ('preprocessor', get_preprocessor(cat_features, num_features)),
        ('regressor', LinearRegression())
    ])
    pipeline.fit(X_train, y_train)
    
    metrics = {
        'R2_Train': r2_score(y_train, pipeline.predict(X_train)),
        'R2_Val': r2_score(y_val, pipeline.predict(X_val))
    }
    return pipeline, metrics

def run_lasso_cv(X_train, X_val, y_train, y_val, cat_features, num_features):
    pipeline = Pipeline([
        ('preprocessor', get_preprocessor(cat_features, num_features)),
        ('regressor', LassoCV(cv=5, random_state=42))
    ])
    pipeline.fit(X_train, y_train)
    
    metrics = {
        'R2_Train': r2_score(y_train, pipeline.predict(X_train)),
        'R2_Val': r2_score(y_val, pipeline.predict(X_val)),
        'Best_Alpha': pipeline.named_steps['regressor'].alpha_
    }
    return pipeline, metrics

def run_ridge_cv(X_train, X_val, y_train, y_val, cat_features, num_features):
    pipeline = Pipeline([
        ('preprocessor', get_preprocessor(cat_features, num_features)),
        ('regressor', RidgeCV(cv=5))
    ])
    pipeline.fit(X_train, y_train)
    
    metrics = {
        'R2_Train': r2_score(y_train, pipeline.predict(X_train)),
        'R2_Val': r2_score(y_val, pipeline.predict(X_val)),
        'Best_Alpha': pipeline.named_steps['regressor'].alpha_
    }
    return pipeline, metrics