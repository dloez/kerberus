use std::path::PathBuf;
use std::fs;
use clap::Parser;
use analyzer::ecosystems::{maven, Ecosystem};

use crate::analyzer::dependencies::{Project, IngestRequest};

mod analyzer;
mod system;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    #[arg(short, long, default_value_t = String::from("."))]
    path: String
}

fn evaluate_directory(path: PathBuf) -> Vec<Box<dyn Ecosystem>> {
    let mut ecosystems: Vec<Box<dyn Ecosystem>> = Vec::new();
    if let Ok(entries) = fs::read_dir(&path) {
        for entry in entries.filter_map(|entry| entry.ok()) {
            let file_path = entry.path();
            if file_path.is_file() {
                if file_path.file_name().map(|f| f == "pom.xml").unwrap_or(false) {
                    ecosystems.push(Box::new(maven::MavenEcosystem {path: path.clone()}));
                }
            }
        }
    }
    ecosystems
}

fn main() {
    let args = Args::parse();

    let path = PathBuf::from(&args.path);
    if !path.exists() {
        println!("Given path does not exists");
        return
    }

    let ecocsystems = evaluate_directory(path);
    let project = Project {
        name: "example".to_string(),
    };
    let mut ingest_request = IngestRequest {
        project: project,
        ingests: Vec::new()
    };
    for ecosystem in ecocsystems {
        ingest_request.ingests.push(ecosystem.get_ingest());
    }

    let ingest = serde_json::to_string(&ingest_request).unwrap();
    let resp: String = ureq::post("http://127.0.0.1:8000/api/limbo/ingest/")
        .set("Content-Type", "application/json")
        .send_string(&ingest)
        .expect("Failed to send ingest to server")
        .into_string()
        .expect("Failed to read response from server");

    println!("{}", resp);
}
