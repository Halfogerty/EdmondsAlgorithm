import csv
import os
from typing import List


def parse_csv(inhandle) -> List[List[int]]:
    csv_reader = csv.reader(inhandle)
    adjacency_matrix = [[int(val) for val in row] for row in csv_reader]
    return adjacency_matrix


def get_outfile_name(infile_name: str) -> str:
    return os.path.splitext(infile_name)[0] + "_matching.csv"


def dump_csv(matrix: List[List[int]], filename: str) -> None:
    with open(filename, mode="w+") as outhandle:
        filewriter = csv.writer(outhandle, lineterminator="\n")
        for row in matrix:
            filewriter.writerow([str(val) for val in row])
