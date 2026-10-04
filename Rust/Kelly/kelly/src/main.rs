use std::fs;

fn main() {
    // manipulates the local FS
    let entries = fs::read_dir("/sys/block").expect("Cannot read /sys/block");

    // this loops thru virtual disks (mounted snaps), not real hardware
    for entry in entries {
        let entry = entry.expect("Bad directory entry");
        // reads the file names we got from reading the /sys/block dir above
        let name = entry.file_name(); // returns an OsString and NOT a string
        // we use .to_string_lossy cuz filenames in Linux aren't guaranteed to be UTF-8 so this is a quick way to print the OsString
        println!("{}", name.to_string_lossy());
    }
}
