# evaluation with measures at measures.py

import docopt
import collections
from measures import Measures
from tqdm import tqdm
from os.path import isfile
from collections import defaultdict
from numpy import average as avg


def get_qrels(qrels_file):
    """
    Read the qrels file to a dictionary: {(q_id, d_id):rel}
    :param qrels_file:
    :return:
    """
    # print("Reading Qrels ... ")
    qdr = {}
    with open(qrels_file, 'r') as qrels:
        for line in tqdm(qrels):
            if line is not None:
                q = line.strip().split()[0]
                doc = line.strip().split()[2]
                rel = int(line.strip().split()[3])
                qdr[(q, doc)] = rel
    # print("Qrels ok.")
    return collections.OrderedDict(sorted(qdr.items()))


if __name__ == "__main__":
    # print("\n------Begin------\n")
    args = docopt.docopt("""
        Usage:
            evaluate.py --r=<runs_file> [--m=<measures_list>] [--rj=<qrels>] --check=<indice> --rank=<ranks_interval>

        Options:
            --r=<run_file>    Give the run to be evaluated.
            --m=<measures_list>    Give the list of desired measures separated with comma.
            --rj=<qrels>    The TREC like relevance judgements.
            --check=<indice>    String to check in file name.
            --rank=<ranks_interval>    Give the list of ranks separated with ',' or a range 'n-m'.
        """)

    # print(args)
    qrels = get_qrels(args["--rj"]) if bool(args["--rj"]) else {}
    # print(qrels)

    if isfile(args["--r"]) and args["--check"] in args["--r"]:
        Q = {}
        with open(args["--r"], 'r') as f:
            for l in f:
                q = l.strip().split()[0]
                if q not in Q:
                    Q[q] = {'y_true': [], 'y_pred': []}
                if not bool(args['--rj']):
                    Q[q]['y_true'].append(int(l.strip().split()[-1]))
                else:
                    try:
                        Q[q]['y_true'].append(qrels[(q, l.strip().split()[2])])
                    except:
                        Q[q]['y_true'].append(0)
                Q[l.strip().split()[0]]['y_pred'].append(float(l.strip().split()[4]))

        eval_measures = ["map", "ndcg", "precision", "recall", "mse", "accuracy"]
        at_k = ["ndcg", "precision", "recall"]
        all_res = ["map", "mse", "accuracy"]
        dispatcher = {
            "map": Measures.map,
            "ndcg": Measures.ndcg,
            "precision": Measures.precision,
            "recall": Measures.recall,
            "mse": Measures.mse,
            "accuracy": Measures.accuracy
        }
        if bool(args["--m"]):
            eval_measures = args["--m"].split(',')
        k = [int(token) for token in args["--rank"].split(',')] if ',' in args["--rank"] \
            else [i for i in range(int(args["--rank"].split('-')[0]),
                                   int(args["--rank"].split('-')[1]) + 1,
                                   1)]  # [1, 3, 5, 10, 20]
        measures_all = defaultdict(list)
        for q in Q:
            # print("Question: ", q)
            res = {}  # {m: {} for m in eval_measures}
            for measure in eval_measures:
                if measure in all_res:
                    measure_f = dispatcher[measure]
                    val = round(measure_f(Q[q]['y_true'], Q[q]['y_pred']), 4)
                    res[measure] = val
                    print('{m}\t{q}\t{v}'.format(m=measure, q=q, v=val))
                    measures_all[measure].append(val)
                if measure in at_k:
                    measure_f = dispatcher[measure]
                    # del(res[measure])
                    # res.update({measure+'@%d' % (k[i]): {} for i in range(len(k))})
                    for i in range(len(k)):
                        measure_f_at_K = measure_f(k[i])
                        val = round(measure_f_at_K(Q[q]['y_true'], Q[q]['y_pred']), 4)
                        res[measure+'@%d' % (k[i])] = val
                        print('{m}\t{q}\t{v}'.format(m=measure+'@%d' % (k[i]), q=q, v=val))
                        measures_all[measure+'@%d' % (k[i])].append(val)
            # print(q, res)
        for measure in measures_all:
            print('{m}\tall\t{v}'.format(m=measure, v=round(avg(measures_all[measure]), 4)))
        # break

    # print("Evaluation finished.")

