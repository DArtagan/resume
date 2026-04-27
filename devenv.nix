{ pkgs, lib, config, inputs, ... }:

{
  packages = [
    pkgs.git
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

  git-hooks.hooks.latexindent.enable = true;
}
