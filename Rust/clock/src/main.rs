use chrono::{Local, NaiveTime, Timelike};
use std::io::{self, Write};
use std::thread;
use std::time::Duration;

fn main() {
    print!("Alarm (HH:MM, 24h)? ");
    io::stdout().flush().unwrap();

    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("couldn't read input");

    // for case forgiveness on AM/PM
    let trimmed = input.trim().to_uppercase();

    let alarm_time = NaiveTime::parse_from_str(&trimmed, "%I:%M %p")
        .expect("didn't understand that time, use HH:MM");

    println!("Alarm set for: {}", alarm_time.format("%I:%M %p"));

    let mut already_rang = false;

    loop {
        let now = Local::now();
        let matches = now.hour() == alarm_time.hour() && now.minute() == alarm_time.minute();

        if matches && !already_rang {
            print!("\r⏰ ALARM! IT IS {}! \x07\n", now.format("%I:%M %p"));
            io::stdout().flush().unwrap();
            for _ in 0..5 {
                print!("\x07");
                io::stdout().flush().unwrap();
                thread::sleep(Duration::from_secs(1));
            }
            break; // exits the outer loop, programme ends and sheell prompt returns
        } else if !matches {
            already_rang = false; // reset once the minute has passed
            print!("\rCurrent Time: {}", now.format("%I:%M:%S"));
            io::stdout().flush().unwrap();
        }

        thread::sleep(Duration::from_secs(1));
    }
}
