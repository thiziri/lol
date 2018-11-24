# copute the performances variation according to the passage length
import os
import docopt
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from itertools import cycle, islice
from tqdm import tqdm

if __name__ == "__main__":
    args = docopt.docopt("""
            Usage:
                performances_in_passages.py --ep=<evaluated_passages> --m=<measures> --c=<clue> --o=<outputfolder> --s=<name_model_separator>

            Options:
                --ep=<evaluated_passages>    Evaluated passages folders.
                --m=<measures>   List of evaluation measures to plot separated bu comas.
                --c=<clue>    Desired file clue.
                --o=<outputfolder>    Where results will be stored.
                --s=<name_model_separator>    A separator to extract model's name from the evaluation file.
            """)
    print(args)
    all_measures = {}
    for measure in args["--m"].split(','):
        print("Reading {m} values of the different models ...".format(m=measure))
        all_measures[measure] = {}
        for passage in tqdm(os.listdir(args["--ep"])):
            for model_file in os.listdir(os.path.join(args["--ep"], passage)):
                if args["--c"] in model_file:
                    model = model_file.replace(args['--c'], '').replace(".eval", '').split(args["--s"])[0]
                    if model not in all_measures[measure]:
                        all_measures[measure][model] = {}  # add the evaluated model's name
                    with open(os.path.join(os.path.join(args["--ep"], passage), model_file), 'r') as res:
                        lines = res.readlines()
                        for line in lines:
                            if "all" in line and measure in line and measure+'0' not in line and '_'+measure not in line:
                                m_val = float(line.split()[2])  # get the measure value
                                all_measures[measure][model][int(passage)] = m_val
            # break
    # style
    plt.style.use('seaborn-darkgrid')
    SMALL_SIZE = 8
    MEDIUM_SIZE = 14
    BIGGER_SIZE = 16
    xmin, xmax = 0, 50
    ymin, ymax = 0, 35

    plt.rc('font', size=MEDIUM_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=BIGGER_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=BIGGER_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=BIGGER_SIZE)  # legend fontsize

    for measure in all_measures:
        data_frame = pd.DataFrame.from_dict(all_measures[measure])
        # print(measure+"\n", data_frame.T)
        df = data_frame
        print(df)
        df.columns = ['CANMM-MLP', 'CANMM-biLSTM']
        print(df)
        # to match the length of your data.
        my_colors = list(islice(cycle(['b', 'r', 'g', 'y', 'k']), None, len(df)))
        df.plot(style='.-', colormap='Paired')  # color=my_colors)  # , figsize=(15,25))
        plt.xlabel("#passage")
        plt.ylabel(measure)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=4, fancybox=True, shadow=True)
        plt.show()
