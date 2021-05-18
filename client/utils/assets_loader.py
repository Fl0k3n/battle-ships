from pathlib import Path


class AssetsLoader:
    _PARENT_DIR = Path(__file__).absolute().parent.parent
    _ASSETS_DIR_NAME = 'assets'

    @classmethod
    def get_path(cls, path: str) -> str:
        f"""Returns absolute path of resource stored within {cls._ASSETS_DIR_NAME} directory.
        Args:
            path (str): path relative to assets directory 
        Returns:
            str: absolute path of resource
        """
        return str(Path.joinpath(cls._PARENT_DIR, cls._ASSETS_DIR_NAME, path))
