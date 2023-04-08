use super::dependencies::Ingest;

pub mod maven;

pub trait Ecosystem {
    fn get_ingest(&self) -> Ingest;
}
