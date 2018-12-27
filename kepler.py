#!/bin/bash/python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
run0 = 'corot2b_all.txt'
run1 = 'hatp36b_R_all.txt'
run2 = 'wasp52b_all.txt'
run = run2

df = pd.read_csv(run ,sep='\t', header=0)
y=0
diff = (df['Norm_Flux']-df['Norm_Flux'].mean())
time = df['BJD_TDB']
plt.plot(time, diff, label=run)
plt.show()
