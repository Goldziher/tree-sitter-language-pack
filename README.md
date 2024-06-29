# Tree Sitter Language Pack

This package bundles a comprehensive collection of [tree-sitter](https://tree-sitter.github.io/tree-sitter/) languages.

It is compatible with [tree-sitter](https://tree-sitter.github.io/tree-sitter/) v0.22.0 and above.

Notes:

- This package is a maintained and updated fork of
  [tree-sitter-languages](https://github.com/grantjenks/py-tree-sitter-languages) by Grant Jenks, and it
  incorporates code contributed by ObserverOfTime (see
  this [PR](https://github.com/grantjenks/py-tree-sitter-languages/pull/65)).
- This package is MIT licensed and the original package of which this is a fork has an Apache 2.0 License. Both licenses
  are available in the LICENSE file.
- All languages bundled by this package are licensed under permissive open-source licenses (MIT or Apache 2.0) - no GPL
  licensed languages are included.

## Installation

```bash
pip install tree-sitter-language-pack
```

## Usage

This library exposes two functions `get_language` and `get_parser`.

```python
from tree_sitter_language_pack import get_language, get_parser

python_lang = get_language('python')  # this is an instance of tree_sitter.Language
python_parser = get_parser('python')  # this is an instance of tree_sitter.Parser
```

See the list of available languages below to get the name of the language you want to use.

## Available Languages:

Each language below is identified by the key used to retrieve it from the `get_language` and `get_parser` functions.

- [agda](https://github.com/tree-sitter/tree-sitter-agda) - MIT License
- [arduino](https://github.com/tree-sitter-grammars/tree-sitter-arduino) - MIT License
- [bash](https://github.com/tree-sitter/tree-sitter-bash) - MIT License
- [bicep](https://github.com/tree-sitter-grammars/tree-sitter-bicep) - MIT License
- [bitbake](https://github.com/tree-sitter-grammars/tree-sitter-bitbake) - MIT License
- [c](https://github.com/tree-sitter/tree-sitter-c) - MIT License
- [cairo](https://github.com/tree-sitter-grammars/tree-sitter-cairo) - MIT License
- [capnp](https://github.com/tree-sitter-grammars/tree-sitter-capnp) - MIT License
- [chatito](https://github.com/tree-sitter-grammars/tree-sitter-chatito) - MIT License
- [clarity](https://github.com/xlittlerag/tree-sitter-clarity) - MIT License
- [commonlisp](https://github.com/tree-sitter-grammars/tree-sitter-commonlisp) - MIT License
- [cpon](https://github.com/tree-sitter-grammars/tree-sitter-cpon) - MIT License
- [cpp](https://github.com/tree-sitter/tree-sitter-cpp) - MIT License
- [csharp](https://github.com/tree-sitter/tree-sitter-c-sharp) - MIT License
- [css](https://github.com/tree-sitter/tree-sitter-css) - MIT License
- [csv](https://github.com/tree-sitter-grammars/tree-sitter-csv) - MIT License
- [cuda](https://github.com/tree-sitter-grammars/tree-sitter-cuda) - MIT License
- [dart](https://github.com/UserNobody14/tree-sitter-dart) - MIT License
- [dot](https://github.com/rydesun/tree-sitter-dot) - MIT License
- [doxygen](https://github.com/tree-sitter-grammars/tree-sitter-doxygen) - MIT License
- [elisp](https://github.com/Wilfred/tree-sitter-elisp) - MIT License
- [elixir](https://github.com/elixir-lang/tree-sitter-elixir) - MIT License
- [elm](https://github.com/elm-tooling/tree-sitter-elm) - MIT License
- [embeddedtemplate](https://github.com/tree-sitter/tree-sitter-embedded-template) - MIT License
- [firrtl](https://github.com/tree-sitter-grammars/tree-sitter-firrtl) - Apache License 2.0
- [fortran](https://github.com/stadelmanma/tree-sitter-fortran) - MIT License
- [func](https://github.com/tree-sitter-grammars/tree-sitter-func) - MIT License
- [gitattributes](https://github.com/tree-sitter-grammars/tree-sitter-gitattributes) - MIT License
- [glsl](https://github.com/tree-sitter-grammars/tree-sitter-glsl) - MIT License
- [gn](https://github.com/tree-sitter-grammars/tree-sitter-gn) - MIT License
- [go](https://github.com/tree-sitter/tree-sitter-go) - MIT License
- [gomod](https://github.com/camdencheek/tree-sitter-go-mod) - MIT License
- [gosum](https://github.com/tree-sitter-grammars/tree-sitter-go-sum) - MIT License
- [gstlaunch](https://github.com/tree-sitter-grammars/tree-sitter-gstlaunch) - MIT License
- [hack](https://github.com/slackhq/tree-sitter-hack) - MIT License
- [hare](https://github.com/tree-sitter-grammars/tree-sitter-hare) - MIT License
- [haskell](https://github.com/tree-sitter/tree-sitter-haskell) - MIT License
- [hcl](https://github.com/tree-sitter-grammars/tree-sitter-hcl) - Apache License 2.0
- [heex](https://github.com/phoenixframework/tree-sitter-heex) - MIT License
- [hlsl](https://github.com/tree-sitter-grammars/tree-sitter-hlsl) - MIT License
- [html](https://github.com/tree-sitter/tree-sitter-html) - MIT License
- [hyperlang](https://github.com/tree-sitter-grammars/tree-sitter-hyperlang) - MIT License
- [hyprlang](https://github.com/tree-sitter-grammars/tree-sitter-hyprlang) MIT License
- [ispc](https://github.com/tree-sitter-grammars/tree-sitter-ispc) - MIT License
- [java](https://github.com/tree-sitter/tree-sitter-java) - MIT License
- [javascript](https://github.com/tree-sitter/tree-sitter-javascript) - MIT License
- [jsdoc](https://github.com/tree-sitter/tree-sitter-jsdoc) - MIT License
- [json](https://github.com/tree-sitter/tree-sitter-json) - MIT License
- [julia](https://github.com/tree-sitter/tree-sitter-julia) - MIT License
- [kconfig](https://github.com/tree-sitter-grammars/tree-sitter-kconfig) - MIT License
- [kdl](https://github.com/tree-sitter-grammars/tree-sitter-kdl) - MIT License
- [kotlin](https://github.com/fwcd/tree-sitter-kotlin) - MIT License
- [linkerscript](https://github.com/tree-sitter-grammars/tree-sitter-linkerscript) - MIT License
- [lua](https://github.com/tree-sitter-grammars/tree-sitter-lua) - MIT License
- [luadoc](https://github.com/tree-sitter-grammars/tree-sitter-luadoc) - MIT License
- [luap](https://github.com/tree-sitter-grammars/tree-sitter-luap) - MIT License
- [luau](https://github.com/tree-sitter-grammars/tree-sitter-luau) - MIT License
- [make](https://github.com/tree-sitter-grammars/tree-sitter-make) - MIT License
- [markdown](https://github.com/tree-sitter-grammars/tree-sitter-markdown) - MIT License
- [matlab](https://github.com/acristoffers/tree-sitter-matlab) - MIT License
- [meson](https://github.com/tree-sitter-grammars/tree-sitter-meson) - MIT License
- [nix](https://github.com/nix-community/tree-sitter-nix) - MIT License
- [nqc](https://github.com/tree-sitter-grammars/tree-sitter-nqc) - MIT License
- [objc](https://github.com/tree-sitter-grammars/tree-sitter-objc) - MIT License
- [ocaml](https://github.com/tree-sitter/tree-sitter-ocaml) - MIT License
- [odin](https://github.com/tree-sitter-grammars/tree-sitter-odin) - MIT License
- [pem](https://github.com/tree-sitter-grammars/tree-sitter-pem) - MIT License
- [perl](https://github.com/tree-sitter-perl/tree-sitter-perl) - Artistic License 2.0
- [php](https://github.com/tree-sitter/tree-sitter-php) - MIT License
- [po](https://github.com/tree-sitter-grammars/tree-sitter-po) - MIT License
- [pony](https://github.com/tree-sitter-grammars/tree-sitter-pony) - MIT License
- [powershell](https://github.com/airbus-cert/tree-sitter-powershell) - MIT License
- [printf](https://github.com/tree-sitter-grammars/tree-sitter-printf) - ISC License
- [properties](https://github.com/tree-sitter-grammars/tree-sitter-properties) - MIT License
- [puppet](https://github.com/tree-sitter-grammars/tree-sitter-puppet) - MIT License
- [pymanifest](https://github.com/tree-sitter-grammars/tree-sitter-pymanifest) - MIT License
- [python](https://github.com/tree-sitter/tree-sitter-python) - MIT License
- [python](https://github.com/tree-sitter/tree-sitter-python) - MIT License
- [ql](https://github.com/tree-sitter/tree-sitter-ql) - MIT License
- [qmldir](https://github.com/tree-sitter-grammars/tree-sitter-qmldir) - MIT License
- [query](https://github.com/tree-sitter-grammars/tree-sitter-query) - Apache License 2.0
- [r](https://github.com/r-lib/tree-sitter-r) - MIT License
- [rbs](https://github.com/joker1007/tree-sitter-rbs) - MIT License
- [re2c](https://github.com/tree-sitter-grammars/tree-sitter-re2c) - MIT License
- [readline](https://github.com/tree-sitter-grammars/tree-sitter-readline) - MIT License
- [requirements](https://github.com/tree-sitter-grammars/tree-sitter-requirements) - MIT License
- [ron](https://github.com/tree-sitter-grammars/tree-sitter-ron) - Apache License 2.0
- [rst](https://github.com/stsewd/tree-sitter-rst) - MIT License
- [ruby](https://github.com/tree-sitter/tree-sitter-ruby) - MIT License
- [rust](https://github.com/tree-sitter/tree-sitter-rust) - MIT License
- [scala](https://github.com/tree-sitter/tree-sitter-scala) - MIT License
- [scss](https://github.com/tree-sitter-grammars/tree-sitter-scss) - MIT License
- [slang](https://github.com/tree-sitter-grammars/tree-sitter-slang) - MIT License
- [smali](https://github.com/tree-sitter-grammars/tree-sitter-smali) - MIT License
- [solidity](https://github.com/JoranHonig/tree-sitter-solidity) - MIT License
- [sql](https://github.com/derekstride/tree-sitter-sql) - MIT License
- [squirrel](https://github.com/tree-sitter-grammars/tree-sitter-squirrel) - MIT License
- [starlark](https://github.com/tree-sitter-grammars/tree-sitter-starlark) - MIT License
- [svelte](https://github.com/tree-sitter-grammars/tree-sitter-svelte) - MIT License
- [swift](https://github.com/alex-pinkus/tree-sitter-swift) - MIT License
- [tablegen](https://github.com/tree-sitter-grammars/tree-sitter-tablegen) - MIT License
- [tcl](https://github.com/tree-sitter-grammars/tree-sitter-tcl) - MIT License
- [test](https://github.com/tree-sitter-grammars/tree-sitter-test) - MIT License
- [thrift](https://github.com/tree-sitter-grammars/tree-sitter-thrift) - MIT License
- [toml](https://github.com/tree-sitter-grammars/tree-sitter-toml) - MIT License
- [typescript](https://github.com/tree-sitter/tree-sitter-typescript) - MIT License
- [udev](https://github.com/tree-sitter-grammars/tree-sitter-udev) - MIT License
- [ungrammar](https://github.com/tree-sitter-grammars/tree-sitter-ungrammar) - MIT License
- [uxntal](https://github.com/tree-sitter-grammars/tree-sitter-uxntal) - MIT License
- [v](https://github.com/nedpals/tree-sitter-v) - MIT License
- [verilog](https://github.com/tree-sitter/tree-sitter-verilog) - MIT License
- [vim](https://github.com/tree-sitter-grammars/tree-sitter-vim) - MIT License
- [vue](https://github.com/tree-sitter-grammars/tree-sitter-vue) - MIT License
- [wgsl](https://github.com/szebniok/tree-sitter-wgsl) - MIT License
- [xcompose](https://github.com/tree-sitter-grammars/tree-sitter-xcompose) - MIT License
- [xml](https://github.com/tree-sitter-grammars/tree-sitter-xml) - MIT License
- [yaml](https://github.com/tree-sitter-grammars/tree-sitter-yaml) - MIT License
- [yuck](https://github.com/tree-sitter-grammars/tree-sitter-yuck) - MIT License

## Contributing

This library is open to and welcomes contributions.

### Setup

1. Fork the repository.
2. Make sure to have [PDM](https://pdm-project.org/en/latest/) installed on your machine.
3. You will also need the clang toolchain installed on your machine and available in path. Consult the pertinent
   documentation for your operating system.
4. Install the dependencies by running `pdm install`.
5. Install the git hooks with `pdm run pre-commit install && pdm run pre-commit install --hook-type commit-msg`

### Adding a new language

#### Adding a Binary Wheel Language

1. Add the language to the [sources/language_definitions.json](sources/language_definitions.json) file
   at the repository's root.

This file contains a JSON array of objects that adheres to the following json schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "LanguageDict",
  "description": "Language configuration for tree-sitter repositories.",
  "type": "object",
  "properties": {
    "repo": {
      "type": "string"
    },
    "branch": {
      "type": "string"
    },
    "directory": {
      "type": "string"
    },
    "cmd": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": [
    "repo"
  ],
  "additionalProperties": false
}
```

That is, each object must have a `repo` key, and optionally a `branch`, `directory`, and `cmd` keys.

- `repo` is the URL of the tree-sitter repository. This value is mandatory
- `branch` the branch of the repository to checkout. You should specify this only when the branch is not called `main` (
  i.e. for `master` or other names, specify this).
- `directory` is the directory under which there is an `src` folder. This should be specified only in cases where
  the `src` folder is not immediately under the root folder.
- `cmd` is a command to execute in a sub-process after cloning the repository. Its an array of commands strings that are
  concatenated, e.g. `["npm", "install"]`. This should be specified only if the binding needs to be build in the
  repository.

1. Update the `SupportedLanguage` literal type in the [__init__.py](./tree_sitter_language_pack/__init__.py) file.
2. Build the bindings by executing: `pdm run setup.py build_ext --inplace`
3. If the build is successful, execute the tests with `pdm run test`
4. If the tests pass, commit your changes and open a pull request.

#### Adding an installed binding
Some bindings are not build from source but are rather installed via PDM and are added to the package dependencies in the [pyproject.toml](./pyproject.toml) file.
To add an installed package follow these steps:

1. Install the bindings with `pdm add <bindings_package_name>`
2. Update both the literal type `InstalledBindings` and the `installed_bindings_map` dictionary in the [__init__.py](./tree_sitter_language_pack/__init__.py) file.
3. Build the bindings by executing: `pdm run setup.py build_ext --inplace`
4. If the build is successful, execute the tests with `pdm run test`
5. If the tests pass, commit your changes and open a pull request.
