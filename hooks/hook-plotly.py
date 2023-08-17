from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_data_files
hiddenimports = collect_submodules('plotly')

datas = collect_data_files('plotly', include_py_files=True)
datas = collect_data_files('_plotly_utils', include_py_files=True)
