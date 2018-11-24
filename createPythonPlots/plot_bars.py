import numpy as np
import matplotlib.pyplot as plt

values = (0.630661, # cdssm
0.630661, # dssm
0.80332, # arcii
0.768282, # arci
0.715542, # anmm
0.818289, # matchpyramid
0.759707, # mvlstm
0.790089, # amvlstm-q
0.780036, # amvlstm-a
0.774055) # amvlstm-q+a

ind = np.arange(len(values))  # the x locations for the groups
width = 0.8  # the width of the bars
MEDIUM_SIZE = 14
BIGGER_SIZE = 16
plt.rc('font', size=BIGGER_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels

fig, ax = plt.subplots()
rects1 = ax.bar(ind, values, width,
                color='blue')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Accuracy')
# ax.set_title('Accuracy values')
ax.set_xticks(ind)
ax.set_xticklabels(('CDSSM',
                    'DSSM',
                    'ARC_II',
                    'ARC_I',
                    'ANMM',
                    'MATCHPYRAMID',
                    'MV-LSTM',
                    'aMV-LSTM(Q)',
                    'aMV-LSTM(A)',
                    'aMV-LSTM(Q+A)'))
plt.xticks(rotation=20)
plt.hlines(y=0.759707, colors='red', xmin=0, xmax=len(values))
plt.hlines(y=max(values), colors='green', xmin=0, xmax=len(values), linestyles="--")
plt.ylim((0.5, 0.9))

# ax.legend()


def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(height), ha=ha[xpos], va='bottom')


# autolabel(rects1)

plt.show()