from bs4 import BeautifulSoup
from svgpathtools import parse_path


def transform_svg_path(svg_path_data):
    path = parse_path(svg_path_data)

    xmin, xmax, ymin, ymax = path.bbox()
    w, h = xmax - xmin, ymax - ymin

    path = path.translated(-xmin - ymin * 1j).scaled(1, -1).translated(h * 1j)

    return (w, h), path.d()


def extract_glyphs(svg_str: str):
    tree = BeautifulSoup(svg_str, "html.parser")

    glyphs = [
        {
            "name": glyph.attrs["glyph-name"],
            "path": glyph.attrs["d"].replace("\n", " "),
            "unicode": glyph.attrs["unicode"],
        }
        for glyph in tree.find_all("glyph")
        if "d" in glyph.attrs and "unicode" in glyph.attrs
    ]

    return glyphs


def extract_icons_from_svg_font(filename: str):
    with open(filename) as html:
        svg_str = html.read()

    glyphs = extract_glyphs(svg_str)

    template = """
    <svg data-name="{name}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
        <path d="{path}" />
    </svg>
    """

    for glyph in glyphs:
        name = glyph["name"]
        (w, h), path = transform_svg_path(glyph["path"])

        with open(f"icons/{name}.svg", "w") as fp:
            fp.write(template.format(name=name, w=w, h=h, path=path))


if __name__ == "__main__":
    filename = "svg/font-regular.svg"

    extract_icons_from_svg_font(filename)
