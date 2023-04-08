use std::collections::HashSet;

use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct IngestRequest {
    pub project: Project,
    pub ingests: Vec<Ingest>
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Project {
    pub name: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Ingest {
    pub hash_id: String,
    pub ecosystem: String,
    pub dependencies: HashSet<Dependency>,
}

#[derive(Eq, Hash, PartialEq, Debug, Serialize, Deserialize)]
pub struct Dependency {
    pub name: String,
    pub version: String,
}
