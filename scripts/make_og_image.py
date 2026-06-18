import struct
import zlib
from pathlib import Path

w, h = 1200, 630
raw = b""
for y in range(h):
    raw += b"\x00"
    for x in range(w):
        if x < 80 or y < 80 or x > w - 80 or y > h - 80:
            raw += bytes([20, 20, 19])
        elif (x - 600) ** 2 + (y - 200) ** 2 < 8100:
            raw += bytes([217, 119, 87])
        else:
            raw += bytes([250, 249, 245])
comp = zlib.compress(raw, 9)


def chunk(tag: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + tag
        + data
        + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    )


png = b"\x89PNG\r\n\x1a\n"
png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
png += chunk(b"IDAT", comp)
png += chunk(b"IEND", b"")

out = Path(__file__).resolve().parent.parent / "docs" / "assets" / "og-cover.png"
out.write_bytes(png)
print(out)
