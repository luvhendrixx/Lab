use notify_rust::Notification;

fn main() {
    let username = whoami::username().unwrap();

    let pic_dir = format!("/home/{}/Pictures/Icons/calvin.jpg", username); // holds the dir

    Notification::new()
        .summary("Firefox news!!!") // heading (&str)
        .body("This is a notification from Rust") // body (&str)
        .icon(&pic_dir) // (&str)
        .show() // sends noti to d-bus
        .unwrap();
}
