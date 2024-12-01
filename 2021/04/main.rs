use std::collections::{HashMap, HashSet, VecDeque};
use std::fmt;
use std::fs::File;
use std::hash::Hash;
use std::io::{self, BufRead};

fn main() {
    let file = File::open("input.txt").unwrap();
    let mut lines = io::BufReader::new(file).lines().map(|l| l.unwrap());

    let numbers_to_draw: Vec<i32> = lines
        .next()
        .unwrap()
        .split(',')
        .map(|l| l.parse::<i32>().unwrap())
        .collect();
    let mut boards = parse_boards(lines);

    for number in numbers_to_draw {
        let mut done = VecDeque::<usize>::new();
        for (i, board) in &mut boards.iter_mut().enumerate() {
            board.try_mark(number);
            if board.is_complete() {
                let score = board.calc_score() * number;
                println!("{}\nScore: {}\n", board, score);

                // Part 1:
                // return;

                // Part 2:
                done.push_front(i);
            }
        }
        for i in done {
            boards.swap_remove(i);
        }
    }
}

type Pos = (usize, usize);

#[derive(Default)]
struct Board {
    rows: Vec<Vec<i32>>,
    marked: HashSet<Pos>,
}

impl fmt::Display for Board {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for (y, row) in self.rows.iter().enumerate() {
            for (x, num) in row.iter().enumerate() {
                let c = if self.marked.contains(&(y, x)) {
                    "X".to_string()
                } else {
                    num.to_string()
                };
                write!(f, "{:>2} ", c)?;
            }
            write!(f, "\n")?;
        }
        Ok(())
    }
}

impl Board {
    fn try_mark(&mut self, number: i32) {
        for (y, row) in self.rows.iter().enumerate() {
            for (x, num) in row.iter().enumerate() {
                if num == &number {
                    self.marked.insert((y, x));
                    return;
                }
            }
        }
    }

    fn is_complete(&self) -> bool {
        let h = count_most_common(self.marked.iter().map(|(y, _)| y));
        if h == self.rows.len() {
            return true;
        }
        let w = count_most_common(self.marked.iter().map(|(_, x)| x));
        if w == self.rows[0].len() {
            return true;
        }
        false
    }

    fn calc_score(&self) -> i32 {
        let mut score = 0;
        for (y, row) in self.rows.iter().enumerate() {
            for (x, num) in row.iter().enumerate() {
                if !self.marked.contains(&(y, x)) {
                    score += num;
                }
            }
        }
        score
    }
}

fn count_most_common<T: Eq + Hash>(items: impl Iterator<Item = T>) -> usize {
    let mut counts = HashMap::<T, usize>::new();
    for x in items {
        *counts.entry(x).or_default() += 1;
    }
    *counts.values().max().unwrap_or(&0)
}

fn parse_boards(lines: impl Iterator<Item = String>) -> Vec<Board> {
    let mut boards = Vec::new();
    let mut b = Board::default();
    for line in lines {
        if line.is_empty() {
            if !b.rows.is_empty() {
                boards.push(b);
                b = Board::default();
            }
        } else {
            let row = line
                .split_whitespace()
                .map(|x| x.parse::<i32>().unwrap())
                .collect();
            b.rows.push(row);
        }
    }
    if !b.rows.is_empty() {
        boards.push(b);
    }
    boards
}
