with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "mantid-exercises";
  src = ./.;
  buildInputs = [bear boost ccls clang cmake cppcheck mesa qt5.full];
}
