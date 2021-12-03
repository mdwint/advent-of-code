use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};

fn main() {
    let file = File::open("input.txt").unwrap();
    let lines: Vec<String> = io::BufReader::new(file)
        .lines()
        .map(|l| l.unwrap())
        .collect();

    part1(lines);
}

fn part1(lines: Vec<String>) {
    let gamma_bin = most_common_bits(lines);
    let gamma = i32::from_str_radix(&gamma_bin, 2).unwrap();

    let epsilon_bin = flip(&gamma_bin);
    let epsilon = i32::from_str_radix(&epsilon_bin, 2).unwrap();

    println!("{}", gamma * epsilon);
}

fn most_common_bits(lines: Vec<String>) -> String {
    let mut result = String::new();
    for i in 0..lines[0].len() {
        let rank = count_ith_bits(i, &lines);
        let bit = rank.iter().max_by_key(|e| e.1).unwrap().0;
        result.push(*bit);
    }
    return result;
}

type Ranking = HashMap<char, usize>;

fn count_ith_bits(i: usize, lines: &Vec<String>) -> Ranking {
    let mut rank = HashMap::from([('0', 0), ('1', 0)]);
    for line in lines {
        let c = line.chars().nth(i).unwrap();
        *rank.get_mut(&c).unwrap() += 1;
    }
    rank
}

fn flip(bits: &str) -> String {
    return bits.replace("0", "_").replace("1", "0").replace("_", "1");
}
