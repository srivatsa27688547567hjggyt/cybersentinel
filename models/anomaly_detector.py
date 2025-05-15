import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(log_data):
    """
    Detect anomalies in log data using IsolationForest.
    Returns:
        - anomalies: 1 if anomaly, 0 otherwise
        - threat_levels: Low/Medium/High based on anomaly score
    """
    # Feature engineering: simple length and digit count as features
    features = pd.DataFrame()
    features['length'] = log_data['log'].astype(str).apply(len)
    features['digit_count'] = log_data['log'].astype(str).apply(lambda x: sum(c.isdigit() for c in x))

    # Fit IsolationForest
    clf = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    preds = clf.fit_predict(features)
    anomaly_scores = clf.decision_function(features)

    # 1 for normal, -1 for anomaly
    anomalies = (preds == -1).astype(int)

    # Map anomaly scores to threat levels
    threat_levels = []
    for score, is_anomaly in zip(anomaly_scores, anomalies):
        if is_anomaly:
            if score < -0.2:
                threat_levels.append('High')
            elif score < 0:
                threat_levels.append('Medium')
            else:
                threat_levels.append('Low')
        else:
            threat_levels.append('Low')
    return anomalies, threat_levels