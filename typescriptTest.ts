import pyodide from 'pyodide';

async function parsePythonCode(pythonCode: string): Promise<any[]> {
    // Load the pyodide library
    await pyodide.loadPackage(['micropip']);
    await pyodide.runPythonAsync(`
        import micropip
        await micropip.install('astor')
    `);

    // Parse the Python code using pyodide
    await pyodide.runPythonAsync(`
        import ast
        import astor

        def parse_python_code(code):
            parsed_code = ast.parse(code)
            return astor.to_source(parsed_code)

        parsed_code = parse_python_code(${JSON.stringify(pythonCode)})
        self.postMessage(parsed_code)  # Send the parsed code back to the main thread
    `);

    // Wait for the message from the Web Worker with the parsed code
    return new Promise(resolve => {
        const worker = new Worker('worker.js');
        worker.onmessage = event => {
            resolve(event.data);
            worker.terminate();
        };
    });
}

// Example usage
const pythonCode = `
def greet(name):
    print("Hello, " + name + "!")
`;

parsePythonCode(pythonCode).then(parsedCode => {
    console.log(parsedCode);
});
