const std = @import("std");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();

    var file = try std.fs.cwd().openFile("input.txt", .{});
    defer file.close();

    var buf_reader = std.io.bufferedReader(file.reader());
    var in_stream = buf_reader.reader();
    var buf: [1024]u8 = undefined;

    var horiz: usize = 0;
    var depth: usize = 0;
    var aim: usize = 0;

    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        var parts = std.mem.tokenize(line, " ");
        const cmd = parts.next() orelse unreachable;
        const x = try std.fmt.parseInt(u32, parts.next() orelse unreachable, 10);

        if (std.mem.eql(u8, cmd, "forward")) {
            horiz += x;
            depth += aim * x;
        } else if (std.mem.eql(u8, cmd, "down")) {
            aim += x;
        } else if (std.mem.eql(u8, cmd, "up")) {
            aim -= x;
        }
    }

    try stdout.print("{d}\n", .{horiz * depth});
}
