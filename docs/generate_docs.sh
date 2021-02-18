cd "$(dirname "$0")"
rm -rf _build
rm -rf source
sphinx-apidoc -f -o source ../pysniff ../test* ../temp* ../untitled* ../__pycache__ ../examples
make html