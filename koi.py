#!/bin/bash/python
from lightkurve import KeplerTargetPixelFile
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('koi.csv', header=0)

print df['rowid'][0]
