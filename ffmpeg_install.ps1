#Downloading ffmpeg
wget https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip -outfile $Env:TEMP\ffmpeg.zip

#Unpacking ffmpeg
Expand-Archive -Path $Env:TEMP\ffmpeg.zip -DestinationPath $Env:USERPROFILE\AppData\Roaming\
Rename-Item -Path (Get-ChildItem -Path $Env:USERPROFILE\AppData\Roaming\ -Filter "ffmpeg-*").FullName  -NewName "ffmpeg"

#Deleting unnecessary files
Remove-Item -Path $Env:TEMP\ffmpeg.zip

#Adding ffmpeg to the current user's environment variables
$oldpath = Get-ItemProperty -Path "HKCU:\Environment" -Name "Path"
$newpath = $oldpath.Path += ";%USERPROFILE%\AppData\Roaming\ffmpeg\bin"
Set-ItemProperty -Path "HKCU:\Environment" -Name "Path" -Value $newpath

Start-Process SystemPropertiesAdvanced