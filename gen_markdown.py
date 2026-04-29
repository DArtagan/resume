import re
import subprocess
import sys


def extract_arg(text, pos):
    """Extract a single {braced} argument starting at pos. Returns (content, end_pos)."""
    if pos >= len(text) or text[pos] != "{":
        return None, pos
    depth = 0
    start = pos + 1
    i = pos
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i], i + 1
        i += 1
    return text[start:], len(text)


def _skip_whitespace_and_comments(text, pos):
    """Skip spaces, newlines, and % comments."""
    while pos < len(text):
        if text[pos] in " \t\n":
            pos += 1
        elif text[pos] == "%":
            while pos < len(text) and text[pos] != "\n":
                pos += 1
        else:
            break
    return pos


def _expand_macro(text, macro_name, n_args, formatter):
    """Replace \\macro_name{arg1}...{argN} with formatter([arg1,...,argN])."""
    cmd = "\\" + macro_name
    result = []
    i = 0
    while i < len(text):
        if text[i:].startswith(cmd):
            end_of_name = i + len(cmd)
            # Ensure it's not part of a longer command name (e.g. \cvsection vs \cvsentence)
            if end_of_name < len(text) and text[end_of_name].isalpha():
                result.append(text[i])
                i += 1
                continue
            pos = _skip_whitespace_and_comments(text, end_of_name)
            args = []
            for arg_idx in range(n_args):
                if pos < len(text) and text[pos] == "{":
                    arg, pos = extract_arg(text, pos)
                    args.append(arg)
                    # Skip whitespace/comments between args but not after the last one,
                    # so content following the macro call is not silently consumed.
                    if arg_idx < n_args - 1:
                        pos = _skip_whitespace_and_comments(text, pos)
                else:
                    break
            if len(args) == n_args:
                result.append(formatter(args))
                i = pos
            else:
                result.append(text[i])
                i += 1
        else:
            result.append(text[i])
            i += 1
    return "".join(result)


def expand_macros(text):
    """Expand awesome-cv macros to standard LaTeX in-place."""
    text = _expand_macro(text, "cvsection", 1,
        lambda a: f"\\section{{{a[0]}}}")
    text = _expand_macro(text, "cvsubsection", 1,
        lambda a: f"\\subsection{{{a[0]}}}")
    def _cventry(a):
        position = a[0].strip()
        location = a[2].strip()
        date = a[3].strip()
        lines = [f"\\subsection{{{a[1]}}}"]
        if position:
            suffix = r"\\" if any(p for p in (location, date) if p) else ""
            lines.append(f"\\textbf{{{position}}}{suffix}")
        loc_date = [p for p in (location, date) if p]
        if loc_date:
            lines.append(" | ".join(loc_date))
        lines.append("")
        lines.append(a[4])
        return "\n".join(lines)
    text = _expand_macro(text, "cventry", 5, _cventry)
    text = _expand_macro(text, "cvline", 3,
        lambda a: f"\\textbf{{{a[0]}}} -- {a[1]} | {a[2]}")
    def _cvhonor(a):
        parts = [p for p in [a[0], a[1], a[2]] if p.strip()]
        line = ", ".join(f"\\textbf{{{parts[0]}}}" if i == 0 else parts[i]
                         for i, _ in enumerate(parts)) if parts else ""
        if a[3].strip():
            line += f" ({a[3]})" if line else a[3]
        return line
    text = _expand_macro(text, "cvhonor", 4, _cvhonor)
    text = _expand_macro(text, "cvskill", 2,
        lambda a: f"\\textbf{{{a[0]}}}: {a[1]}")
    return text


def clean_tex(text):
    """Clean TeX inline commands to plain text."""
    text = re.sub(r"\$\\rightarrow\$", "→", text)
    text = text.replace(r"\--", "--")
    text = text.replace(r"\---", "---")
    text = re.sub(r"\{\\enskip\\cdotp\\enskip\}", " · ", text)
    # Leave \textasciitilde as-is so pandoc converts it to a rendered tilde character
    text = text.replace(r"\enskip", " ")
    text = text.replace(r"\enspace", " ")
    text = text.replace(r"\quad", " ")
    text = re.sub(r"\\'\{(\w)\}", r"\1", text)  # \'{e} -> e
    text = text.replace(r"\&", "&")
    # Leave \$ as-is so pandoc's LaTeX reader converts it to a literal $
    text = re.sub(r"``(.*?)''", r'"\1"', text, flags=re.DOTALL)
    text = text.replace("``", '"')  # unmatched open-quote
    text = text.replace("\\\\", " ")  # \\ line-break → space
    return text


