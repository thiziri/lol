import docopt
import os
from tqdm import tqdm
from collections import defaultdict
from os.path import join
from numpy import average as avg
from collections import OrderedDict

def aggregate_passages(run_file, output, name):
    results = defaultdict(list)
    with open(run_file, 'r') as run:
        for line in tqdm(run):
            tokens = line.strip().split()
            q_id = tokens[0]
            d_id = tokens[2].split('_p')[0]
            results[(q_id, d_id)].append(float(tokens[4]))
    # print("Writing results ...")
    if not os.path.exists(output):
        os.mkdir(output)
    out_avg = open(join(output, "avg_" + name), 'w')
    with open(join(output, "max_" + name), 'w') as out_max:
        for result in tqdm(OrderedDict(sorted(results.items()))):
            out_max.write("{q}\tQ0\t{d}\t1\t{s}\t{m}\t0\n".format(q=result[0], d=result[1], s=max(results[result]),
                                                                  m=name))
            out_avg.write("{q}\tQ0\t{d}\t1\t{s}\t{m}\t0\n".format(q=result[0], d=result[1], s=avg(results[result]),
                                                                  m=name))
    out_avg.close()

if __name__ == "__main__":
    args = docopt.docopt("""
           Usage:
              aggregate_passages.py --r=<passages_run_file_or_folder> --o=<output_directory> [--n=<name>] [--tocheck=<clue>]

           Example:
              aggregate_passages.py --r=passages --o=path/to/output --n=documents.run 

           Options:
              --r=<passages_run_file>    TREC run file or folder of files of retrieved passages.
              --o=<output_directory>    Directory where final run will be stored.
              --n=<name>    Name of the model, optional.
              --tocheck=<clue>    Give the desired file name clue.
           """)

    if os.path.isfile(args["--r"]):
        print("Reading run file ...")
        aggregate_passages(args["--r"], args["--o"], args["--n"])
    else:
        print("Reading run files ...")
        for file in os.listdir(args["--r"]):
            if args["--tocheck"] in file and ".sh" not in file:
                print(file)
                name = file.split('.')[1].split('_')[0]
                aggregate_passages(os.path.join(args["--r"], file), args["--o"], name)

    print("Done.")
