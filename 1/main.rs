use std::fs::File;
use std::io::{self, BufRead};

fn main() {
    let file = File::open("input.txt").unwrap();
    let numbers: Vec<i32> = io::BufReader::new(file)
        .lines()
        .map(|l| l.unwrap().parse().unwrap())
        .collect();

    // Part 1:
    //println!("{}", count_increasing(numbers.into_iter()));

    // Part 2:
    let windows = sum_sliding_windows(numbers).into_iter();
    println!("{}", count_increasing(windows));
}

fn sum_sliding_windows(numbers: Vec<i32>) -> Vec<i32> {
    let mut sums = Vec::new();
    for i in 0..numbers.len() - 2 {
        sums.push(numbers[i..i + 3].iter().sum());
    }
    sums
}

fn count_increasing(mut numbers: impl Iterator<Item = i32>) -> i32 {
    let mut num_increasing = 0;
    let mut prev = numbers.next().unwrap();
    for current in numbers {
        if current > prev {
            num_increasing += 1;
        }
        prev = current
    }
    num_increasing
}
