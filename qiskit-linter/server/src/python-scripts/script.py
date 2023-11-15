import json
import sys
import ast
from enum import Enum

class AstObject:
    def __init__(self, ast_line, start, end):
        self.ast_line = ast_line
        self.start = start
        self.end = end

class ErrorType(Enum):
    NO_ARG = "Gate initialized with no qubits. Please initialize with qubit"
    WRONG_QUBIT = "This qubit is not available. Please provide a valid qubit"
    INFO_TYPE = "Info test"

code = sys.argv[1]

def parse_line_by_line(code):
    lines = code.split('\n')
    parsed_lines = []
    pointerstart = 0
    pointerEnd = 0

    for line in lines:
        try:
            parsed_line = ast.parse(line, mode='exec')
            pointerEnd = pointerstart + len(line)
            parsed_lines.append(AstObject(parsed_line, pointerstart, pointerEnd))
            pointerstart = pointerEnd + 1
        except SyntaxError as e:
            pointerEnd = pointerstart + len(line)
            pointerstart = pointerEnd + 1
            

    return parsed_lines



parsed_code = parse_line_by_line(code)

if parsed_code:
    import_modules = {}
    Quantum_Circuits = {}
    errors = []
    infos = []

    for astObject in parsed_code:
        for node in ast.walk(astObject.ast_line):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_modules[alias.name] = alias.asname or alias.name
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module
                for alias in node.names:
                    import_modules[f"{module_name}.{alias.name}"] = alias.asname or alias.name
            elif isinstance(node, ast.Assign):
                if node.value.func.id in [import_modules.get('qiskit.QuantumCircuit', None), 'QuantumCircuit', import_modules.get('qiskit.*', None)]:
                    value = [0,0]
                    if isinstance(node.value.args[0], ast.Num):
                        value[0] = node.value.args[0].value
                    if isinstance(node.value.args[1], ast.Num):
                        value[1] = node.value.args[1].value
                    Quantum_Circuits[node.targets[0].id] = value
                # elif node.value.func.id in [import_modules['qiskit.QuantumRegister'], 'QuantumRegister']:
                #     Quantum_Circuits[node.targets[0].id] = [node.value.args[0].value, 0]   
            elif isinstance(node, ast.Expr):
                if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute) and isinstance(node.value.func.value, ast.Name):
                    if node.value.func.value.id in Quantum_Circuits.keys():
                        for args in node.value.args:
                            if(args.value>= Quantum_Circuits[node.value.func.value.id][0] or args.value<0):
                                errors.append([ErrorType.WRONG_QUBIT.value, astObject.start, astObject.end])
                
            
    result = {
        'importModules': import_modules,
        'quantumCircuits': Quantum_Circuits,
        'errors': errors
    }

    print(json.dumps(result))


