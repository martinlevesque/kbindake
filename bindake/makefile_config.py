from dataclasses import dataclass


@dataclass
class MakefileConfig:
    filepath: str

    def read_file_lines(self):
        with open(self.filepath, "r", encoding="utf-8") as file:
            return file.readlines()

    def parse(self):
        pass
