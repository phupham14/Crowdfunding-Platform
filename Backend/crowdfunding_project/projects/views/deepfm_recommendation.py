import os

import joblib
import numpy as np
from django.conf import settings


class DeepFMRecommender:
    def __init__(self, artifacts_path=None):
        self.tf = self._import_tensorflow()
        self.artifacts_path = artifacts_path or os.path.join(
            settings.BASE_DIR,
            "projects",
            "DeepFM Exports",
        )
        self._load_artifacts()
        self._load_model()

    @staticmethod
    def _import_tensorflow():
        try:
            import tensorflow as tf
        except Exception as exc:
            raise RuntimeError(f"TensorFlow cannot be imported: {exc}") from exc
        return tf

    def _custom_objects(self):
        tf = self.tf

        class SquareLayer(tf.keras.layers.Layer):
            def call(self, inputs):
                return tf.square(inputs)

        class ReduceSumLayer(tf.keras.layers.Layer):
            def __init__(self, axis=None, keepdims=False, **kwargs):
                super().__init__(**kwargs)
                self.axis = axis
                self.keepdims = keepdims

            def call(self, inputs):
                return tf.reduce_sum(inputs, axis=self.axis, keepdims=self.keepdims)

            def get_config(self):
                config = super().get_config()
                config.update({
                    "axis": self.axis,
                    "keepdims": self.keepdims,
                })
                return config

        return {
            "SquareLayer": SquareLayer,
            "ReduceSumLayer": ReduceSumLayer,
        }

    def _artifact_path(self, filename):
        return os.path.join(self.artifacts_path, filename)

    def _load_artifacts(self):
        self.scaler = joblib.load(self._artifact_path("scaler.joblib"))
        self.label_encoders = joblib.load(self._artifact_path("label_encoders.joblib"))
        self.vocab_sizes = joblib.load(self._artifact_path("vocab_sizes.joblib"))
        self.num_features = joblib.load(self._artifact_path("numerical_features.joblib"))
        self.cat_features = joblib.load(self._artifact_path("categorical_features.joblib"))

    def _load_model(self):
        self.model = self.tf.keras.models.load_model(
            self._artifact_path("deepfm_model.keras"),
            custom_objects=self._custom_objects(),
            compile=False,
        )

    def recommend(self, user_data, candidate_items_df):
        scored_df = self.score_candidates(user_data, candidate_items_df)
        return scored_df["project_id"].tolist()

    def score_candidates(self, user_data, candidate_items_df):
        inference_df = candidate_items_df.copy()
        for key, value in user_data.items():
            inference_df[key] = value

        self._validate_features(inference_df)
        inputs = self._build_model_inputs(inference_df)

        scores = self.model.predict(inputs, verbose=0).flatten()
        inference_df["score"] = scores
        return inference_df.sort_values("score", ascending=False)

    def predict_scores(self, candidate_items_df):
        inference_df = candidate_items_df.copy()
        self._validate_features(inference_df)
        inputs = self._build_model_inputs(inference_df)
        return self.model.predict(inputs, verbose=0).flatten()

    def _validate_features(self, inference_df):
        required_features = self.cat_features + self.num_features
        missing_features = [
            column for column in required_features
            if column not in inference_df.columns
        ]
        if missing_features:
            raise ValueError(f"Missing DeepFM features: {missing_features}")

    def _build_model_inputs(self, inference_df):
        inputs = {}
        for column in self.cat_features:
            inputs[f"input_{column}"] = self._encode_categorical(
                inference_df,
                column,
            )

        numerical_df = (
            inference_df[self.num_features]
            .replace([np.inf, -np.inf], 0)
            .fillna(0)
        )
        inputs["numerical_input"] = self.scaler.transform(numerical_df)
        return inputs

    def _encode_categorical(self, inference_df, column):
        encoder = self.label_encoders[column]
        encoded_values = inference_df[column].astype(str).apply(
            lambda value: encoder.transform([value])[0]
            if value in encoder.classes_
            else 0
        )
        return encoded_values.to_numpy().reshape(-1, 1)
