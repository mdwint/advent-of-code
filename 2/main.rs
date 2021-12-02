use std::fs::File;
use std::io::{self, BufRead};

fn main() {
    let file = File::open("input.txt").unwrap();
    let lines: Vec<String> = io::BufReader::new(file)
        .lines()
        .map(|l| l.unwrap())
        .collect();

    let (mut h, mut d, mut a) = (0, 0, 0);

    for line in lines {
        let mut parts = line.split(" ");
        let cmd = parts.next().unwrap();
        let x: i32 = parts.next().unwrap().parse().unwrap();
        match cmd {
            "forward" => {
                h += x;
                d += a * x;
            }
            "down" => a += x,
            "up" => a -= x,
            _ => unreachable!(),
        };
    }

    println!("{} * {} = {}", h, d, h * d);
}
