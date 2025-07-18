"""
Módulo de ingeniería de características para el modelo de retención estudiantil.

Este módulo contiene funciones para crear características relevantes
para predecir el abandono estudiantil basado en datos demográficos,
académicos y comportamentales.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeatureEngineer:
    """
    Clase para la ingeniería de características del modelo de retención estudiantil.
    """
    
    def __init__(self):
        """Inicializa el ingeniero de características."""
        self.feature_columns = []
        self.categorical_columns = []
        self.numerical_columns = []
        
    def create_demographic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Crea características demográficas.
        
        Args:
            df: DataFrame con información de estudiantes
            
        Returns:
            DataFrame con características demográficas
        """
        logger.info("🔧 Creando características demográficas...")
        
        # Copiar el DataFrame original
        features_df = df.copy()
        
        # Codificar variables categóricas
        categorical_cols = ['gender', 'age_band', 'highest_education', 'region', 'disability']
        
        for col in categorical_cols:
            if col in features_df.columns:
                # One-hot encoding para variables categóricas
                dummies = pd.get_dummies(features_df[col], prefix=col, dummy_na=True)
                features_df = pd.concat([features_df, dummies], axis=1)
                features_df.drop(columns=[col], inplace=True)
        
        # Crear características derivadas
        if 'imd_band' in features_df.columns:
            # Convertir IMD band a numérico (asumiendo que es ordinal)
            imd_mapping = {
                '0-10%': 1, '10-20%': 2, '20-30%': 3, '30-40%': 4, '40-50%': 5,
                '50-60%': 6, '60-70%': 7, '70-80%': 8, '80-90%': 9, '90-100%': 10
            }
            features_df['imd_band_numeric'] = features_df['imd_band'].map(imd_mapping)
            features_df.drop(columns=['imd_band'], inplace=True)
        
        logger.info(f"✅ Características demográficas creadas: {features_df.shape[1]} columnas")
        return features_df
    
    def create_academic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Crea características académicas.
        
        Args:
            df: DataFrame con información de estudiantes
            
        Returns:
            DataFrame con características académicas
        """
        logger.info("🔧 Creando características académicas...")
        
        features_df = df.copy()
        
        # Características de intentos previos
        if 'num_of_prev_attempts' in features_df.columns:
            features_df['has_prev_attempts'] = (features_df['num_of_prev_attempts'] > 0).astype(int)
            features_df['multiple_prev_attempts'] = (features_df['num_of_prev_attempts'] > 1).astype(int)
        
        # Características de créditos estudiados
        if 'studied_credits' in features_df.columns:
            features_df['is_full_time'] = (features_df['studied_credits'] >= 120).astype(int)
            features_df['is_part_time'] = (features_df['studied_credits'] < 120).astype(int)
        
        # Características de fechas
        if 'date_registration' in features_df.columns:
            features_df['registration_week'] = features_df['date_registration'] // 7
            features_df['early_registration'] = (features_df['date_registration'] <= 0).astype(int)
            features_df['late_registration'] = (features_df['date_registration'] > 0).astype(int)
        
        if 'date_unregistration' in features_df.columns:
            features_df['has_unregistration'] = features_df['date_unregistration'].notna().astype(int)
            features_df['unregistration_week'] = features_df['date_unregistration'].fillna(-1)
        
        # Características del módulo
        if 'module_presentation_length' in features_df.columns:
            features_df['module_length_weeks'] = features_df['module_presentation_length'] // 7
        
        logger.info(f"✅ Características académicas creadas: {features_df.shape[1]} columnas")
        return features_df
    
    def create_behavioral_features(self, df: pd.DataFrame, interaction_features: pd.DataFrame) -> pd.DataFrame:
        """
        Crea características comportamentales basadas en interacciones VLE.
        
        Args:
            df: DataFrame con información de estudiantes
            interaction_features: DataFrame con características de interacciones
            
        Returns:
            DataFrame con características comportamentales
        """
        logger.info("🔧 Creando características comportamentales...")
        
        features_df = df.copy()
        
        # Unir con características de interacciones
        if not interaction_features.empty:
            features_df = features_df.merge(
                interaction_features, 
                on='id_student', 
                how='left'
            )
            
            # Rellenar valores faltantes con 0
            interaction_cols = [col for col in interaction_features.columns if col != 'id_student']
            features_df[interaction_cols] = features_df[interaction_cols].fillna(0)
        
        # Crear características derivadas de interacciones
        if 'total_clicks' in features_df.columns:
            features_df['high_activity'] = (features_df['total_clicks'] > features_df['total_clicks'].median()).astype(int)
            features_df['low_activity'] = (features_df['total_clicks'] <= features_df['total_clicks'].median()).astype(int)
        
        if 'avg_clicks_per_week' in features_df.columns:
            features_df['consistent_activity'] = (features_df['avg_clicks_per_week'] > 0).astype(int)
        
        if 'weeks_active' in features_df.columns:
            features_df['long_term_engagement'] = (features_df['weeks_active'] > features_df['weeks_active'].median()).astype(int)
        
        logger.info(f"✅ Características comportamentales creadas: {features_df.shape[1]} columnas")
        return features_df
    
    def create_target_variable(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Crea la variable objetivo para el modelo.
        
        Args:
            df: DataFrame con información de estudiantes
            
        Returns:
            Tuple con DataFrame de características y Series de variable objetivo
        """
        logger.info("🎯 Creando variable objetivo...")
        
        features_df = df.copy()
        
        # Crear variable objetivo binaria (Withdrawn = 1, otros = 0)
        if 'final_result' in features_df.columns:
            target = (features_df['final_result'] == 'Withdrawn').astype(int)
            features_df.drop(columns=['final_result'], inplace=True)
        else:
            raise ValueError("No se encontró la columna 'final_result'")
        
        logger.info(f"✅ Variable objetivo creada. Distribución: {target.value_counts().to_dict()}")
        return features_df, target
    
    def prepare_features(self, 
                        student_df: pd.DataFrame, 
                        interaction_features: Optional[pd.DataFrame] = None) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepara todas las características para el modelo.
        
        Args:
            student_df: DataFrame con información de estudiantes
            interaction_features: DataFrame opcional con características de interacciones
            
        Returns:
            Tuple con DataFrame de características y Series de variable objetivo
        """
        logger.info("🚀 Iniciando preparación de características...")
        
        # Crear características demográficas
        features_df = self.create_demographic_features(student_df)
        
        # Crear características académicas
        features_df = self.create_academic_features(features_df)
        
        # Crear características comportamentales
        if interaction_features is not None:
            features_df = self.create_behavioral_features(features_df, interaction_features)
        
        # Crear variable objetivo
        features_df, target = self.create_target_variable(features_df)
        
        # Identificar tipos de columnas
        self.categorical_columns = features_df.select_dtypes(include=['object']).columns.tolist()
        self.numerical_columns = features_df.select_dtypes(include=['number']).columns.tolist()
        self.feature_columns = features_df.columns.tolist()
        
        logger.info(f"✅ Preparación completada. Características: {len(self.feature_columns)}")
        logger.info(f"   - Numéricas: {len(self.numerical_columns)}")
        logger.info(f"   - Categóricas: {len(self.categorical_columns)}")
        
        return features_df, target
    
    def get_feature_importance_ranking(self, features_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula un ranking de importancia de características basado en correlación con la variable objetivo.
        
        Args:
            features_df: DataFrame con características
            
        Returns:
            DataFrame con ranking de importancia
        """
        logger.info("📊 Calculando ranking de importancia de características...")
        
        # Calcular correlaciones con la variable objetivo (asumiendo que está en el DataFrame)
        if 'target' in features_df.columns:
            correlations = features_df.corr()['target'].abs().sort_values(ascending=False)
            
            # Crear DataFrame con ranking
            ranking_df = pd.DataFrame({
                'feature': correlations.index,
                'correlation': correlations.values
            })
            
            # Filtrar solo características (excluir target)
            ranking_df = ranking_df[ranking_df['feature'] != 'target']
            
            logger.info(f"✅ Ranking calculado para {len(ranking_df)} características")
            return ranking_df
        
        return pd.DataFrame() 