@echo off

IF "%1"=="fmt" (
    call batch\format.bat
) ELSE IF "%1"=="cov" (
    call batch\coverage.bat
) ELSE (
    echo Invalid flag. Please specify a valid flag.
)
