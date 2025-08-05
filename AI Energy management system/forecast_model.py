import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

def forecast_energy(df):
    df = df.copy()
    df["hour"] = pd.to_datetime(df["datetime"]).dt.hour
    features = df[["temperature", "humidity", "wind_speed", "hour"]]
    target = df["total_energy"]

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2)
    model = XGBRegressor()
    model.fit(X_train, y_train)
    forecast = model.predict(features)
    return forecast
