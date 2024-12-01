"""
Module for creating and using a gradient boosting classifier model.
"""
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import GradientBoostingClassifier


class ModelException(Exception):
    """Exception raised for errors in the model creation or prediction process."""
    pass


class ClassifierModel:
    """A class for creating and using a gradient boosting classifier model."""

    def __init__(self, path) -> None:
        self.path = path

    def create_model(self):
        """Creates and trains a gradient boosting model on the Iris dataset."""
        try:
            iris = load_iris()
            X, y = iris.data, iris.target

            model = GradientBoostingClassifier()
            model.fit(X, y)

            joblib.dump(model, self.path + '/trained_model_gb.pkl')

        except Exception as exc:
            raise ModelException(
                f'Model creation failed: {exc}'
            ) from exc

    def predict(self, features):
        """Predicts the class label for the given input data."""
        try:
            # Perform prediction
            model = joblib.load(self.path + '/trained_model_gb.pkl')
            prediction = model.predict(features)
            return prediction[0]

        except Exception as exc:
            raise ModelException(
                f'Model prediction failed: {exc}'
            ) from exc


def get_ml_service(path):
    """Creates an instance of ClassifierModel"""
    return ClassifierModel(path)