def extract_header(text):
    """Extract personal info from the preamble and return markdown header string."""
    fields = {}

    m = re.search(r"\\name\s*\{", text)
    if m:
        pos = m.end() - 1
        first, pos = extract_arg(text, pos)
        last, pos = extract_arg(text, pos)
        suffix, pos = extract_arg(text, pos)
        if first is not None and last is not None:
            name = f"{first} {last}"
            if suffix:
                name += suffix
            fields["name"] = name

    for cmd in ("address", "mobile", "email", "github", "linkedin", "homepage"):
        m = re.search(rf"\\{cmd}\s*\{{", text)
        if m:
            content, _ = extract_arg(text, m.end() - 1)
            if content:
                fields[cmd] = content

    header_lines = []
    if "name" in fields:
        header_lines.append(f"# {clean_tex(fields['name'])}")
        header_lines.append("")

    if "address" in fields:
        header_lines.append(clean_tex(fields["address"]))
        header_lines.append("")

    contact = []
    if "mobile" in fields:
        contact.append(f"Phone: {fields['mobile']}")
    if "email" in fields:
        contact.append(f"Email: {fields['email']}")
    if "github" in fields:
        contact.append(f"GitHub: github.com/{fields['github']}")
    if "linkedin" in fields:
        contact.append(f"LinkedIn: linkedin.com/in/{fields['linkedin']}")
    if "homepage" in fields:
        contact.append(fields["homepage"])
    if contact:
        header_lines.append(" | ".join(contact))
        header_lines.append("")

    return "\n".join(header_lines)


def strip_preamble(text):
    """Remove preamble commands and personal info that pandoc can't handle."""
    text = re.sub(r"\\documentclass\[.*?\]\{.*?\}", "", text)
    text = re.sub(r"\\geometry\{.*?\}", "", text)
    text = re.sub(r"\\fontdir\[.*?\]", "", text)
    text = re.sub(r"\\colorlet\{.*?\}\{.*?\}", "", text)
    text = re.sub(r"\\setbool\{.*?\}\{.*?\}", "", text)
    text = re.sub(r"\\renewcommand\{\\acvHeaderSocialSep\}\{.*?\}", "", text)
    text = re.sub(r"\\makecvheader", "", text)
    text = re.sub(
        r"\\makecvfooter\s*\{.*?\}\s*\{.*?\}\s*\{.*?\}", "", text, flags=re.DOTALL
    )

    # Remove personal info commands (line-based since they're on their own lines)
    for cmd in (
        "name",
        "address",
        "mobile",
        "email",
        "github",
        "linkedin",
        "homepage",
        "position",
    ):
        text = re.sub(rf"^\\{cmd}\b.*$", "", text, flags=re.MULTILINE)

    # quote may contain nested braces, so use brace-balanced extraction
    while True:
        m = re.search(r"\\quote\s*\{", text)
        if not m:
            break
        _, end = extract_arg(text, m.end() - 1)
        text = text[:m.start()] + text[end:]

    return text


def replace_environments(text):
    """Replace custom awesome-cv environments with standard LaTeX or markdown."""
    # Remove wrapper-only environments
    for env in ("cventries", "cvsentence", "cvhonors", "cvskills", "cvparagraph"):
        text = re.sub(rf"\\begin\{{{env}\}}", "", text)
        text = re.sub(rf"\\end\{{{env}\}}", "", text)

    # cvitems -> itemize
    text = re.sub(r"\\begin\{cvitems\}", r"\\begin{itemize}", text)
    text = re.sub(r"\\end\{cvitems\}", r"\\end{itemize}", text)

    # Remove cventryskills blocks entirely (skills are consolidated separately)
    text = re.sub(
        r"\\begin\{cventryskills\}.*?\\end\{cventryskills\}",
        "",
        text,
        flags=re.DOTALL,
    )

    return text


def collect_skills(text):
    """Extract all skills from cventryskills blocks, deduplicated in first-appearance order."""
    seen = {}
    for block in re.findall(
        r"\\begin\{cventryskills\}(.*?)\\end\{cventryskills\}", text, re.DOTALL
    ):
        items = re.findall(r"\\item\s+(.*?)(?=\\item|\Z)", block, re.DOTALL)
        for raw in items:
            skill = clean_tex(raw.strip())
            if skill and skill not in seen:
                seen[skill] = True
    return list(seen.keys())


def process(text):
    """Preprocess LaTeX for pandoc. Does not include the header -- call extract_header() separately."""
    text = clean_tex(text)
    text = strip_preamble(text)
    text = replace_environments(text)
    text = expand_macros(text)
    return text


def run_pandoc(latex_text):
    """Convert preprocessed LaTeX to markdown, then unescape pandoc-escaped pipes."""
    result = subprocess.run(
        ["pandoc", "-f", "latex", "-t", "markdown"],
        input=latex_text,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.replace(r"\|", "|")


def latexpand(path):
    """Run latexpand on a .tex file and return the flattened source."""
    result = subprocess.run(
        ["latexpand", path],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def main():
    args = [a for a in sys.argv[1:] if a != "--dump-latex"]
    dump_latex = "--dump-latex" in sys.argv
    if args:
        text = latexpand(args[0])
    else:
        text = sys.stdin.read()
    processed = process(text)
    if dump_latex:
        print(r"\documentclass{article}")
        print(r"\begin{document}")
        print(processed)
        print(r"\end{document}")
        return
    header = extract_header(text)
    skills = collect_skills(clean_tex(text))
    md_body = run_pandoc(processed)
    if header:
        print(header)
        print()
    if skills:
        print("# Skills")
        print()
        print(" · ".join(skills))
        print()
    print(md_body, end="")


if __name__ == "__main__":
    main()
