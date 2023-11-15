import ast

code = """
from qiskit import QuantumCircuit as qc
from qiskit import QuantumRegister as qr 
from qiskit import ClassicalRegister as cr
from qiksit import *
# from qiskit import QuantumCircuit as qc, QuantumRegister as qr


bell = qc(1,8)
cell = qc(2,7)
qreg = qr(3)
creg = cr(4)
qc1 = qc(qreg,creg)

"""

parsed_code = ast.parse(code)

import_modules = {}
Quantum_Circuits = {}

for node in ast.walk(parsed_code):
    if isinstance(node, ast.Import):
        for alias in node.names:
            import_modules[alias.name] = alias.asname or alias.name
    elif isinstance(node, ast.ImportFrom):
        module_name = node.module
        for alias in node.names:
            import_modules[f"{module_name}.{alias.name}"] = alias.asname or alias.name
    elif isinstance(node, ast.Assign):
        if node.value.func.id in [import_modules['qiskit.QuantumCircuit'], 'QuantumCircuit']:
            value = [0,0]
            if isinstance(node.value.args[0], ast.Num):
                value[0] = node.value.args[0].value
            if isinstance(node.value.args[1], ast.Num):
                value[1] = node.value.args[1].value
            Quantum_Circuits[node.targets[0].id] = value
        # elif node.value.func.id in [import_modules['qiskit.QuantumRegister'], 'QuantumRegister']:
        #     Quantum_Circuits[node.targets[0].id] = [node.value.args[0].value, 0]   
        pass
        

print(import_modules) 
print(Quantum_Circuits)

# class QiskitVisitor(ast.NodeVisitor):
#     def __init__(self):
#         self.circuit_qubits = {}
#         self.import_modules = {}

#     def visit_Import(self, node):
#         for alias in node.names:
#             self.import_modules[alias.name] = alias.asname or alias.name
#         self.generic_visit(node)

#     def visit_ImportFrom(self, node):
#         module_name = node.module
#         for alias in node.names:
#             self.import_modules[f"{module_name}.{alias.name}"] = alias.asname or alias.name
#         self.generic_visit(node)

#     def visit_Call(self, node):
#         if isinstance(node.func, ast.Name) and node.func.id in self.import_modules.values():
#             if len(node.args) >= 1 and isinstance(node.args[0], ast.Num):
#                 qubits = node.args[0].n
#                 circuit_name = node.func.id
#                 self.circuit_qubits[circuit_name] = qubits
#         self.generic_visit(node)

# parsed_code = ast.parse(code)

# visitor = QiskitVisitor()

# visitor.visit(parsed_code)

# print("QuantumCircuit variables and their associated qubits:")
# for circuit, qubits in visitor.circuit_qubits.items():
#     print(f"{circuit}: {qubits} qubits")