//! Pure core of the OpenLeet server: content, study lists, scheduling, scoring and search.
//! Storage and HTTP live in the binary.

pub mod content;
pub mod lists;
pub mod model;
pub mod scheduler;
pub mod scorer;
pub mod search;
pub mod service;
