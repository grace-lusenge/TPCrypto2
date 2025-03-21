[Setup]
AppName=CryptoAnalyse
AppVersion=1.0
AppVerName=CryptoAnalyse 1.0
DefaultDirName={pf}\CryptoAnalyse
DefaultGroupName=CryptoAnalyse
OutputDir=.
OutputBaseFilename=CryptoAnalyse_Installer
Compression=none

[Files]
Source: "dist\CryptoAnalyse.exe"; DestDir: "{app}"; Flags: ignoreversion




[Icons]
Name: "{group}\CryptoAnalyse"; Filename: "{app}\CryptoAnalyse.exe"
Name: "{userdesktop}\CryptoAnalyse"; Filename: "{app}\CryptoAnalyse.exe"

