"""Command-line interface for ASCII art generator."""

import argparse
import sys

from .enhanced import EnhancedAsciiArtGenerator


def build_parser():
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="ashiart",
        description="Convert images to ASCII art (terminal, text or HTML)",
    )
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument(
        "-o", "--output",
        help="Path to save the ASCII art output (if not provided, prints to console)"
    )
    parser.add_argument(
        "-w", "--width",
        type=int,
        default=100,
        help="Width of the ASCII art in characters (default: 100)"
    )
    parser.add_argument(
        "-H", "--height",
        type=int,
        help="Height of the ASCII art in characters (defaults to proportional height)"
    )
    parser.add_argument(
        "-c", "--chars",
        help="Custom ASCII characters from darkest to lightest (e.g. '@#$%%*+;:,.')"
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["standard", "dense", "blocks", "braille"],
        default="standard",
        help="Rendering mode (default: standard)"
    )
    parser.add_argument("--contrast", type=float, default=1.0,
                        help="Contrast adjustment, 1.0 is neutral (default: 1.0)")
    parser.add_argument("--brightness", type=float, default=1.0,
                        help="Brightness adjustment, 1.0 is neutral (default: 1.0)")
    parser.add_argument("--sharpness", type=float, default=1.0,
                        help="Sharpness adjustment, 1.0 is neutral (default: 1.0)")
    parser.add_argument("--edge-enhance", action="store_true",
                        help="Enhance edges before mapping")
    parser.add_argument("--edges", action="store_true",
                        help="Overlay directional edge glyphs (- / | \\) on contours")
    parser.add_argument("--edge-threshold", type=float, default=0.35,
                        help="Normalized edge strength for --edges (default: 0.35)")
    parser.add_argument("--no-autocontrast", action="store_true",
                        help="Disable automatic level stretching")
    parser.add_argument("--dithering", action="store_true",
                        help="Apply dithering for more texture")
    parser.add_argument("--invert", action="store_true",
                        help="Invert brightness mapping")
    parser.add_argument("--color", action="store_true",
                        help="ANSI truecolor terminal output")
    parser.add_argument("--html",
                        metavar="PATH",
                        help="Also write color HTML output to PATH")
    parser.add_argument("--font-size", type=int, default=8,
                        help="Font size for HTML output (default: 8)")
    return parser


def main(argv=None):
    """Run the command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)

    chars = list(args.chars) if args.chars else None
    generator = EnhancedAsciiArtGenerator(
        chars=chars,
        width=args.width,
        height=args.height,
        mode=args.mode,
    )
    generator.set_enhancement(
        contrast=args.contrast,
        brightness=args.brightness,
        sharpness=args.sharpness,
        autocontrast=not args.no_autocontrast,
        dithering=args.dithering,
        edge_enhance=args.edge_enhance,
        edges=args.edges,
        edge_threshold=args.edge_threshold,
        invert=args.invert,
    )

    try:
        ascii_art = generator.generate_from_image(args.image_path, ansi=args.color)

        if args.html:
            html = generator.generate_html(
                args.image_path,
                preserve_color=True,
                font_size=args.font_size,
            )
            generator.save_html_to_file(html, args.html)
            print(f"HTML output saved to {args.html}")

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