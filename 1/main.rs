use std::fs::File;
use std::io::{self, BufRead};

fn main() {
    let file = File::open("input.txt").unwrap();
    let numbers: Vec<i32> = io::BufReader::new(file)
        .lines()
        .map(|l| l.unwrap().parse::<i32>().unwrap())
        .collect();

    // Part 1:
    //println!("Increasing: {}", count_increasing(numbers.into_iter()));

    // Part 2:
    let windows = sum_sliding_windows(numbers).into_iter();
    println!("Increasing: {}", count_increasing(windows));
}

fn sum_sliding_windows(numbers: Vec<i32>) -> Vec<i32> {
    let n = numbers.len();
    let mut sums = Vec::new();

    for i in 0..n {
        let j = i + 3;
        if j > n {
            break;
        }
        sums.push(numbers[i..j].iter().sum());
    }

    sums
}

fn count_increasing(mut numbers: impl Iterator<Item = i32>) -> i32 {
    let mut prev = numbers.next().unwrap();
    let mut num_increasing = 0;

    println!("{} : (N/A)", prev);
    for current in numbers {
        let diff = current - prev;
        println!("{} : {}", current, diff);
        if diff > 0 {
            num_increasing += 1;
        }
        prev = current
    }

    num_increasing
}
