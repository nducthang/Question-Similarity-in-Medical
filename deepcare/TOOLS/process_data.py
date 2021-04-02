import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('./data.csv')


# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'not_labeled', 'labeled'
not_labeded = len(data[data['is_labeled']==0])
labeled = len(data[data['is_labeled']==1])
n = len(data)
sizes = [not_labeded/n, labeled/n]
explode = (0, 0.1)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()