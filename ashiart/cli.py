"""Command-line interface for ASCII art generator."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import webbrowser

from .enhanced import EnhancedAsciiArtGenerator
from .io import demo_image

VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}


def _demo_path():
    """Procedural demo image, written once to the system temp directory."""
    path = os.path.join(tempfile.gettempdir(), "ashiart-demo.png")
    if not os.path.exists(path):
        demo_image().save(path)
    return path


def _is_video_source(source):
    """File extensions that need frame decoding instead of Pillow."""
    return (
        isinstance(source, str)
        and os.path.splitext(source)[1].lower() in VIDEO_EXTENSIONS
    )


def _fit_playback_width(source, width):
    """Shrink animation width so proportional rows fit the terminal.

    Only local Pillow-decodable files can be measured upfront; webcam,
    video, and remote sources keep the requested width.
    """
    if _is_video_source(source) or not isinstance(source, str):
        return width
    try:
        from .io import open_image

        with open_image(source) as probe:
            img_w, img_h = probe.size
    except (FileNotFoundError, ValueError, OSError):
        return width
    try:
        term_rows = shutil.get_terminal_size().rows
    except OSError:
        return width
    rows = int(img_h * width / img_w * 0.5)
    cap = max(term_rows - 4, 1)
    return max(int(width * cap / rows), 1) if rows > cap else width


def _render_frames(generator, pil_frames, ansi):
    """Convert (frame, duration_ms) pairs to (text, duration_ms) pairs."""
    return [
        (generator.generate_from_pil_image(frame, ansi=ansi), duration)
        for frame, duration in pil_frames
    ]


def _play_webcam(generator, args):
    """Stream webcam frames as ASCII until the device ends or Ctrl-C."""
    from .animate import CLEAR_SCREEN, CURSOR_HOME
    from .video import iter_webcam_frames

    sys.stdout.write(CLEAR_SCREEN)
    try:
        for frame in iter_webcam_frames(args.webcam):
            sys.stdout.write(CURSOR_HOME)
            sys.stdout.write(generator.generate_from_pil_image(frame, ansi=args.color))
            sys.stdout.write("\n")
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    return 0


def _play_animation_source(generator, args, source):
    """Play GIF frames or video files as a looping ASCII animation."""
    from .animate import iter_gif_frames, play_animation, save_animation_html

    if _is_video_source(source):
        from .video import iter_video_frames

        pil_frames = list(iter_video_frames(source))
    else:
        pil_frames = iter_gif_frames(source)
    if not pil_frames:
        raise ValueError("No frames found in animation input")
    texts = _render_frames(generator, pil_frames, args.color)
    durations = [duration for _, duration in pil_frames]
    if args.html:
        save_animation_html(
            [text for text, _ in texts],
            args.html,
            durations,
            args.font_size,
            bg=args.bg,
        )
        print(f"Animation HTML saved to {args.html}")
    play_animation(
        [text for text, _ in texts], durations, loops=args.loop, max_fps=args.max_fps
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="ashiart",
        description="Convert images to ASCII art (terminal, text or HTML)",
    )
    parser.add_argument(
        "image_path", nargs="?", help="Local image path, http(s) URL, or - for stdin"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Render a built-in calibration image (no input needed)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to save the ASCII art output (if not provided, prints to console)",
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        default=None,
        help="Width of the ASCII art in characters (default: terminal width, else 100)",
    )
    parser.add_argument(
        "-H",
        "--height",
        type=int,
        help="Height of the ASCII art in characters (defaults to proportional height)",
    )
    parser.add_argument(
        "-c",
        "--chars",
        help="Custom ASCII characters from darkest to lightest (e.g. '@#$%%*+;:,.')",
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["standard", "dense", "blocks", "braille"],
        default="standard",
        help="Rendering mode (default: standard)",
    )
    parser.add_argument(
        "--contrast",
        type=float,
        default=1.0,
        help="Contrast adjustment, 1.0 is neutral (default: 1.0)",
    )
    parser.add_argument(
        "--brightness",
        type=float,
        default=1.0,
        help="Brightness adjustment, 1.0 is neutral (default: 1.0)",
    )
    parser.add_argument(
        "--sharpness",
        type=float,
        default=1.0,
        help="Sharpness adjustment, 1.0 is neutral (default: 1.0)",
    )
    parser.add_argument(
        "--gamma",
        type=float,
        default=1.0,
        help="Tonal curve exponent, >1 darkens midtones (default: 1.0)",
    )
    parser.add_argument(
        "--resample",
        choices=["lanczos", "box"],
        default="lanczos",
        help="Downsampling filter (default: lanczos)",
    )
    parser.add_argument(
        "--edge-enhance",
        action="store_true",
        help="PIL edge-enhancement filter before mapping",
    )
    parser.add_argument(
        "--edges",
        action="store_true",
        help="Overlay directional edge glyphs (- / | \\) on contours",
    )
    parser.add_argument(
        "--edge-threshold",
        type=float,
        default=0.35,
        help="Normalized edge strength for --edges (default: 0.35)",
    )
    parser.add_argument(
        "--no-autocontrast",
        action="store_true",
        help="Disable automatic level stretching",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Bypass the URL download cache",
    )
    parser.add_argument(
        "--dithering", action="store_true", help="Apply dithering for more texture"
    )
    parser.add_argument(
        "--clahe",
        action="store_true",
        help="Local contrast equalization for flat photos",
    )
    parser.add_argument(
        "--dog",
        nargs=3,
        type=float,
        default=None,
        metavar=("SMALL", "LARGE", "AMPLIFY"),
        help="Difference-of-Gaussians detail emphasis, e.g. --dog 0.8 2.0 2.0",
    )
    parser.add_argument(
        "--invert", action="store_true", help="Invert brightness mapping"
    )
    parser.add_argument(
        "--color", action="store_true", help="ANSI truecolor terminal output"
    )
    parser.add_argument(
        "--play",
        action="store_true",
        help="Play GIF/video input as a looping ASCII animation",
    )
    parser.add_argument(
        "--webcam",
        nargs="?",
        const=0,
        default=None,
        type=int,
        metavar="INDEX",
        help="Live ASCII from a webcam device (default: 0, Ctrl-C stops)",
    )
    parser.add_argument(
        "--loop",
        type=int,
        default=0,
        help="Animation loop count, 0 loops forever (default: 0)",
    )
    parser.add_argument(
        "--max-fps",
        type=float,
        default=30,
        help="Animation frame-rate cap (default: 30)",
    )
    parser.add_argument(
        "--html", metavar="PATH", help="Also write color HTML output to PATH"
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the --html output in a browser (requires --html)",
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=8,
        help="Font size for HTML output (default: 8)",
    )
    parser.add_argument(
        "--bg",
        choices=["black", "white"],
        default="black",
        help="HTML page background (default: black)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if os.environ.get("NO_COLOR") or os.environ.get("TERM") == "dumb":
        args.color = False

    if args.open and not args.html:
        parser.error("--open requires --html PATH")

    if args.demo:
        source = _demo_path()
    elif not args.image_path and args.webcam is None:
        parser.error("an image path, URL, - for stdin, --demo, or --webcam is required")
    elif args.image_path == "-":
        source = sys.stdin.buffer.read()
    else:
        source = args.image_path

    width = args.width
    if width is None:
        try:
            width = shutil.get_terminal_size().columns if sys.stdout.isatty() else 100
        except OSError:
            width = 100
    if (args.play or args.webcam is not None) and args.height is None:
        width = _fit_playback_width(source, width)
    chars = list(args.chars) if args.chars else None
    generator = EnhancedAsciiArtGenerator(
        chars=chars,
        width=width,
        height=args.height,
        mode=args.mode,
        resample=args.resample,
    )
    generator.set_enhancement(
        contrast=args.contrast,
        brightness=args.brightness,
        sharpness=args.sharpness,
        gamma=args.gamma,
        autocontrast=not args.no_autocontrast,
        dithering=args.dithering,
        edge_enhance=args.edge_enhance,
        edges=args.edges,
        edge_threshold=args.edge_threshold,
        clahe=args.clahe,
        dog=tuple(args.dog) if args.dog else None,
        invert=args.invert,
    )

    try:
        if args.webcam is not None:
            return _play_webcam(generator, args)
        if args.play or _is_video_source(source):
            return _play_animation_source(generator, args, source)
        ascii_art = generator.generate_from_image(
            source, ansi=args.color, cache=not args.no_cache
        )

        if args.html:
            html = generator.generate_html(
                source,
                preserve_color=True,
                font_size=args.font_size,
                bg=args.bg,
                cache=not args.no_cache,
            )
            generator.save_html_to_file(html, args.html)
            print(f"HTML output saved to {args.html}")
            if args.open:
                webbrowser.open("file://" + os.path.abspath(args.html))

        if args.output:
            generator.save_to_file(ascii_art, args.output)
            print(f"ASCII art saved to {args.output}")
        else:
            # Avoid breaking pipes when output contains ANSI codes
            print(ascii_art)

        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
