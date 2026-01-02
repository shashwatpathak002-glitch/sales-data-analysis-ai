"""Sales Forecasting Model - Linear Regression based forecasting"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from datetime import datetime, timedelta
from typing import Tuple, Dict


class ForecastingModel:
    """
    Linear Regression-based forecasting model for sales prediction.
    """
    
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False
        self.metrics = {}
    
    def prepare_features(self, df: pd.DataFrame, date_col: str = 'date', 
                        sales_col: str = 'sales') -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare X and y for model training.
        
        Args:
            df: Input DataFrame
            date_col: Date column name
            sales_col: Sales column name
            
        Returns:
            Tuple[X, y]: Features and target arrays
        """
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(by=date_col)
        
        # Create time-based features
        df['days'] = (df[date_col] - df[date_col].min()).dt.days
        df['month'] = df[date_col].dt.month
        df['quarter'] = df[date_col].dt.quarter
        
        X = df[['days', 'month', 'quarter']].values
        y = df[sales_col].values
        
        return X, y
    
    def train(self, df: pd.DataFrame, date_col: str = 'date', 
             sales_col: str = 'sales') -> Dict:
        """
        Train the forecasting model.
        
        Args:
            df: Input DataFrame with training data
            date_col: Date column name
            sales_col: Sales column name
            
        Returns:
            dict: Training metrics
        """
        X, y = self.prepare_features(df, date_col, sales_col)
        self.model.fit(X, y)
        self.is_trained = True
        
        # Calculate metrics
        y_pred = self.model.predict(X)
        self.metrics = {
            'mae': mean_absolute_error(y, y_pred),
            'rmse': np.sqrt(mean_squared_error(y, y_pred)),
            'r2_score': r2_score(y, y_pred)
        }
        
        return self.metrics
    
    def forecast(self, periods: int = 30, last_date: datetime = None) -> pd.DataFrame:
        """
        Forecast sales for future periods.
        
        Args:
            periods: Number of days to forecast
            last_date: Last date from training data
            
        Returns:
            pd.DataFrame: Forecast dataframe with dates and predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making forecasts")
        
        if last_date is None:
            last_date = datetime.now()
        
        future_dates = [last_date + timedelta(days=i) for i in range(1, periods + 1)]
        future_df = pd.DataFrame({'date': future_dates})
        
        # Create features for future dates
        min_date = last_date - timedelta(days=365)
        future_df['days'] = (future_df['date'] - min_date).dt.days
        future_df['month'] = future_df['date'].dt.month
        future_df['quarter'] = future_df['date'].dt.quarter
        
        X_future = future_df[['days', 'month', 'quarter']].values
        future_df['forecast'] = self.model.predict(X_future)
        
        return future_df[['date', 'forecast']]
