"""Tests for gen-markdown.py preprocessing pipeline."""

import subprocess
import textwrap

import pytest

from pathlib import Path

from gen_markdown import (
    _skip_whitespace_and_comments,
    clean_tex,
    expand_macros,
    extract_arg,
    extract_header,
    latexpand as gen_latexpand,
    process,
    replace_environments,
    run_pandoc,
    strip_preamble,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def latexpand(path: str) -> str:
    """Run latexpand on a .tex file and return the flattened source."""
    resolved = Path(__file__).parent / path
    result = subprocess.run(
        ["latexpand", str(resolved)],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def pipeline(latex: str) -> str:
    """Run latex through the full gen-markdown pipeline and return markdown."""
    return run_pandoc(process(latex))


# ---------------------------------------------------------------------------
# extract_arg
# ---------------------------------------------------------------------------


def test_extract_arg_simple():
    content, end = extract_arg("{hello} rest", 0)
    assert content == "hello"
    assert end == 7


def test_extract_arg_nested():
    content, end = extract_arg("{a{b}c} rest", 0)
    assert content == "a{b}c"
    assert end == 7


def test_extract_arg_empty():
    content, end = extract_arg("{} rest", 0)
    assert content == ""
    assert end == 2


def test_extract_arg_not_brace():
    content, end = extract_arg("hello", 0)
    assert content is None
    assert end == 0


def test_extract_arg_unterminated():
    content, end = extract_arg("{unterminated", 0)
    assert content == "unterminated"
    assert end == len("{unterminated")


# ---------------------------------------------------------------------------
# _skip_whitespace_and_comments
# ---------------------------------------------------------------------------


def test_skip_whitespace_and_comments_spaces():
    assert _skip_whitespace_and_comments("  abc", 0) == 2


def test_skip_whitespace_and_comments_percent_comment():
    text = "%this is a comment\n{arg}"
    assert _skip_whitespace_and_comments(text, 0) == len("%this is a comment\n")


def test_skip_whitespace_and_comments_mixed():
    text = "  %comment\n  {arg}"
    assert _skip_whitespace_and_comments(text, 0) == len("  %comment\n  ")


# ---------------------------------------------------------------------------
# clean_tex
# ---------------------------------------------------------------------------


def test_clean_tex_rightarrow():
    assert clean_tex(r"Senior $\rightarrow$ Staff") == "Senior → Staff"


def test_clean_tex_dashes():
    assert clean_tex(r"2021 \-- 2025") == "2021 -- 2025"
    assert clean_tex(r"em\---dash") == "em---dash"


def test_clean_tex_cdotp():
    assert clean_tex(r"Boston{\enskip\cdotp\enskip}MA") == "Boston · MA"


def test_clean_tex_textasciitilde():
    # \textasciitilde must stay as-is so pandoc converts it to a rendered tilde ~
    assert clean_tex(r"team of \textasciitilde 11") == r"team of \textasciitilde 11"


def test_clean_tex_dollar():
    # \$ must remain as \$ so pandoc's LaTeX reader can convert it to $
    assert clean_tex(r"\$150M+") == r"\$150M+"


def test_pipeline_escaped_dollar_renders():
    # \$150M+ in LaTeX body must produce $150M+ in the markdown output
    doc = r"\begin{document}\$150M+ revenue.\end{document}"
    result = pipeline(doc)
    assert "$150M+" in result


def test_clean_tex_accent():
    assert clean_tex(r"Saint-Exup\'{e}ry") == "Saint-Exupery"


def test_clean_tex_quotes():
    assert clean_tex(r"``hello world''") == '"hello world"'


def test_clean_tex_unclosed_open_quote():
    # `` without matching '' should still become "
    assert clean_tex(r'``hello world"') == '"hello world"'


def test_clean_tex_double_backslash_becomes_space():
    # \\ (LaTeX line break) in preamble text should become a space
    assert clean_tex(r"rather\\teach") == "rather teach"


# ---------------------------------------------------------------------------
# extract_header
# ---------------------------------------------------------------------------

SAMPLE_PREAMBLE = r"""
\name{William H.}{Weiskopf}{, IV}
\address{91 Westland Avenue{\enskip\cdotp\enskip}Boston, MA}
\mobile{(+1) 720-663-9455}
\email{william@weiskopf.me}
\github{dartagan}
\linkedin{whweiskopf}
\quote{``A quote.'' -Author}
"""


def test_extract_header_name():
    result = extract_header(SAMPLE_PREAMBLE)
    assert "William H. Weiskopf, IV" in result


def test_extract_header_address():
    result = extract_header(SAMPLE_PREAMBLE)
    assert "Boston, MA" in result


def test_extract_header_contact():
    result = extract_header(SAMPLE_PREAMBLE)
    assert "Phone: (+1) 720-663-9455" in result
    assert "Email: william@weiskopf.me" in result
    assert "GitHub: github.com/dartagan" in result
    assert "LinkedIn: linkedin.com/in/whweiskopf" in result


def test_extract_header_no_quote():
    result = extract_header(SAMPLE_PREAMBLE)
    assert "A quote." not in result
    assert ">" not in result


def test_extract_header_name_is_h1():
    result = extract_header(SAMPLE_PREAMBLE)
    assert result.startswith("# William H. Weiskopf, IV")


# ---------------------------------------------------------------------------
# strip_preamble
# ---------------------------------------------------------------------------

SAMPLE_PREAMBLE_FULL = r"""
\documentclass[11pt, letterpaper]{awesome-cv}
\geometry{left=1.4cm, top=.8cm, right=1.4cm}
\fontdir[fonts/]
\colorlet{awesome}{awesome-red}
\setbool{acvSectionColorHighlight}{true}
\renewcommand{\acvHeaderSocialSep}{\quad\textbar\quad}
\name{William H.}{Weiskopf}{, IV}
\address{91 Westland Avenue}
\mobile{(+1) 720-663-9455}
\email{william@weiskopf.me}
\github{dartagan}
\linkedin{whweiskopf}
\quote{``A quote.''}
\begin{document}
\makecvheader
\makecvfooter
  {\today}
  {William H. Weiskopf~~~·~~~Résumé}
  {\thepage}
\end{document}
"""


def test_strip_preamble_removes_documentclass():
    result = strip_preamble(SAMPLE_PREAMBLE_FULL)
    assert r"\documentclass" not in result


def test_strip_preamble_removes_geometry():
    result = strip_preamble(SAMPLE_PREAMBLE_FULL)
    assert r"\geometry" not in result


def test_strip_preamble_removes_personal_info():
    result = strip_preamble(SAMPLE_PREAMBLE_FULL)
    for cmd in (r"\name", r"\address", r"\mobile", r"\email", r"\github", r"\linkedin"):
        assert cmd not in result


def test_strip_preamble_removes_quote():
    result = strip_preamble(SAMPLE_PREAMBLE_FULL)
    assert r"\quote" not in result


def test_strip_preamble_removes_makecvheader():
    result = strip_preamble(SAMPLE_PREAMBLE_FULL)
    assert r"\makecvheader" not in result


def test_strip_preamble_removes_makecvfooter():
    result = strip_preamble(SAMPLE_PREAMBLE_FULL)
    assert r"\makecvfooter" not in result


def test_strip_preamble_removes_quote_with_nested_braces():
    text = r"\quote{\textbf{bold} quote}"
    result = strip_preamble(text)
    assert r"\quote" not in result
    assert r"\textbf" not in result


def test_strip_preamble_preserves_document_env():
    result = strip_preamble(SAMPLE_PREAMBLE_FULL)
    assert r"\begin{document}" in result
    assert r"\end{document}" in result


# ---------------------------------------------------------------------------
# replace_environments
# ---------------------------------------------------------------------------


def test_replace_environments_removes_cventries():
    text = r"\begin{cventries}content\end{cventries}"
    assert r"\begin{cventries}" not in replace_environments(text)
    assert r"\end{cventries}" not in replace_environments(text)
    assert "content" in replace_environments(text)


def test_replace_environments_removes_cvsentence_midline():
    # cvsentence appears inside cventry arg, mid-line
    text = r"\cventry{pos}{title}{loc}{date}{%\begin{cvsentence}Intro text.\end{cvsentence}}"
    result = replace_environments(text)
    assert r"\begin{cvsentence}" not in result
    assert r"\end{cvsentence}" not in result
    assert "Intro text." in result


def test_replace_environments_cvitems_to_itemize():
    text = r"\begin{cvitems}\item foo\end{cvitems}"
    result = replace_environments(text)
    assert r"\begin{itemize}" in result
    assert r"\end{itemize}" in result
    assert r"\begin{cvitems}" not in result


def test_replace_environments_cventryskills_removed():
    text = textwrap.dedent(r"""
        \begin{cventryskills}
        \item Python
        \item PostgreSQL
        \item Docker
        \end{cventryskills}
    """)
    result = replace_environments(text)
    assert r"\begin{cventryskills}" not in result
    assert "Skills:" not in result
    assert "Python" not in result


# ---------------------------------------------------------------------------
# collect_skills
# ---------------------------------------------------------------------------


def test_collect_skills_single_block():
    from gen_markdown import collect_skills
    text = textwrap.dedent(r"""
        \begin{cventryskills}
        \item Python
        \item Docker
        \end{cventryskills}
    """)
    assert collect_skills(text) == ["Python", "Docker"]


def test_collect_skills_multiple_blocks_dedup():
    from gen_markdown import collect_skills
    text = textwrap.dedent(r"""
        \begin{cventryskills}
        \item Python
        \item Docker
        \end{cventryskills}
        Some other content.
        \begin{cventryskills}
        \item Kubernetes
        \item Python
        \end{cventryskills}
    """)
    assert collect_skills(text) == ["Python", "Docker", "Kubernetes"]


def test_collect_skills_cleans_latex():
    from gen_markdown import collect_skills
    text = textwrap.dedent(r"""
        \begin{cventryskills}
        \item Kubernetes \& Kustomize
        \end{cventryskills}
    """)
    assert collect_skills(text) == ["Kubernetes & Kustomize"]


def test_collect_skills_empty():
    from gen_markdown import collect_skills
    assert collect_skills("no skills here") == []


# ---------------------------------------------------------------------------
# expand_macros
# ---------------------------------------------------------------------------


def test_expand_macros_cvsection():
    assert expand_macros(r"\cvsection{Experience}") == r"\section{Experience}"


def test_expand_macros_cvsubsection():
    assert expand_macros(r"\cvsubsection{Awards}") == r"\subsection{Awards}"


def test_expand_macros_cvline():
    result = expand_macros(r"\cvline{CSM Alumni}{Software Developer}{2010 -- 2014}")
    assert r"\textbf{CSM Alumni}" in result
    assert "Software Developer" in result
    assert "2010 -- 2014" in result


def test_expand_macros_cventry_basic():
    result = expand_macros(r"\cventry{Senior Eng}{Acme}{Boston}{2020 -- 2024}{Desc.}")
    assert r"\subsection{Acme}" in result
    assert r"\textbf{Senior Eng}" in result
    assert "Boston" in result
    assert "2020 -- 2024" in result
    assert "Desc." in result


def test_expand_macros_cventry_empty_args():
    result = expand_macros(r"\cventry{}{SingToWho.site}{}{June 2020}{A cool project.}")
    assert r"\subsection{SingToWho.site}" in result
    assert "A cool project." in result


def test_expand_macros_cventry_percent_suffix():
    """\\cventry% (trailing %) is used in the actual resume files."""
    result = expand_macros("\\cventry%\n{Senior Eng}{Acme}{Boston}{2020}{Desc.}")
    assert r"\subsection{Acme}" in result
    assert r"\textbf{Senior Eng}" in result


def test_expand_macros_cventry_multiline_fifth_arg():
    src = textwrap.dedent(r"""
        \cventry{Engineer}{Acme}{City}{2020 -- 2024}{%
          Intro text.
          \begin{itemize}
          \item Bullet one.
          \item Bullet two.
          \end{itemize}
        }
    """).strip()
    result = expand_macros(src)
    assert r"\subsection{Acme}" in result
    assert r"\textbf{Engineer}" in result
    assert "Intro text." in result
    assert r"\begin{itemize}" in result


def test_expand_macros_cventry_position_on_own_line():
    result = expand_macros(r"\cventry{Senior Eng}{Acme}{Boston}{2020 -- 2024}{Desc.}")
    lines = result.split("\n")
    position_line = next(l for l in lines if "Senior Eng" in l)
    assert "Boston" not in position_line
    assert "2020" not in position_line


def test_expand_macros_cventry_location_date_on_same_line():
    result = expand_macros(r"\cventry{Senior Eng}{Acme}{Boston}{2020 -- 2024}{Desc.}")
    lines = result.split("\n")
    loc_date_line = next(l for l in lines if "Boston" in l)
    assert "2020" in loc_date_line



def test_pipeline_cventry_position_on_own_line():
    doc = minimal_doc(r"\cventry{Senior Engineer}{Acme Corp}{Boston, MA}{2020 -- 2024}{}")
    result = pipeline(doc)
    lines = result.strip().split("\n")
    pos_line = next(l for l in lines if "**Senior Engineer**" in l)
    assert "Boston" not in pos_line
    assert "2020" not in pos_line


def test_pipeline_cventry_location_date_on_same_line():
    doc = minimal_doc(r"\cventry{Senior Engineer}{Acme Corp}{Boston, MA}{2020 -- 2024}{}")
    result = pipeline(doc)
    lines = result.strip().split("\n")
    loc_line = next(l for l in lines if "Boston, MA" in l)
    assert "2020" in loc_line


def test_pipeline_cventry_no_escaped_pipe():
    doc = minimal_doc(r"\cventry{Senior Engineer}{Acme Corp}{Boston, MA}{2020 -- 2024}{}")
    result = pipeline(doc)
    assert r"\|" not in result
    assert "|" in result


def test_expand_macros_cvhonor_empty_args():
    result = expand_macros(r"\cvhonor{Award}{}{}{2020}")
    assert ", --" not in result
    assert r"\textbf{Award}" in result
    assert "2020" in result


def test_expand_macros_no_newcommand_in_output():
    """expand_macros replaces calls; no \\newcommand definitions should be present."""
    result = expand_macros(r"\cvsection{X}\cventry{a}{b}{c}{d}{e}")
    assert r"\newcommand" not in result


def test_expand_macros_leaves_standard_latex_unchanged():
    text = r"\section{Existing}\textbf{bold}\begin{itemize}\item x\end{itemize}"
    assert expand_macros(text) == text


def test_expand_macros_preserves_whitespace_after_macro():
    """Content and blank lines after a macro must not be consumed by arg-skipping."""
    result = expand_macros("\\cvsection{A}\n\ntext after\n")
    assert result.startswith("\\section{A}")
    assert "text after" in result
    # The blank line between the section and the following text must be preserved
    assert "\n\n" in result


# ---------------------------------------------------------------------------
# Integration: pipeline through pandoc
# ---------------------------------------------------------------------------


def minimal_doc(body: str) -> str:
    return (
        r"\documentclass{article}"
        + "\n"
        + r"\begin{document}"
        + "\n"
        + body
        + "\n"
        + r"\end{document}"
    )


def test_pipeline_cvsection_becomes_h1():
    doc = minimal_doc(r"\cvsection{Experience}")
    result = pipeline(doc)
    assert "# Experience" in result


def test_pipeline_cventry_org_becomes_h2():
    doc = minimal_doc(
        r"\cventry{Senior Engineer}{Acme Corp}{Boston, MA}{2020 -- 2024}{}"
    )
    result = pipeline(doc)
    assert "## Acme Corp" in result


def test_pipeline_cventry_position_is_bold():
    doc = minimal_doc(
        r"\cventry{Senior Engineer}{Acme Corp}{Boston, MA}{2020 -- 2024}{}"
    )
    result = pipeline(doc)
    assert "**Senior Engineer**" in result


def test_pipeline_cventry_location_and_date_present():
    doc = minimal_doc(
        r"\cventry{Senior Engineer}{Acme Corp}{Boston, MA}{2020 -- 2024}{}"
    )
    result = pipeline(doc)
    assert "Boston, MA" in result
    assert "2020" in result
    assert "2024" in result


def test_pipeline_cventry_empty_args_ok():
    # projects.tex has empty position and location args
    doc = minimal_doc(r"\cventry{}{SingToWho.site}{}{June 2020}{A cool project.}")
    result = pipeline(doc)
    assert "## SingToWho.site" in result
    assert "A cool project." in result


def test_pipeline_cventry_multiline_fifth_arg():
    """\\cventry with a multi-line 5th arg containing an itemize (as in experience.tex)."""
    doc = minimal_doc(
        textwrap.dedent(r"""
            \cventry{Senior Engineer}{Acme Corp}{Boston, MA}{2020 -- 2024}{%
              Intro sentence.
              \begin{cvitems}
              \item {First bullet with some text.} \\
                Continuation text after a line break.
              \item Second bullet.
              \end{cvitems}
            }
        """)
    )
    result = pipeline(doc)
    assert "## Acme Corp" in result
    assert "First bullet" in result
    assert "Second bullet" in result


def test_pipeline_cvitems_become_bullets():
    doc = minimal_doc(
        textwrap.dedent(r"""
            \begin{cvitems}
            \item First bullet
            \item Second bullet
            \end{cvitems}
        """)
    )
    result = pipeline(doc)
    assert "- First bullet" in result
    assert "- Second bullet" in result


def test_pipeline_item_with_double_backslash_continuation():
    """\\item {text} \\\\ continuation is used in Oliver Wyman section."""
    doc = minimal_doc(
        textwrap.dedent(r"""
            \begin{cvitems}
            \item {First part.} \\
              Continuation text.
            \item Second item.
            \end{cvitems}
        """)
    )
    result = pipeline(doc)
    assert "First part" in result
    assert "Second item" in result


def test_pipeline_cventryskills_removed_from_body():
    doc = minimal_doc(
        textwrap.dedent(r"""
            \begin{cventryskills}
            \item Python
            \item Docker
            \end{cventryskills}
        """)
    )
    result = pipeline(doc)
    assert "*Skills:" not in result
    assert "cventryskills" not in result


def test_pipeline_cvline():
    doc = minimal_doc(r"\cvline{CSM Alumni}{Software Developer}{2010 -- 2014}")
    result = pipeline(doc)
    assert "**CSM Alumni**" in result
    assert "Software Developer" in result
    assert "2010" in result


def test_pipeline_textasciitilde_renders_tilde():
    doc = minimal_doc(r"\cventry{team of \textasciitilde 11}{Acme}{}{2020}{}")
    result = pipeline(doc)
    assert "~" in result


def test_pipeline_cventry_empty_fields_no_bare_pipes():
    # Projects use cventry with empty position and location; should not produce "| |" or "\| \|"
    doc = minimal_doc(r"\cventry{}{\href{https://singtowho.site}{SingToWho.site}}{}{June 2020}{Desc.}")
    result = pipeline(doc)
    assert r"\| \|" not in result
    assert "| |" not in result
    assert "singtowho.site" in result
    assert "June 2020" in result


def test_pipeline_href_preserved():
    doc = minimal_doc(r"\cventry{}{\href{https://singtowho.site}{SingToWho.site}}{}{June 2020}{}")
    result = pipeline(doc)
    assert "singtowho.site" in result


def test_pipeline_rightarrow_cleaned():
    doc = minimal_doc(
        r"\cventry{Senior $\rightarrow$ Staff}{Acme}{}{2020 -- 2024}{}"
    )
    result = pipeline(doc)
    assert "→" in result
    assert r"$\rightarrow$" not in result


def test_pipeline_no_leftover_latex():
    """Spot-check that common TeX commands don't appear raw in output."""
    doc = minimal_doc(
        textwrap.dedent(r"""
            \cvsection{Experience}
            \cventry{Senior Engineer}{Acme Corp}{Boston, MA}{2020 -- 2024}{
              \begin{cvitems}
              \item Did things.
              \end{cvitems}
            }
            \begin{cventryskills}
            \item Python
            \end{cventryskills}
        """)
    )
    result = pipeline(doc)
    for cmd in (r"\cvsection", r"\cventry", r"\begin{cvitems}", r"\begin{cventryskills}"):
        assert cmd not in result


# ---------------------------------------------------------------------------
# process() integration: do the pipeline stages compose correctly?
# ---------------------------------------------------------------------------

MINIMAL_AWESOME_CV_DOC = r"""
\documentclass[11pt, letterpaper]{awesome-cv}
\geometry{left=1.4cm}
\colorlet{awesome}{awesome-red}
\name{Jane}{Doe}{}
\email{jane@doe.com}
\begin{document}
\makecvheader
\cvsection{Experience}
\begin{cventries}
\cventry{Engineer}{Acme Corp}{City}{2020 -- 2024}{%
\begin{cvitems}
\item Did stuff.
\end{cvitems}
}
\begin{cventryskills}
\item Python
\end{cventryskills}
\end{cventries}
\end{document}
"""


def test_process_no_raw_markdown_block():
    """process() must not emit ```{=markdown} blocks -- pandoc's LaTeX reader rejects them."""
    result = process(MINIMAL_AWESOME_CV_DOC)
    assert "{=markdown}" not in result


def test_process_expands_cvsection():
    """process() should expand \\cvsection to \\section (no custom macros left for pandoc)."""
    result = process(MINIMAL_AWESOME_CV_DOC)
    assert r"\cvsection" not in result
    assert r"\section{Experience}" in result


def test_process_expands_cventry():
    """process() should expand \\cventry to standard LaTeX subsection + bold."""
    result = process(MINIMAL_AWESOME_CV_DOC)
    assert r"\cventry" not in result
    assert r"\subsection{Acme Corp}" in result


def test_process_documentclass_stripped():
    """\\documentclass must not reach pandoc -- it causes pandoc to load the .cls file."""
    result = process(MINIMAL_AWESOME_CV_DOC)
    assert r"\documentclass" not in result


# ---------------------------------------------------------------------------
# Integration: full resume round-trip
# ---------------------------------------------------------------------------


def full_pipeline(tex_source: str) -> str:
    """Mimic what main() does: header + skills section + pandoc body."""
    from gen_markdown import collect_skills, clean_tex
    header = extract_header(tex_source)
    skills = collect_skills(clean_tex(tex_source))
    body = run_pandoc(process(tex_source))
    parts = [header, ""]
    if skills:
        parts += ["# Skills", "", " · ".join(skills), ""]
    parts.append(body)
    return "\n".join(parts)


def test_full_resume_sections_present():
    md = full_pipeline(latexpand("resume.tex"))
    assert "# Experience" in md
    assert "# Education" in md
    assert "# Projects" in md


def test_full_resume_header_present():
    md = full_pipeline(latexpand("resume.tex"))
    assert "# William H. Weiskopf, IV" in md
    assert "william@weiskopf.me" in md


def test_full_resume_header_not_escaped():
    # The markdown header must use literal # and > not pandoc-escaped \# and \>
    md = full_pipeline(latexpand("resume.tex"))
    assert r"\#" not in md
    assert r"\>" not in md


def test_full_resume_ginkgo_present():
    md = full_pipeline(latexpand("resume.tex"))
    assert "Ginkgo Bioworks" in md


def test_full_resume_no_cventryskills_env():
    md = full_pipeline(latexpand("resume.tex"))
    assert "cventryskills" not in md


def test_full_resume_has_skills_section():
    md = full_pipeline(latexpand("resume.tex"))
    assert "# Skills" in md


def test_full_resume_skills_before_experience():
    md = full_pipeline(latexpand("resume.tex"))
    assert md.index("# Skills") < md.index("# Experience")


def test_full_resume_no_inline_skills():
    md = full_pipeline(latexpand("resume.tex"))
    assert "*Skills:" not in md


# ---------------------------------------------------------------------------
# main() CLI: --dump-latex flag
# ---------------------------------------------------------------------------


def run_main(tex_source: str, args: list[str] | None = None) -> str:
    """Run gen_markdown.py as a subprocess and return stdout."""
    result = subprocess.run(
        ["python3", "gen_markdown.py"] + (args or []),
        input=tex_source,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def test_dump_latex_outputs_preprocessed_latex():
    tex = r"\begin{document}\cvsection{Exp}\end{document}"
    out = run_main(tex, ["--dump-latex"])
    assert r"\section{Exp}" in out
    assert r"\cvsection" not in out


def test_dump_latex_output_is_latex_not_markdown():
    tex = r"\begin{document}\cvsection{Exp}\end{document}"
    out = run_main(tex, ["--dump-latex"])
    assert "# Exp" not in out  # no markdown headers


def test_dump_latex_includes_documentclass_wrapper():
    tex = r"\begin{document}\cvsection{Exp}\end{document}"
    out = run_main(tex, ["--dump-latex"])
    assert r"\documentclass{article}" in out
    assert r"\begin{document}" in out
    assert r"\end{document}" in out


def test_default_mode_still_produces_markdown():
    tex = r"\begin{document}\cvsection{Exp}\end{document}"
    out = run_main(tex)
    assert "# Exp" in out


def test_main_with_file_arg_produces_markdown():
    resume_path = str(Path(__file__).parent / "resume.tex")
    result = subprocess.run(
        ["python3", "gen_markdown.py", resume_path],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "# Experience" in result.stdout
    assert "# William H. Weiskopf, IV" in result.stdout


def test_main_with_file_arg_dump_latex():
    resume_path = str(Path(__file__).parent / "resume.tex")
    result = subprocess.run(
        ["python3", "gen_markdown.py", "--dump-latex", resume_path],
        capture_output=True,
        text=True,
        check=True,
    )
    assert r"\documentclass{article}" in result.stdout
    assert r"\section{Experience}" in result.stdout


# ---------------------------------------------------------------------------
# latexpand()
# ---------------------------------------------------------------------------


def test_gen_latexpand_flattens_inputs():
    resume_path = str(Path(__file__).parent / "resume.tex")
    result = gen_latexpand(resume_path)
    assert r"\cventry" in result
    assert r"\input{" not in result
