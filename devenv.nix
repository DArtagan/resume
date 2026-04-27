{ pkgs, lib, config, inputs, ... }:

{
  packages = [
    pkgs.git
    pkgs.tex-fmt
  ];

  languages.texlive = {
    enable = true;
    lsp.enable = true;
    packages = [
      "enumitem"
      "ifmtarg"
      "xifthen"
    ];
  };

  git-hooks.hooks.tex-fmt = {
    enable = true;
    name = "tex-fmt --nowrap";
    entry = "tex-fmt";
    types = [ "tex" ];
    language = "system";
  };
}
