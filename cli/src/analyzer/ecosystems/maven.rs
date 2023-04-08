use std::{path::PathBuf, collections::HashSet, fs::{File, remove_dir_all, create_dir_all}, io::{BufReader, BufRead}};
use crate::analyzer::dependencies::{Ingest, Dependency};
use super::Ecosystem;
use crate::system::shell::call_command;

pub struct MavenEcosystem {
    pub path: PathBuf
}

const CACHE_DIR: &str = &".kerberus";

impl Ecosystem for MavenEcosystem {
    fn get_ingest(&self) -> Ingest{
        let mut cache_dir = self.path.clone();
        cache_dir.push(CACHE_DIR);
        if cache_dir.exists() {
            remove_dir_all(&cache_dir).expect("Could not delete cache directory");
        }
        let mut dependencies_file = cache_dir.clone();
        dependencies_file.push("dependencies.log");

        create_dir_all(&cache_dir).expect("Could not create cache directory");
        call_command(&format!("mvn dependency:list -DoutputFile={:?} -DappendOutput=true", dependencies_file.as_os_str()), &self.path);
        let dependencies = read_dependencies(&dependencies_file);
        remove_dir_all(&cache_dir).expect("Could not delete cache directory");

        Ingest {
            hash_id: "50d858e0985ecc7f60418aaf0cc5ab587f42c2570a884095a9e8ccacd0f6545c".to_string(),
            ecosystem: "maven".to_string(),
            dependencies: dependencies
        }
    }
}

pub fn read_dependencies(file: &PathBuf) -> HashSet<Dependency> {
    let file = File::open(file).expect("Failed to open dependencies file");
    let reader = BufReader::new(file);

    let mut on_dependency = false;
    let mut dependencies: HashSet<Dependency> = HashSet::new();
    for line in reader.lines() {
        let line = line.unwrap();
        let line = line.trim();
        if !on_dependency && line == "The following files have been resolved:" {
            on_dependency = true;
            continue;
        }

        if on_dependency {
            if line == "" || line == "none" {
                on_dependency = false;
                continue;
            }
            
            let mut iter = line.split(":");
            let group_id = String::from(iter.next().unwrap_or(""));
            let artifact_id = String::from(iter.next().unwrap_or(""));
            let _packaging = String::from(iter.next().unwrap_or(""));
            let version = String::from(iter.next().unwrap_or(""));
            let _scope = String::from(iter.next().unwrap_or(""));

            let dependency = Dependency {
                name: format!("{}:{}", group_id, artifact_id),
                version: version
            };

            dependencies.insert(dependency);
        }
    }
    dependencies
}
