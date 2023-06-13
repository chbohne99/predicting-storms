from registry import load_model
from preprocessing import preprocessing

def prediction(X_pred):


    X_processed = preprocessing(X_pred)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                        random_state=42)
    y_pred = []
    return y_pred
