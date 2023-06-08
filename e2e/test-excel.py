from leeger.util.excel import leagueToExcel
from variables import LEAGUE
import os

if __name__ == "__main__":
    tempDir = os.environ["TEMP_DIR"]

    fullPath = os.path.abspath(os.path.join(tempDir, "excel.xlsx"))

    print(f"fullPath: {fullPath}")

    leagueToExcel(LEAGUE, fullPath)
