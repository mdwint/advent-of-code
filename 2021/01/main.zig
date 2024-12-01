const std = @import("std");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();

    var file = try std.fs.cwd().openFile("input.txt", .{});
    defer file.close();

    var buf_reader = std.io.bufferedReader(file.reader());
    var in_stream = buf_reader.reader();
    var buf: [1024]u8 = undefined;

    var prev: u32 = std.math.maxInt(u32);
    var num_increasing: usize = 0;

    // Part 1:
    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        const current = try std.fmt.parseInt(u32, line, 10);
        if (current > prev) num_increasing += 1;
        prev = current;
    }

    try stdout.print("{d}\n", .{num_increasing});
}
