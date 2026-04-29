{
  pkgs,
  ...
}:

{
  packages = [
    pkgs.git
    pkgs.pandoc
    pkgs.tectonic
    pkgs.tex-fmt
    pkgs.texlivePackages.latexpand
  ];

  languages.python = {
    enable = true;
    uv = {
      enable = true;
      sync.enable = true;
    };
    lsp = {
      enable = true;
      package = pkgs.ty;
    };
  };

  git-hooks.hooks = {
    tex-fmt = {
      enable = true;
      name = "tex-fmt";
      entry = "tex-fmt --nowrap";
      types = [ "tex" ];
      language = "system";
    };
    end-of-file-fixer.enable = true;
    deadnix.enable = true;
    flake-checker.enable = true;
    nixfmt.enable = true;
    statix.enable = true;
    trim-trailing-whitespace.enable = true;
    resumes = {
      enable = true;
      name = "generate resumes";
      entry = "devenv tasks run resume";
      types = [ "tex" ];
      language = "system";
      pass_filenames = false;
    };
  };

  #processes = {
  #  build-resume-markdown = {
  #    exec = "python gen_markdown.py resume.tex > resume.md";
  #    watch = {
  #      paths = [ ./. ./resume ];
  #      extensions = [ "tex" ];
  #    };
  #  };
  #  build-resume-pdf = {
  #    exec = "tectonic resume.tex";
  #    watch = {
  #      paths = [ ./. ./resume ];
  #      extensions = [ "tex" ];
  #    };
  #  };
  #};

  tasks = {
    "resume:markdown" = {
      exec = "python gen_markdown.py resume.tex > resume.md";
    };
    "resume:pdf" = {
      exec = "SOURCE_DATE_EPOCH=${toString builtins.currentTime} tectonic resume.tex";
    };
  };
}
