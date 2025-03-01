import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from typing import List, Dict, Any


class IrrigationModel:
    """
    Modelo de machine learning para predicción de necesidades de riego.
    """

    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        """
        Inicializa el modelo de predicción de riego.

        :param n_estimators: Número de árboles en el bosque aleatorio
        :param random_state: Semilla para reproducibilidad
        """
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        self.scaler = StandardScaler()
        self.feedback_history: List[Dict[str, Any]] = []

    def prepare_features(self, recommendation: Dict[str, Any]) -> List[float]:
        """
        Prepara características para entrenamiento del modelo.

        :param recommendation: Recomendación de riego
        :return: Vector de características
        """
        return [
            recommendation["current_conditions"].get("temperature", 0),
            recommendation["current_conditions"].get("humidity", 0),
            # Mapear etapa del cultivo a valor numérico
            {
                "dormancia": 0,
                "floracion": 1,
                "cuaja": 2,
                "desarrollo_fruto": 3,
                "cosecha": 4,
            }.get(recommendation["crop_stage"], 2),
            # Mapear tipo de suelo a valor numérico
            {"sandy": 0, "loam": 1, "clay": 2}.get(recommendation["soil_type"], 1),
            # Mapear recomendación a valor numérico
            {"Riego Mínimo": 0, "Riego Moderado": 1, "Riego Intensivo": 2}.get(
                recommendation["recommendation"], 1
            ),
        ]

    def train(self, recommendations: List[Dict[str, Any]], outcomes: List[bool]) -> None:
        """
        Entrena el modelo con recomendaciones y resultados.

        :param recommendations: Lista de recomendaciones de riego
        :param outcomes: Lista de resultados booleanos correspondientes
        """
        # Preparar características
        X = [self.prepare_features(rec) for rec in recommendations]
        y = [1 if outcome else 0 for outcome in outcomes]

        # Escalar características
        X_scaled = self.scaler.fit_transform(X)

        # Entrenar modelo
        self.model.fit(X_scaled, y)

    def predict_success_probability(self, recommendation: Dict[str, Any]) -> float:
        """
        Predice la probabilidad de éxito de una recomendación.

        :param recommendation: Recomendación de riego
        :return: Probabilidad de éxito
        """
        # Preparar características
        features = self.prepare_features(recommendation)
        features_scaled = self.scaler.transform([features])

        # Predecir probabilidad de éxito
        return self.model.predict_proba(features_scaled)[0][1]

    def log_feedback(self, recommendation: Dict[str, Any], success: bool) -> None:
        """
        Registra retroalimentación sobre una recomendación.

        :param recommendation: Recomendación de riego
        :param success: Resultado de la recomendación
        """
        feedback_entry = {
            "recommendation": recommendation,
            "success": success,
            "features": self.prepare_features(recommendation),
        }
        self.feedback_history.append(feedback_entry)

        # Si hay suficientes datos, entrenar modelo
        if len(self.feedback_history) > 10:
            recommendations = [entry["recommendation"] for entry in self.feedback_history]
            outcomes = [entry["success"] for entry in self.feedback_history]
            self.train(recommendations, outcomes)
