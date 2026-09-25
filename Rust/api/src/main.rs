use axum::{Json, Router, routing::get};
use serde::Serialize;
use std::net::SocketAddr;

// define a struct that derives Serialize to auto convert it to JSON
#[derive(Serialize)]
struct MessageResponse {
    message: String,
    status: String,
}

// the async handler func for the endpoint
async fn hello() -> Json<MessageResponse> {
    let response = MessageResponse {
        message: "Hello from Rust API".to_string(),
        status: "Success".to_string(),
    };

    Json(response)
}

#[tokio::main]
async fn main() {
    // build the router and attach the GET handler to the /hello path
    let app = Router::new().route("/hello", get(hello));

    // define the sock addr
    let addr = SocketAddr::from(([127, 0, 0, 1], 8080));
    println!("Server running at http://{}", addr);

    // create a TCP listening and start serving the application
    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
