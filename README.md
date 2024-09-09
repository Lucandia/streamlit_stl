# Streamlit STL Display Component

A Streamlit component to display STL files.

## Installation

**This component requires access to write files to the temporary directory.**

```
pip install streamlit_stl
```

## Example

![Alt Text](https://github.com/Lucandia/streamlit_stl/blob/main/example.png?raw=true)

Look at the [example](https://st-stl.streamlit.app/) for a streamlit Web App:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://st-stl.streamlit.app/)

The original STL file is from [Printables](https://www.printables.com/it/model/505713-flexifier-flexi-3d-models-generator-print-in-place).

## Usage

### Display from file paths

```
import streamlit as st
from streamlit_stl import stl_from_file

success = stl_from_file(file_path=path_to_conf,     # path to the stl file
                        color='#FF9900',            # color of the stl file
                        material='material',        # material of the stl file, either 'material' or 'wireframe'
                        auto_rotate=True,           # auto rotate the stl file
                        height='500',               # height of the viewer frame
                        key=None)                   # streamlit component key
```

### Display from file text

```
import streamlit as st
from streamlit_stl import stl_from_text

file_input = st.file_uploader("Or upload a STL file ", type=["stl"])

success = stl_from_text(text=file_input.getvalue(), # text of te stl file
                        color='#FF9900',            # color of the stl file
                        material='material',        # material of the stl file, either 'material' or 'wireframe'
                        auto_rotate=True,           # auto rotate the stl file
                        height='500',               # height of the viewer frame
                        key=None)                   # streamlit component key
```

The functions return a boolean value indicating if the program was able to write and read the files.

## License

Code is licensed under the GNU General Public License v3.0 ([GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html))

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%20v3-lightgrey.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)
