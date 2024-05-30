import numpy as np
import h5py
import sys

in_file = "siftsmall/siftsmall_base.fvecs"
out_file = "input/siftsmall_base.hdf5"

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
        print("Usage: python fvecs_to_hdf5.py [input file] [output file] [sample size]")
        return 1
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    sample_size = int(sys.argv[3])

    matrix = read_fvecs(in_file)
    matrix = matrix[:sample_size,:]

    try:
    # save the matrix to a hdf5 file
        with h5py.File(out_file, "w") as f:
            f.create_dataset("*", data=matrix, dtype=np.float64)
    except IOError:
        sys.exit("Could not create file: " + out_file)
    #with h5py.File(out_file, "r") as f:
    #    loaded_matrix = f["*"][:]
    # print(loaded_matrix.shape)

    print(f"Converted {in_file} to {out_file}\n")

if __name__ == '__main__':
    main()
