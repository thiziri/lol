import docopt
import os
from tqdm import tqdm
from os.path import join

def reconstruct(run_file, output, name):
    with open(join(output, "trec_" + name), 'w') as out_file:
        with open(run_file, 'r') as run:
            for line in tqdm(run):
                tokens = line.strip().split()
                q_id = tokens[0]
                # print(q_id)
                d_id = tokens[2]
                # print(d_id)
                new_line = line.replace(d_id, d_id.split("_")[0])
                # print(new_line)
                # break
                out_file.write("{l}".format(l=new_line))


if __name__ == "__main__":
    args = docopt.docopt("""
           Usage:
              reconstruct_trec_doc_ids.py --r=<run_file_or_folder> --o=<output_directory>  [--n=<name>] [--tocheck=<clue>]

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
        reconstruct(args["--r"], args["--o"], args["--n"])
    else:
        print("Reading run files ...")
        for file in os.listdir(args["--r"]):
            if args["--tocheck"] in file and ".sh" not in file:
                print(file)
                name = file.split('.')[1].split('.')[0]
                reconstruct(os.path.join(args["--r"], file), args["--o"], name)

    print("Done.")
