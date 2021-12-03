use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};

fn main() {
    let file = File::open("input.txt").unwrap();
    let lines: Vec<String> = io::BufReader::new(file)
        .lines()
        .map(|l| l.unwrap())
        .collect();

    //part1(lines);
    part2(lines);
}

fn part1(lines: Vec<String>) {
    let gamma_bin = most_common_bits(lines);
    let gamma = i32::from_str_radix(&gamma_bin, 2).unwrap();

    let epsilon_bin = flip(&gamma_bin);
    let epsilon = i32::from_str_radix(&epsilon_bin, 2).unwrap();

    println!("{}", gamma * epsilon);
}

fn part2(lines: Vec<String>) {
    let oxygen_bin = find_line(oxygen_crit, &lines);
    let oxygen = i32::from_str_radix(&oxygen_bin, 2).unwrap();

    let co2_bin = find_line(co2_crit, &lines);
    let co2 = i32::from_str_radix(&co2_bin, 2).unwrap();

    println!("{}", oxygen * co2);
}

type BitCriteria = fn(usize, usize) -> char;

fn oxygen_crit(zeros: usize, ones: usize) -> char {
    if zeros <= ones {
        '1'
    } else {
        '0'
    }
}

fn co2_crit(zeros: usize, ones: usize) -> char {
    if zeros <= ones {
        '0'
    } else {
        '1'
    }
}

fn find_line(bit_crit: BitCriteria, lines: &Vec<String>) -> String {
    let mut lines = lines.clone();

    for i in 0..lines[0].len() {
        let (zeros, ones) = count_ith_bits(i, &lines);

        let bit = if zeros == 0 {
            '1'
        } else if ones == 0 {
            '0'
        } else {
            bit_crit(zeros, ones)
        };

        lines.retain(|line| line.chars().nth(i).unwrap() == bit);
        if lines.len() == 1 {
            return lines[0].clone();
        }
    }

    panic!("not found");
}

fn most_common_bits(lines: Vec<String>) -> String {
    let mut result = String::new();
    for i in 0..lines[0].len() {
        let (zeros, ones) = count_ith_bits(i, &lines);
        let bit = if zeros > ones { '0' } else { '1' };
        result.push(bit);
    }
    result
}

fn count_ith_bits(i: usize, lines: &Vec<String>) -> (usize, usize) {
    let mut rank = HashMap::from([('0', 0), ('1', 0)]);
    for line in lines {
        let c = line.chars().nth(i).unwrap();
        *rank.get_mut(&c).unwrap() += 1;
    }
    (rank[&'0'], rank[&'1'])
}

fn flip(bits: &str) -> String {
    bits.replace("0", "_").replace("1", "0").replace("_", "1")
}
