from tensorflow.keras import Sequential, regularizers
from tensorflow.keras.layers import LSTM,Dense,Dropout,Input,Lambda
from tensorflow.keras.optimizers.experimental import RMSprop
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

##initialize model
def initialize_model(input_shape):

  reg=regularizers.l1_l2(l2=0.005)

  model = Sequential()

  #input layer:
  model.add(Input(shape=input_shape))
  #1st LSTM layer: 64 units, activation tanh
  # model.add(LSTM(units=64, activation='tanh',return_sequences=True))

  #2nd LSTM layer: 32 units, activation=tanh
  model.add(LSTM(units=32,activation='tanh', return_sequences=False))

  #3rd Dense layer: 20 neurons, activation=relu
  model.add(Dense(20,activation='relu',kernel_regularizer=reg))

  #Dropout layer
  model.add(Dropout(rate=0.1))

  #4th predictive layer: output_features=6, activation = linear
  model.add(Dense(6,activation='linear'))

  print("✅ Model initialized")

  return model

def compile_model(model,learning_rate=0.0005):
  model.compile(loss='mean_squared_error',
                optimizer=RMSprop(learning_rate=learning_rate),
                metrics=['mse','mae'])
  print("✅ Model compiled")
  return model

def train_model(
        model,
        X,
        y,
        batch_size=16,
        patience=30,
        validation_data=None, # overrides validation_split
        validation_split=0.1
    ):
  es=EarlyStopping(
      patience=patience,
      restore_best_weights=True,
      monitor='val_loss',
      verbose=1)
  history=model.fit(
      X,
      y,
      validation_data=validation_data,
      validation_split=validation_split,
      epochs=200,
      batch_size=batch_size,
      callbacks=[es],
      verbose=0)
  print(f"✅ Model trained on {len(X)} sequences with min val MAE: {round(np.min(history.history['val_mae']), 2)}")

  return model,history


def init_baseline():
    # $CHALLENGIFY_BEGIN
    model = Sequential()
    model.add(Lambda(lambda x: x[:,None,-1,:]))
    adam = Adam(learning_rate=0.0005)
    model.compile(loss='mse', optimizer=adam, metrics=['mse',"mae"])
    print("✅ Baseline Model created")
    return model

def plot_history(history_longer):
    fig,axs=plt.subplots(1,3,figsize=(10,5))
    axs[0].plot(history_longer.history['loss'],label='train_loss')
    axs[0].plot(history_longer.history['val_loss'],label='val_loss')
    axs[0].set_title('loss')
    axs[0].legend()

    axs[1].plot(history_longer.history['mae'],label='mae')
    axs[1].plot(history_longer.history['val_mae'],label='val_mae')
    axs[1].legend()
    axs[1].set_title('mae')

    axs[2].plot(history_longer.history['mse'],label='mse')
    axs[2].plot(history_longer.history['val_mse'],label='val_mse')
    axs[2].legend()
    axs[2].set_title('mse')
    return plt.show()
