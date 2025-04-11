mod test;
use pyo3::prelude::*;

fn call_python(module: &str, function: &str) -> Result<String, String> {
    // Initialize the Python interpreter
    pyo3::prepare_freethreaded_python();

    let result = Python::with_gil(|py| -> PyResult<String> {
        // Add the directory containing the Python file to the Python path
        let sys = py.import("sys")?;
        let path = sys.getattr("path")?;
        path.call_method1("append", (".",))?;

        // Import the module
        let module = PyModule::import(py, format!("python.{module}"))?;

        // Call the function
        let result = module.getattr(function)?.call0()?.extract::<String>()?;

        Ok(result)
    })
    .map_err(|e| e.to_string())?;

    Ok(result)
}
