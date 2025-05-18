# lintx

[![License](https://img.shields.io/github/license/ai-agentx/lintx.svg?color=brightgreen)](https://github.com/ai-agentx/lintx/blob/main/LICENSE)
[![Tag](https://img.shields.io/github/tag/ai-agentx/lintx.svg?color=brightgreen)](https://github.com/ai-agentx/lintx/tags)



## Introduction

*lintx* is a lint agent.



## Build

```bash
uv build
uv pip install dist/lintx-*.whl
```



## Usage

```bash
usage: lintx [-h] [--language LANGUAGE] file

lintx

positional arguments:
  file                 Path to the code file to be linted

options:
  -h, --help           show this help message and exit
  --language LANGUAGE  Programming language of the code (optional)
```



## License

Project License can be found [here](LICENSE).



## Reference

- [camel-install](https://github.com/camel-ai/camel/blob/master/docs/get_started/installation.md)
- [uv-install](https://gist.github.com/craftslab/aabc92b5cbb1899d5b01a45a2ea5af21)
