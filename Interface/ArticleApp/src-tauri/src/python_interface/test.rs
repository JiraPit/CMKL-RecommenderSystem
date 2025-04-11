#[cfg(test)]
mod tests {
    use super::super::call_python;

    #[test]
    fn test_call_python_test() {
        // Call the function and check the result
        let result = call_python("test", "test").unwrap();
        assert_eq!(result, "test");
    }
}
