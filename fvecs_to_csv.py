import numpy as np
import sys
import pandas as pd

def read_fvecs(file_path):
    try:
        with open(file_path, "rb") as f:
            data = np.fromfile(f, dtype=np.float32)
            d_view = data.view(dtype=np.int32)
            dim = d_view[0]
            num_vectors = int (data.size / (dim+1))
            vectors = data.reshape(num_vectors, dim + 1)
            vectors = vectors[:, 1:]
    except IOError:
        sys.exit("Could not open file: " + file_path)
    return vectors

def main():
    if len(sys.argv) != 4:
        print("Usage: python fvecs_to_csv.py [input file] [output file] [sample size]")
        return 1
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    sample_size = int(sys.argv[3])
    data = read_fvecs(in_file)
    data = data[:sample_size,:]
    try:
        df = pd.DataFrame(data)
        df.to_csv(out_file, header=False, index=False)
    except IOError:
        sys.exit("Could not create file: " + out_file)
    print(f"Converted {in_file} to {out_file}\n")

if __name__ == '__main__':
    main()
