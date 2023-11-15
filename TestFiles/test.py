from qiskit import QuantumCircuit as qc
from qiskit import 


bell = qc(9,9)
bell.h(2)
bell.h(1)
cell = qc(8,9)
bell.x(8)
bell.x(0)
cell = qc(1,4)
cell.h(6)
cell.h(0)
qell = QuantumCircuit(2,6)
qell.x(1)




