import ast

code = """
from qiskit import QuantumCircuit as qc
from qiskit import QuantumRegister as qr 
from qiskit import ClassicalRegister as cr
from qiksit import *


bell = qc(1, 8)
cell = qc(2, 7)
"""

class QiskitVisitor(ast.NodeVisitor):
    def __init__(self):
        self.circuit_qubits = {}

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == 'QuantumCircuit':
                self.circuit_qubits[alias.asname] = None
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module_name = node.module
        for alias in node.names:
            if alias.name == 'QuantumCircuit':
                self.circuit_qubits[alias.asname] = None
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in self.circuit_qubits:
            if len(node.args) >= 1 and isinstance(node.args[0], ast.Num):
                qubits = node.args[0].n
                circuit_name = node.func.id
                self.circuit_qubits[circuit_name] = qubits
        self.generic_visit(node)

# Parse the code into an abstract syntax tree (AST)
parsed_code = ast.parse(code)

# Create an instance of QiskitVisitor
visitor = QiskitVisitor()

# Visit the AST nodes using the visitor
visitor.visit(parsed_code)

# Print QuantumCircuit variables and their associated qubits
print("QuantumCircuit variables and their associated qubits:")
for circuit, qubits in visitor.circuit_qubits.items():
    print(f"{circuit}: {qubits} qubits")
