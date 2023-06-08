from leeger.util.excel import leagueToExcel
from variables import LEAGUE
import os

if __name__ == "__main__":
    tempDir = os.environ["TEMP_DIR"]

    leagueToExcel(LEAGUE, f"{tempDir}\\excel.xlsx")
