use std::fs::File;
use std::io::{self, BufRead};

fn main() {
    let file = File::open("input.txt").unwrap();
    let lines: Vec<String> = io::BufReader::new(file)
        .lines()
        .map(|l| l.unwrap())
        .collect();

    let (mut horiz, mut depth, mut aim) = (0, 0, 0);

    for line in lines {
        let mut parts = line.split(" ");
        let cmd = parts.next().unwrap();
        let x: i32 = parts.next().unwrap().parse().unwrap();
        match cmd {
            "forward" => {
                horiz += x;
                depth += aim * x;
            }
            "down" => aim += x,
            "up" => aim -= x,
            _ => unreachable!(),
        };
    }

    println!("{}", horiz * depth);
}
