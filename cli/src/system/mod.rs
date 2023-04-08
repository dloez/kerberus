#[cfg(windows)]
pub mod shell {
    use std::{process::Command, path::PathBuf};

    pub fn call_command(command: &str, path: &PathBuf) -> String {
        let mut wrapper = Command::new("powershell");
        wrapper.current_dir(path);
    
        let output = wrapper.arg("-command")
            .arg(format!("\"{}\"", command))
            .output()
            .expect("failed to run powershell command");
    
        String::from_utf8(output.stdout).expect("failed to convert output to String")
    }
}

#[cfg(not(windows))]
pub mod shell {
    use std::{process::Command, path::PathBuf};

    pub fn call_command(command: &str, path: &PathBuf) -> String {
        let mut wrapper = Command::new("sh");
        wrapper.current_dir(path);
    
        let output = wrapper.arg("-c")
            .arg(command)
            .output()
            .expect("failed to run powershell command");
    
        String::from_utf8(output.stdout).expect("failed to convert output to String")
    }
}
