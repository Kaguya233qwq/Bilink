import importlib
from pathlib import Path
from ..utils.logger import Logger


def load_all():
    """
    加载所有插件
    """
    # 获取指定目录路径下的所有 .py 文件

    directory = Path(__file__).parent.parent / "plugins"
    if not directory.exists():
        Logger.success("插件目录初始化成功，请在plugins文件夹下创建你的插件")
        directory.mkdir()
        return
    for module_file in directory.glob("*.py"):
        # 获取模块名（去掉 .py 后缀）
        module_name = module_file.stem
        # 动态导入模块
        importlib.import_module(f".plugins.{module_name}","src.bilink")
        Logger.success(f"plugin {module_name} loaded successfully")
