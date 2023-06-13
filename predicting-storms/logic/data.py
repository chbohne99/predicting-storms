import numpy as np


def create_most_events_data(raw_df,most_events):
  frequency_data=raw_df[['YEARMONTH','STATE','EVENT_TYPE','EVENT_ID']]\
      .groupby(['YEARMONTH','STATE','EVENT_TYPE'],as_index=False)\
      .count().rename(columns={'EVENT_ID':'EVENT_NO'})
  most_events_data=frequency_data[frequency_data['EVENT_TYPE'].isin(most_events)]
  return most_events_data

def one_state(df,state):
  state_data = df[df['STATE']==state]
  for yearmonth in df.YEARMONTH.unique():
    if yearmonth in set(state_data.YEARMONTH.unique()):
      continue
    else:
      append_data = pd.DataFrame(dict(YEARMONTH=[yearmonth],STATE=[state],EVENT_TYPE=['Flood'],EVENT_NO=[0]))
      state_data = pd.concat([state_data,append_data],ignore_index=True)

  state_data = state_data[['YEARMONTH','EVENT_TYPE','EVENT_NO']]

  state_df = state_data.pivot(index='YEARMONTH',columns='EVENT_TYPE', values='EVENT_NO').fillna(0)

  #check columns of state_df
  #state_df must include 6 columns
  for event in most_events:
    if event in state_df.columns:
      continue
    else:
      state_df[event]=0.0

  X=state_df[state_df.index!=state_df.index[-1]].to_numpy()
  y=state_df[state_df.index==state_df.index[-1]].to_numpy()

  return X,y

def tensors_create(df,removed_states=None):
  X_list=[]
  y_list=[]
  states = df.STATE.unique()

  if removed_states:
    states=[x for x in states if x not in removed_states]

  for state in states:
    X,y=one_state(df,state)
    X_list.append(X)
    y_list.append(y)

  return np.array(X_list),np.array(y_list)
