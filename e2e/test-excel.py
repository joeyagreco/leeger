import os

from variables import LEAGUE

from leeger.util.excel import leagueToExcel

if __name__ == "__main__":
    tempDir = os.environ["TEMP_DIR"]

    fullPath = os.path.abspath(os.path.join(tempDir, "excel.xlsx"))

    leagueToExcel(LEAGUE, fullPath)
