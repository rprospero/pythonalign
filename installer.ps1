$source = "https://codeload.github.com/rprospero/pythonalign/zip/master"
$destination = "master.zip"

# Invoke-WebRequest $source -OutFile $destination

$shell_app=new-object -com shell.application
(Get-Location).Path + "\$destination"
$zip_file = $shell_app.namespace((Get-Location).Path + "\$destination")
$destination = $shell_app.namespace((Get-Location).Path)
$destination.Copyhere($zip_file.items())

cd pythonalign-master

pip3 install --user virtualenv
python3 -m virtualenv .
Scripts/activate.ps1
pip3 install -r requirements.txt
