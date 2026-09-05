fn main() {
    let number: [i32; 5] = [25, 24, 23, 22, 30];

    let outcome = find_max(&number);

    match outcome {
        // change 'outcome' to 'num' to print the actual values
        Some(num) => println!("The greatest number is: {}", num),
        // completed the None arm with a fallback action
        None => println!("This list was empty"),
    }
}

fn find_max(numbers: &[i32]) -> Option<i32> {
    // returns true or false if numbers var is empty
    // if it IS empty, it returns None
    if numbers.is_empty() {
        return None;
    }
    // grabs the number at postion 0 (which in this case is 25)
    let mut max = numbers[0];

    // tells rust to skip the first index (0) and start at index 1
    // and give me a view (a slice) of all the remaining elements
    for &num in &numbers[1..] {
        // if the number in index 1 going foward
        // is greater than the number at postion 0
        // replace the number at position 0 with the greator number
        if num > max {
            max = num;
        }
    }
    // return Some value which is max
    Some(max)
}
