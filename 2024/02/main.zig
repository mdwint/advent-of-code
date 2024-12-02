const std = @import("std");
const print = std.debug.print;

const Report = struct {
    levels: [8]i8,
    len: u8,

    fn is_safe(self: *const Report) bool {
        var prev_sign: i8 = 0;

        for (1..self.len) |i| {
            const x = self.levels[i - 1];
            const y = self.levels[i];
            const diff = y - x;

            const sign: i8 = if (diff > 0) 1 else -1;
            if (sign != prev_sign and prev_sign != 0) return false;
            prev_sign = sign;

            const dist = @abs(diff);
            if (dist < 1 or dist > 3) return false;
        }

        return true;
    }

    fn without_level(self: *const Report, i: usize) Report {
        var r = Report{ .levels = self.levels, .len = self.len - 1 };
        for (i..r.len) |j| {
            r.levels[j] = r.levels[j + 1];
        }
        return r;
    }
};

pub fn main() !void {
    var reports: [1000]Report = undefined;

    {
        var file = try std.fs.cwd().openFile("input.txt", .{});
        defer file.close();

        var buf_reader = std.io.bufferedReader(file.reader());
        var reader = buf_reader.reader();
        var buf: [24]u8 = undefined;

        var i: usize = 0;
        while (try reader.readUntilDelimiterOrEof(&buf, '\n')) |line| : (i += 1) {
            var parts = std.mem.tokenizeAny(u8, line, " ");
            const report = &reports[i];

            var j: u8 = 0;
            while (parts.next()) |num| : (j += 1) {
                report.levels[j] = try std.fmt.parseInt(i8, num, 10);
            }
            report.len = j;
        }
    }

    var safe1: u16 = 0;
    var safe2: u16 = 0;

    for (reports) |r| {
        if (r.is_safe()) {
            safe1 += 1;
            continue;
        }

        for (0..r.len) |i| {
            if (r.without_level(i).is_safe()) {
                safe2 += 1;
                break;
            }
        }
    }

    print("Part 1: {}\nPart 2: {}\n", .{ safe1, safe1 + safe2 });
}
