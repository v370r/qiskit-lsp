import { TextDocument } from 'vscode-languageserver-textdocument';
import { Diagnostic, DiagnosticSeverity } from 'vscode-languageserver/node';
import { PythonExecutor } from './runPythonScript';
import { join } from 'path';
import { stringify } from 'querystring';

const pythonScriptPath = join(__dirname,'..', '..', 'server', 'src', 'python-scripts', 'script.py');


export class validateQubits {
	constructor() {

	}

	async validateImports(textDocument: TextDocument, maxNumberOfProblems: number) : Promise<Diagnostic[]>{
		const text = textDocument.getText();
		const diagnostics: Diagnostic[] = [];
		const output = await new PythonExecutor(pythonScriptPath, text).execute();
		const result = JSON.parse(output);

		if(result) {
			const importModulesList: {id: string; value: string}[] = result.importModules;
			const quantumCircuits: {id: string; value: number[]} = result.quantumCircuits;
			const errors: [] = result.errors;
			errors.forEach(error => {
				const diagnostic: Diagnostic = 
				{
					severity: DiagnosticSeverity.Error,
					range: {
						start: textDocument.positionAt(error[1]),
						end: textDocument.positionAt(error[2])
					},
					message: `${error[0]}`,
					source: 'Try to correctly initialize the gate'
				};
				diagnostics.push(diagnostic);
			});
		}	
		return diagnostics;
	}
}


