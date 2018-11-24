from os import listdir
from os.path import join
import docopt
from tqdm import tqdm

# read unique values from column n in the file f
def read_values(f, n):
    inf = open(f, "r")
    lines = inf.readlines()
    result = []
    for x in lines:
        result.append(x.split(' ')[n])
    inf.close()
    return set(result)


if __name__ == '__main__':
    args = docopt.docopt("""
       Usage:
          merge_runs.py [--r=<runs_directory> | --rl=<run1>,<run2>...] --o=<output_directory>  --n=<name>

       Example:
          merge_runs.py [--r=<runs_directory> | --rl=<list>] --o=<output_directory> 

       Options:
          --r=<runs_directory>    Path to directory that contain TREC run files.
          --rl=<run1>,<run2>...    List of run files separated with ','.
          --o=<output_directory>    Directory where final run will be stored.
          --n=<name>    Name of the model.
       """)

    out = join(args["--o"], args["--n"])
    with open(out, 'w') as outfile:
        if bool(args["--r"]):
            print("Merging runs in ", args["--r"])
            for f in tqdm(listdir(args["--r"])):
                with open(join(args["--r"], f)) as infile:
                    for l in tqdm(infile):
                        outfile.write(l)
        elif bool(args["--rl"]):
            runs_list = args["--rl"][0].split(",")
            print("Merging runs ", args["--rl"])
            for f in tqdm(runs_list):
                with open(f) as infile:
                    for l in tqdm(infile):
                        outfile.write(l)

    print("Finished.\nResult saved to ", out)
