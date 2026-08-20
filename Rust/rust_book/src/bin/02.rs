fn main() {
    let mut count = 0;
    'counting_up: loop {
        // giving the loop a name
        // the ' is rust syntax for naming loops (loop label)
        println!("Count = {count}");
        let mut remaining = 10;

        loop {
            println!("Remaining = {remaining}");
            if remaining == 9 {
                break;
            }
            if count == 2 {
                break 'counting_up; // telling rust what loop we want to break out of
            }
            remaining -= 1;
        }
        count += 1;
    }
    println!("End count = {count}");
}
