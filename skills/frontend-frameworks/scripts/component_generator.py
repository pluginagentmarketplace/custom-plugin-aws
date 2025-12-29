#!/usr/bin/env python3
"""React component generator."""
from pathlib import Path

def generate_component(name: str, path: str = "src/components"):
    dir_path = Path(path) / name
    dir_path.mkdir(parents=True, exist_ok=True)

    (dir_path / f"{name}.tsx").write_text(f'''
interface {name}Props {{
  className?: string;
}}

export function {name}({{ className }}: {name}Props) {{
  return <div className={{className}}>{name}</div>;
}}
''')

    (dir_path / f"{name}.test.tsx").write_text(f'''
import {{ render, screen }} from "@testing-library/react";
import {{ {name} }} from "./{name}";

test("renders {name}", () => {{
  render(<{name} />);
  expect(screen.getByText("{name}")).toBeInTheDocument();
}});
''')

    (dir_path / "index.ts").write_text(f'export {{ {name} }} from "./{name}";')
    print(f"Created: {dir_path}")

if __name__ == "__main__":
    import sys
    generate_component(sys.argv[1] if len(sys.argv) > 1 else "Button")
