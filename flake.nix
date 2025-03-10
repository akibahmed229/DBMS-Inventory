{
  description = "Dev Environment for Weather Forecasting";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {nixpkgs, ...}: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
      config = {allowUnfree = true;};
    };
  in {
    devShells.${system}.default = pkgs.mkShell {
      name = "weather-forecasting";

      # Add packages to the shell environment
      packages =
        (with pkgs; [
          python312
        ])
        ++ (with pkgs.python312Packages; [
          virtualenv
          pip
          requests
          tkinter
          pymysql
        ]);

      # Add environment variables to the shell environment
      env = {
        LD_LIBRARY_PATH =
          pkgs.lib.makeLibraryPath [
          ];
      };

      # Add shell hooks to the shell environment to be executed on entering the shell
      shellHook = ''
        echo "Entering devShell for ${system}";

        # Persistent virtual environment setup
        if [[ ! -d ./venv ]]; then
          python -m venv ./venv
        fi
        source ./venv/bin/activate

        # workaround for vscode's to find the venv
        venv="$(cd $(dirname $(which python)); cd ..; pwd)"
        ln -Tsf "$venv" .venv

        zsh
      '';
    };
  };
}
