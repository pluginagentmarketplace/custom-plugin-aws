#!/usr/bin/env python3
"""Generate responsive media queries."""

BREAKPOINTS = {
    "sm": 640, "md": 768, "lg": 1024, "xl": 1280, "2xl": 1536
}

def generate_media_queries(properties: dict, breakpoint: str) -> str:
    """Generate CSS media query."""
    if breakpoint not in BREAKPOINTS:
        return ""

    css = f"@media (min-width: {BREAKPOINTS[breakpoint]}px) {{\n"
    for selector, styles in properties.items():
        css += f"  {selector} {{\n"
        for prop, value in styles.items():
            css += f"    {prop}: {value};\n"
        css += "  }\n"
    css += "}"
    return css

if __name__ == "__main__":
    props = {".container": {"max-width": "1200px", "padding": "2rem"}}
    print(generate_media_queries(props, "lg"))
