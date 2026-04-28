# Awesome CV [![Example](https://img.shields.io/badge/example-pdf-green.svg)](https://raw.githubusercontent.com/posquit0/Awesome-CV/master/examples/resume.pdf)


[**Awesome CV**](https://github.com/posquit0/Awesome-CV) is LaTeX template for a **CV(Curriculum Vitae)**, **Résumé** or **Cover Letter** inspired by [Fancy CV](https://www.sharelatex.com/templates/cv-or-resume/fancy-cv). It is easy to customize your own template, especially since it is really written by a clean, semantic markup.


## Table of contents

* [Preview](#preview)
* [Quick Start](#quick-start)
* [How to Use](#how-to-use)
* [Credit](#credit)
* [Contact](#contact)


## <a name="preview"></a>Preview

#### Résumé

You can see [PDF](https://raw.githubusercontent.com/posquit0/Awesome-CV/master/examples/resume.pdf)

![Résumé(Page 1)](https://raw.githubusercontent.com/posquit0/Awesome-CV/master/examples/resume-0.png)
![Résumé(Page 2)](https://raw.githubusercontent.com/posquit0/Awesome-CV/master/examples/resume-1.png)

#### Cover Letter

You can see [PDF](https://raw.githubusercontent.com/posquit0/Awesome-CV/master/examples/coverletter.pdf)

![Cover Letter(Traditional)](https://raw.githubusercontent.com/posquit0/Awesome-CV/master/examples/coverletter-0.png)
![Cover Letter(Awesome)](https://raw.githubusercontent.com/posquit0/Awesome-CV/master/examples/coverletter-1.png)


## <a name="quick-start">Quick Start

* [**Edit Résumé on OverLeaf.com**](https://www.overleaf.com/latex/templates/awesome-cv/tvmzpvdjfqxp)
* [**Edit Résumé on ShareLaTeX.com**](https://www.sharelatex.com/templates/cv-or-resume/awesome-cv)
* [**Edit Cover Letter on OverLeaf.com**](https://www.overleaf.com/latex/templates/awesome-cv-cover-letter/pfzzjspkthbk)
* [**Edit Cover Letter on ShareLaTeX.com**](https://www.sharelatex.com/templates/cover-letters/awesome-cv-cover-letter)

**_Note:_ Above services do not guarantee up-to-date source code of Awesome CV**


## <a name="how-to-use">How to Use

#### Requirements

This repo uses [devenv](https://devenv.sh) to set up the local development environment, which provides [Tectonic](https://tectonic-typesetting.github.io) and `tex-fmt`. With [devenv](https://devenv.sh) and [direnv](https://direnv.net) installed, run `direnv allow` once in the repo root to activate the shell.

Alternatively, a full TeX distribution (e.g. TeX Live) can be used — see [installation options](http://tex.stackexchange.com/q/55437).

#### Usage

Using `tectonic`:

```bash
tectonic resume.tex       # produces resume.pdf (auto-fetches required packages)
tectonic cover_letter.tex # produces cover_letter.pdf
```

With a full TeX distribution:

```bash
xelatex resume.tex        # produces resume.pdf
xelatex cover_letter.tex  # produces cover_letter.pdf
```

`tex-fmt` runs automatically as a pre-commit git hook to format `.tex` files.


## <a name="credit">Credit

[**LaTeX**](http://www.latex-project.org) is a fantastic typesetting program that a lot of people use these days, especially the math and computer science people in academia.

[**LaTeX FontAwesome**](https://github.com/furl/latex-fontawesome) is bindings for FontAwesome icons to be used in XeLaTeX.

[**Roboto**](https://github.com/google/roboto) is the default font on Android and ChromeOS, and the recommended font for Google’s visual language, Material Design.

[**Source Sans Pro**](https://github.com/adobe-fonts/source-sans-pro) is a set of OpenType fonts that have been designed to work well in user interface (UI) environments.


## <a name="contact">Contact

You are free to take my `.tex` file and modify it to create your own resume. Please don't use my resume for anything else without my permission, though!

If you have any questions, feel free to join me at [`#posquit0` on Freenode](irc://irc.freenode.net/posquit0) and ask away. Click [here](https://kiwiirc.com/client/irc.freenode.net/posquit0) to connect.

Good luck!
