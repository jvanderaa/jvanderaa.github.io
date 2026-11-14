"""Render the X teaser using Pillow for titles and FFmpeg for video.

Run: python3 social/2026/chatgpt-dots/build_teaser.py
Requires Pillow and ffmpeg. Source screenshots and cover remain unchanged.
"""
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BUNDLE = ROOT / "content/posts/2026/chatgpt_dot_just_does_things"
W, H = 1280, 720
BG, INK, MUTED, TEAL = "#0b1d2c", "#edf5ff", "#acc4d6", "#50e3d1"
REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def text(draw, xy, value, size=54, color=INK, bold=False, spacing=12):
    draw.multiline_text(xy, value, fill=color,
                        font=ImageFont.truetype(BOLD if bold else REGULAR, size),
                        spacing=spacing)


def base(number, label):
    frame = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(frame)
    draw.line((64, 62, 1216, 62), fill="#25465c", width=1)
    text(draw, (64, 84), label, 20, TEAL, bold=True)
    text(draw, (64, 666), "JOSH VANDERAA  /  josh-v.com", 18, MUTED)
    for i in range(4):
        draw.rounded_rectangle((1112 + i * 28, 674, 1130 + i * 28, 679),
                               radius=2, fill=TEAL if i == number else "#345266")
    return frame


def insert(frame, path, box, radius=16):
    # Fit source into its frame without distorting or cropping its contents.
    source = Image.open(path).convert("RGB")
    fitted = ImageOps.contain(source, (box[2], box[3]), Image.Resampling.LANCZOS)
    mask = Image.new("L", fitted.size)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, fitted.width, fitted.height),
                                          radius=radius, fill=255)
    frame.paste(fitted, (box[0], box[1]), mask)


def blur_names(frame):
    """Redact both name mentions in the composed video frame before transitions.

    Coordinates refer to the 1280x720 slide, including the fitted screenshot.
    Applying this before encoding also redacts the storyboard and every fade.
    """
    filters = (
        "[0:v]split=3[base][full][short];"
        "[full]crop=242:42:628:392,boxblur=14:3:6:3[fullblur];"
        "[short]crop=62:38:298:526,boxblur=14:3:6:3[shortblur];"
        "[base][fullblur]overlay=628:392[first];"
        "[first][shortblur]overlay=298:526,format=rgb24[out]"
    )
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-filter_complex_threads", "1",
         "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{W}x{H}",
         "-i", "pipe:0", "-filter_complex", filters, "-map", "[out]", "-frames:v", "1",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"],
        input=frame.tobytes(), stdout=subprocess.PIPE, check=True,
    )
    return Image.frombytes("RGB", (W, H), result.stdout)


def slides():
    first = base(0, "A SMALL, USEFUL SURPRISE")
    draw = ImageDraw.Draw(first)
    text(draw, (64, 175), "My AI assistant\nspotted a conflict.", 63, bold=True)
    text(draw, (64, 385), "Before I asked.", 46, TEAL)
    text(draw, (64, 485), "A real moment with ChatGPT Dots.", 25, MUTED)
    insert(first, BUNDLE / "feature.png", (725, 198, 490, 300))

    second = base(1, "KERMIT'S HEADS-UP")
    draw = ImageDraw.Draw(second)
    text(draw, (64, 150), "A conference talk. A flight to catch.", 52, bold=True)
    text(draw, (64, 235), "The talk block started after my planned hotel departure.", 28, MUTED)
    insert(second, BUNDLE / "kermit_heads_up_dark.png", (64, 320, 1152, 310))
    second = blur_names(second)

    third = base(2, "WHAT I WANT NEXT")
    draw = ImageDraw.Draw(third)
    text(draw, (64, 155), "Now I want a team.", 66, bold=True)
    text(draw, (64, 257), "Specialist Dots. Shared context. Working together.", 29, MUTED)
    for i, (name, description) in enumerate([
        ("Travel", "Plans + schedules"), ("Writing", "Ideas + drafts"),
        ("Projects", "Code + research")
    ]):
        left = 64 + 396 * i
        if i < 2:
            draw.line((left + 350, 458, left + 396, 458), fill=TEAL, width=3)
        draw.rounded_rectangle((left, 360, left + 350, 560), radius=22,
                               fill="#122e43", outline="#315369", width=2)
        draw.rounded_rectangle((left + 26, 389, left + 48, 411), radius=7, fill=TEAL)
        text(draw, (left + 26, 437), name, 36, bold=True)
        text(draw, (left + 26, 502), description, 23, MUTED)

    fourth = base(3, "NEW ON THE BLOG")
    draw = ImageDraw.Draw(fourth)
    text(draw, (64, 155), "ChatGPT Dots Are\nStarting to\nJust Do Things", 58, bold=True)
    insert(fourth, BUNDLE / "feature.png", (770, 190, 440, 270))
    text(draw, (64, 449), "Read the story", 29, TEAL, bold=True)
    text(draw, (64, 508), "josh-v.com/\nchatgpt-dots-just-do-things/", 30, MUTED)
    return [first, second, third, fourth]


def main():
    durations = [4.5, 7, 4.5, 4.5]
    fade = 0.4
    with tempfile.TemporaryDirectory(prefix="dots-teaser-") as tmp:
        tmp = Path(tmp)
        frames = slides()
        command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
        for i, (frame, duration) in enumerate(zip(frames, durations)):
            path = tmp / f"slide-{i}.png"
            frame.save(path)
            command += ["-loop", "1", "-framerate", "30", "-t", str(duration), "-i", str(path)]
        filters = [f"[{i}:v]format=yuv420p,setsar=1,settb=AVTB[v{i}]" for i in range(4)]
        elapsed = durations[0]
        previous = "v0"
        for i in range(1, 4):
            output = f"fade{i}"
            filters.append(f"[{previous}][v{i}]xfade=transition=fade:duration={fade}:"
                           f"offset={elapsed - fade}[{output}]")
            previous = output
            elapsed += durations[i] - fade
        command += ["-filter_complex_threads", "1", "-filter_complex", ";".join(filters),
                    "-map", f"[{previous}]", "-an", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    str(HERE / "chatgpt-dots-teaser.mp4")]
        subprocess.run(command, check=True)
        # A contact sheet makes all title frames easy to review together.
        sheet = Image.new("RGB", (1280, 720), BG)
        for i, frame in enumerate(frames):
            sheet.paste(frame.resize((640, 360), Image.Resampling.LANCZOS),
                        ((i % 2) * 640, (i // 2) * 360))
        sheet.save(HERE / "storyboard.jpg", quality=92)
        frames[0].save(HERE / "poster.jpg", quality=92)


if __name__ == "__main__":
    main()
