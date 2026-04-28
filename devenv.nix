{
  pkgs,
  ...
}:

{
  packages = [
    pkgs.git
    pkgs.tectonic
    pkgs.tex-fmt
  ];

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
    shellcheck.enable = true;
    statix.enable = true;
    trim-trailing-whitespace.enable = true;
  };
}
