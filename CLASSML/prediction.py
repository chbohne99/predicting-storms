from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

def prediction(df):
    '''
    Evaluate the model and compare it to baseline score
    '''

    baseline_score = df.encoded_f_scale.value_counts()[0]/len(df)
    print(f'The Baseline Score amounts to {round(baseline_score,2)}!')

    X = df.drop(columns = 'encoded_f_scale')
    y = df['encoded_f_scale']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                        random_state=42)
    y_pred = []
    return y_pred
