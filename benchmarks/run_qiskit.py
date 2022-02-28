'''
    We consider the optimizations used up to level 3 with basis {u1, u2, u3, CNOT}
'''

from qiskit import QuantumCircuit
from qiskit.compiler import transpile
import os
import sys
import time

def count(d):
    sum = 0
    for k in d.keys():
        sum += d[k]
    return sum

def run(d, fname):
    
    f = open(fname, "w")
    
    f.write("name,1q,2q,total,time\n")
    
    for fname in os.listdir(d):

        print("Processing %s..." % fname)
        
        circ = QuantumCircuit.from_qasm_file(os.path.join(d, fname))

        start = time.perf_counter()
        new_circ = transpile(circ, basis_gates=['u1', 'u2', 'u3', 'cx'], coupling_map=None, optimization_level=3)
        stop = time.perf_counter()

        total_count = count(new_circ.count_ops())
        two_count = 0
        for inst, _, _ in new_circ.data:
            if (inst.name == "cx"):
                two_count += 1
        one_count = total_count - two_count
        print("\t Total %d, 1q %d, CNOT %d\n" % (total_count, one_count, two_count))

        f.write("%s,%d,%d,%d,%f\n" % (fname, one_count, two_count, total_count, stop - start))
        
    f.close()

if (len(sys.argv) != 3):
    print("Usage: python run_qiskit.py <input directory> <output file>")
    exit(-1)

run(sys.argv[1], sys.argv[2])

