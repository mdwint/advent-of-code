const std = @import("std");
const print = std.debug.print;

pub fn main() !void {
    var a: [1000]i32 = undefined;
    var b: [1000]i32 = undefined;

    {
        var file = try std.fs.cwd().openFile("input.txt", .{});
        defer file.close();

        var buf_reader = std.io.bufferedReader(file.reader());
        var reader = buf_reader.reader();
        var buf: [16]u8 = undefined;

        var i: usize = 0;
        while (try reader.readUntilDelimiterOrEof(&buf, '\n')) |line| : (i += 1) {
            var parts = std.mem.tokenize(u8, line, " ");
            a[i] = try std.fmt.parseInt(i32, parts.next().?, 10);
            b[i] = try std.fmt.parseInt(i32, parts.next().?, 10);
        }
    }

    std.mem.sort(i32, &a, {}, std.sort.asc(i32));
    std.mem.sort(i32, &b, {}, std.sort.asc(i32));

    var total: u32 = 0;
    for (0.., a) |i, x| {
        const y = b[i];
        total += @abs(x - y);
    }
    print("Part 1: {}\n", .{total});

    var score: i32 = 0;
    for (a) |x| {
        for (b) |y| {
            if (y == x) {
                score += x;
            }
        }
    }
    print("Part 2: {}\n", .{score});
}
