// 1km = 1000m
fn km_to_m(km: u32) -> u32 {
    km * 1000
}

fn m_to_km(m: u32) -> u32 {
    m / 1000
}

fn main() {
    let km: u32 = 1;
    let m = km_to_m(km);
    println!("1km to m is {}", m);

    let m_to_km = m_to_km(m);
    println!("1000m to km is {}", m_to_km);
}
