import csv
import sys

def preprocess(src, dest):
    """clean up messy coast capital csv"""
    with open(dest, "w") as destfile:
        with open(src) as srcfile:
            r = csv.reader(srcfile)
            for row in r:
                # skip blank lines
                if len(row) > 0:
                    # who needs that first column
                    row = row[1:]
                    # split that middle column into three:
                    # description, payee, source
                    row = row[0:1] + [" ".join([row[1][:29].strip(), row[1][29:58].strip(), row[1][58:].strip()])] + row[2:]
                    print(",".join(row), file=destfile)


if __name__ == "__main__":
    preprocess(sys.argv[1], sys.argv[2])
