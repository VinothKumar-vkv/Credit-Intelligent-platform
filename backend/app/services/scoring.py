from __future__ import annotations
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from dataclasses import dataclass
import numpy as np
from typing import Dict, List, Tuple

@dataclass
class OnlineModel:
    scaler: StandardScaler
    reg: SGDRegressor
    feature_order: List[str]

    @staticmethod
    def create(feature_order: List[str]) -> "OnlineModel":
        return OnlineModel(
            scaler=StandardScaler(with_mean=True, with_std=True),
            reg=SGDRegressor(loss="huber", penalty="elasticnet", alpha=1e-4, l1_ratio=0.15, max_iter=1, learning_rate="invscaling", eta0=0.01, random_state=42),
            feature_order=feature_order,
        )

    def partial_fit(self, X: np.ndarray, y: np.ndarray) -> None:
        if not hasattr(self.reg, "t_"):
            Xs = self.scaler.fit_transform(X)
            self.reg.partial_fit(Xs, y)
        else:
            Xs = self.scaler.transform(X)
            self.reg.partial_fit(Xs, y)

    def predict(self, features: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        x = np.array([[features.get(f, 0.0) for f in self.feature_order]])
        xs = self.scaler.transform(x)
        score = float(self.reg.predict(xs)[0])
        # Explainability: coefficient * standardized value mapped back to raw feature names
        contribs: Dict[str, float] = {}
        if hasattr(self.reg, "coef_"):
            for i, f in enumerate(self.feature_order):
                contribs[f] = float(self.reg.coef_[i] * xs[0, i])
        return score, contribs

