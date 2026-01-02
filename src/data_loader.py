"""Data Loader Module - Load and read sales data from CSV files"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional


class DataLoader:
    """
    Load sales data from CSV files and return pandas DataFrames.
    """
    
    @staticmethod
    def load_csv(filepath: str) -> pd.DataFrame:
        """
        Load CSV file into a DataFrame.
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            pd.DataFrame: Loaded data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a valid CSV
        """
        try:
            if not Path(filepath).exists():
                raise FileNotFoundError(f"File not found: {filepath}")
            
            df = pd.read_csv(filepath)
            return df
        except pd.errors.ParserError as e:
            raise ValueError(f"Invalid CSV file: {str(e)}")
    
    @staticmethod
    def validate_data(df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate if DataFrame has required columns.
        
        Required columns: Date, Sales, Quantity
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, message)
        """
        required_cols = ['Date', 'Sales', 'Quantity']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            return False, f"Missing required columns: {', '.join(missing_cols)}"
        
        if len(df) == 0:
            return False, "DataFrame is empty"
        
        return True, "Data validation passed"
    
    @staticmethod
    def convert_date(df: pd.DataFrame, date_col: str = 'Date') -> pd.DataFrame:
        """
        Convert Date column to datetime format.
        
        Args:
            df: Input DataFrame
            date_col: Name of date column
            
        Returns:
            pd.DataFrame: DataFrame with converted date column
        """
        df_copy = df.copy()
        try:
            df_copy[date_col] = pd.to_datetime(df_copy[date_col])
            df_copy = df_copy.sort_values(by=date_col)
        except Exception as e:
            raise ValueError(f"Error converting date: {str(e)}")
        
        return df_copy
    
    @staticmethod
    def get_basic_info(df: pd.DataFrame) -> dict:
        """
        Get basic information about the dataset.
        
        Args:
            df: Input DataFrame
            
        Returns:
            dict: Dictionary with shape, dtypes, and missing values
        """
        return {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'basic_stats': df.describe().to_dict()
        }
