use std::time::Instant;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // start the clock when we ACTUALLY GET THE BYTES
    let start = Instant::now();

    // start the GET request
    // dyn (dynmaic) tells rust, your strict but..idk what will go in here at runtime, so just be prepared
    // handle errors
    // make the blocking request (makes the computer wait till the GET req is done)
    let response = reqwest::blocking::get("https://httpbin.org//stream-bytes/10000000")?; // the ? is for error checking BTS

    // don't try to interpret into text, GIVE ME THE RAW BYTES
    let raw_bytes = response.bytes()?; // handle the errors that may occur using the ? keyword(literally like a try/except in python)

    // start counting the raw bytes
    let byte_count = raw_bytes.len() as f64; // convet to f64 for dec math

    // hit stop on the time and record it
    let duration = start.elapsed();

    // convert duration to seconds
    let seconds = duration.as_secs_f64();

    // calc bytes per second
    let bytes_bytes_per_sec = byte_count / seconds;

    // convert to MBps
    // 1 MB = 1,000,000 bytes or 1,048,576 bytes depending on your standard)
    let mega_bytes_per_sec = (bytes_bytes_per_sec * 8.0) / 1_000_000.0;

    println!(
        "Downloaded: {} Bytes\nTime taken: {:.4} s\nSpeed: {:.2} B/s\nSpeed: {} Mbps ",
        byte_count, seconds, bytes_bytes_per_sec, mega_bytes_per_sec
    );

    if mega_bytes_per_sec < 1.0 {
        println!("Bro...your internet is ASSS CHEEKS 😂🫵")
    } else {
        println!("Not bad user...not bad 🤔");
    }
    Ok(())
}
