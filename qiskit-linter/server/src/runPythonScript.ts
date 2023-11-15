import { spawn } from 'child_process';

export class PythonExecutor {
    private pythonScriptPath: string;
    private pythonCode: string;
    private pythonProcess: import('child_process').ChildProcessWithoutNullStreams;
	private pythonOutput: string;

    constructor(pythonScriptPath: string, pythonCode: string) {
        this.pythonScriptPath = pythonScriptPath;
        this.pythonCode = pythonCode;
        this.pythonProcess = spawn('python', [this.pythonScriptPath, this.pythonCode], { stdio: 'pipe' });
		this.pythonOutput = '';
    }

    async execute():Promise<string>{
        let pythonOutput = '';

        this.pythonProcess.stdout.on('data', (data) => {
            pythonOutput += data.toString();
        });

        this.pythonProcess.stderr.on('data', (data) => {
            console.error(`Python error: ${data.toString()}`);
        });

        return new Promise((resolve, reject) => {
            this.pythonProcess.on('close', (code) => {
                if (code === 0) {
                    try {
                        resolve(pythonOutput);
                    } catch (error) {
                        console.error('Error parsing JSON:', error);
                        reject(error);
                    } 
                } else {
					if (code === 1) {
						console.log('Parsing Error');
					}
                }
            });
        });
    }

	getPythonOutput(): string {
        return this.pythonOutput;
    }

    cleanup(): void {
        if (this.pythonProcess) {
            this.pythonProcess.kill();
        }
    }
}