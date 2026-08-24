extern "C" {
    // tell rust the signature of the C++ function (what input(s) it needs)
    fn add_numbers(a: i32, b: i32) -> i32;
}

fn main() {
    let x = 15;
    let y = 27;

    // call the C++ fn inside the unsafe block
    let result = unsafe { add_numbers(x, y) };

    println!("Rust called C++! {} + {} = {}", x, y, result);
}
