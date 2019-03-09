import numpy as np
import pandas as pd

t = [0, 1, 2, 3, 4, 5]
amp = [150, 200, -10, 40, 500]

data = np.matrix([t, amp]).T
data_ = np.matrix([0, 1, 2, 3, 4, 5, 150, 200, -10, 40, 500]).T
print(data_)