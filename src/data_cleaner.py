"""Data Cleaner Module - Clean and preprocess sales data"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class DataCleaner:
    """
    Clean and preprocess sales data for analysis.
    """
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
        """
        Handle missing values in the DataFrame.
        
        Args:
            df: Input DataFrame
            strategy: 'mean', 'median', 'forward_fill', or 'drop'
            
        Returns:
            pd.DataFrame: DataFrame with handled missing values
        """
        df_copy = df.copy()
        
        numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
        
        if strategy == 'mean':
            df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].mean())
        elif strategy == 'median':
            df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].median())
        elif strategy == 'forward_fill':
            df_copy = df_copy.fillna(method='ffill')
        elif strategy == 'drop':
            df_copy = df_copy.dropna()
        
        return df_copy
    
    @staticmethod
    def remove_outliers(df: pd.DataFrame, column: str, threshold: float = 3) -> pd.DataFrame:
        """
        Remove outliers using Z-score method.
        
        Args:
            df: Input DataFrame
            column: Column to check for outliers
            threshold: Z-score threshold (default 3)
            
        Returns:
            pd.DataFrame: DataFrame without outliers
        """
        df_copy = df.copy()
        mean = df_copy[column].mean()
        std = df_copy[column].std()
        z_scores = np.abs((df_copy[column] - mean) / std)
        df_copy = df_copy[z_scores < threshold]
        return df_copy
    
    @staticmethod
    def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names (lowercase, remove spaces).
        
        Args:
            df: Input DataFrame
            
        Returns:
            pd.DataFrame: DataFrame with standardized column names
        """
        df_copy = df.copy()
        df_copy.columns = df_copy.columns.str.lower().str.strip().str.replace(' ', '_')
        return df_copy
    
    @staticmethod
    def get_cleaning_report(df: pd.DataFrame, original_shape: tuple) -> Dict:
        """
        Generate a report of cleaning operations.
        
        Args:
            df: Cleaned DataFrame
            original_shape: Original DataFrame shape
            
        Returns:
            dict: Cleaning report
        """
        return {
            'original_rows': original_shape[0],
            'cleaned_rows': df.shape[0],
            'rows_removed': original_shape[0] - df.shape[0],
            'removal_percentage': ((original_shape[0] - df.shape[0]) / original_shape[0] * 100),
            'missing_values': df.isnull().sum().to_dict()
        }
