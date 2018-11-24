# evaluation with measures at measures.py

import docopt
import collections
from measures import Measures
from tqdm import tqdm
from os.path import isfile


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
            evalRuns.py --r=<runs_file> [--m=<measures_list>] [--rj=<qrels>]

        Options:
            --r=<runs_folder>    Give the folder of runs to be evaluated.
            --m=<measures_list>    Give the list of desired measures separated with comma.
            --rj=<qrels>    The TREC like relevance judgements.
        """)

    # print(args)
    qrels = get_qrels(args["--rj"]) if bool(args["--rj"]) else {}
    # print(qrels)

    if isfile(args["--r"]):
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
        k = [1, 3, 5, 10, 20]
        for q in Q:
            # print("Question: ", q)
            res = {}  # {m: {} for m in eval_measures}
            for measure in eval_measures:
                if measure in all_res:
                    measure_f = dispatcher[measure]
                    val = round(measure_f(Q[q]['y_true'], Q[q]['y_pred']), 4)
                    res[measure] = val
                    print('{m}\t{q}\t{v}'.format(m=measure, q=q, v=val))
                if measure in at_k:
                    measure_f = dispatcher[measure]
                    # del(res[measure])
                    # res.update({measure+'@%d' % (k[i]): {} for i in range(len(k))})
                    for i in range(len(k)):
                        measure_f_at_K = measure_f(k[i])
                        val = round(measure_f_at_K(Q[q]['y_true'], Q[q]['y_pred']), 4)
                        res[measure+'@%d' % (k[i])] = val
                        print('{m}\t{q}\t{v}'.format(m=measure+'@%d' % (k[i]), q=q, v=val))
            # print(q, res)
            # break

    # print("Evaluation finished.")

