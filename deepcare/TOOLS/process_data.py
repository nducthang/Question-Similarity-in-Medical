import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('./data.csv')

data['question_similaries'] = [None] * len(data)

data.to_csv('./data.csv', index=False)