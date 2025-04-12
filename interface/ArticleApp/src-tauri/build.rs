use std::fs;

fn main() {
    // Copy dataset files to the dataset directory
    // fs::copy(
    //     "../../../proto/system_backend.proto",
    //     "proto/system_backend.proto",
    // )
    // .unwrap_or_default();

    // Build protobuf
    tonic_build::compile_protos("proto/system_backend.proto").unwrap();

    tauri_build::build()
}
