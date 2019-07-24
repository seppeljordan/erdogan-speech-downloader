with import <nixpkgs> {};
let

f =
  { buildPythonPackage
  , beautifulsoup4
  , requests
  , black
  }:
  buildPythonPackage rec {
    pname = "speech-crawler";
    version = "1.0";
    src = ./.;
    propagatedBuildInputs = [
      beautifulsoup4
      requests
    ];
    checkInputs = [ black ];
  };

in

python3.pkgs.callPackage f {}
