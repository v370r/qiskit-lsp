import * as path from 'path';
import * as vscode from 'vscode';
import { workspace, ExtensionContext } from 'vscode';
import {PVSC_EXTENSION_ID, PYLANCE_EXTENSION_ID} from './common/constants';

import {
	LanguageClient,
	LanguageClientOptions,
	ServerOptions,
	TransportKind
} from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: ExtensionContext) {
	const serverModule = context.asAbsolutePath(
		path.join('server', 'out', 'server.js')
	);
	const pythonScriptPath = context.asAbsolutePath('python-scripts/script.py');
	vscode.window.showInformationMessage(`Hello qiskit-linter initialized! `);
	const debugOptions = { execArgv: ['--nolazy', '--inspect=6009'] };

	const serverOptions: ServerOptions = {
		run: { module: serverModule, transport: TransportKind.ipc },
		debug: {
			module: serverModule,
			transport: TransportKind.ipc,
			options: debugOptions,
		}
	};


	const clientOptions: LanguageClientOptions = {
		documentSelector: [{ scheme: 'file', language: 'python' }],
		synchronize: {
			fileEvents: workspace.createFileSystemWatcher('**/.clientrc')
		}
	};

	client = new LanguageClient(
		'languageServerExample',
		'Qiskit Language Server',
		serverOptions,
		clientOptions
	);
	let disposable = vscode.commands.registerCommand('qiskit-linter.start', () => {
		vscode.window.showInformationMessage('Hello VS code!');
	});

	disposable = vscode.commands.registerCommand('qiskit-linter.current_time', () => {
		const dateTime = new Date();
		vscode.window.showInformationMessage('Current time: ' + dateTime);

	});


	context.subscriptions.push(disposable);
	client.start();
}




export function deactivate(): Thenable<void> | undefined {
	if (!client) {
		return undefined;
	}
	vscode.window.showInformationMessage('Hello QISKIT uninstalled code!');
	return client.stop();
}
