from django.core.management.base import BaseCommand
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import joblib

class Command(BaseCommand):
    help = "Train the LSTM health prediction model"

    def handle(self, *args, **kwargs):
        file_path = "/Users/harisatyam/Documents/Vital_Sign_Monitoring_Alert_Notification/human_vital_signs_dataset_2024.csv"
        df = pd.read_csv(file_path)

        df.dropna(inplace=True)

        features = ['body_temperature', 'spo2', 'heart_rate', 'respiration_rate', 'bp_systolic', 'bp_diastolic']
        target = 'label'

        X = df[features].values
        y = df[target].values

        scaler = MinMaxScaler()
        X = scaler.fit_transform(X)

        X = X.reshape((X.shape[0], 1, X.shape[1]))

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = Sequential([
            LSTM(64, activation='relu', return_sequences=True, input_shape=(1, X.shape[2])),
            Dropout(0.2),
            LSTM(32, activation='relu'),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(3, activation='softmax')
        ])

        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        model.fit(X_train, y_train, epochs=20, batch_size=16, validation_data=(X_test, y_test))

        model.save("lstm_health_model.h5")
        joblib.dump(scaler, "scaler.pkl")

        self.stdout.write(self.style.SUCCESS("LSTM Model Trained and Saved Successfully!"))
