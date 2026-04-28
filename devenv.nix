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
      name = "tex-fmt --nowrap";
      entry = "tex-fmt";
      types = [ "tex" ];
      language = "system";
    };
    end-of-file-fixer.enable = true;
    deadnix.enable = true;
    flake-checker.enable = true;
    nixfmt.enable = true;
    statix.enable = true;
    trim-trailing-whitespace.enable = true;
  };
}
