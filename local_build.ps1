pip install -r requirements.txt
pip install -r requirements-dev.txt

python -m ok.update.copy_ok_folder

Get-ChildItem -Path .\src -Recurse -Filter *.py -Exclude '__init__.py' | ForEach-Object { Rename-Item $_.FullName -NewName ($_.FullName -replace '\.py$', '.pyx') }

$currentTag = git describe --tags $(git rev-list --tags="v*" --max-count=1 --current)

python setup.py build_ext --inplace
Get-ChildItem -Path .\src -Recurse -Filter *.pyx | ForEach-Object { Remove-Item $_.FullName }
Get-ChildItem -Path .\src -Recurse -Filter *.cpp | ForEach-Object { Remove-Item $_.FullName }


python -m ok.test.RunTests



python -m ok.update.package_launcher $currentTag deploy.txt
python -m ok.update.package_full_with_profile $currentTag 0
Copy-Item -Path "dist" -Destination "ok-nslg" -Recurse
7z a -t7z -r "ok-nslg-$currentTag.7z" "ok-nslg"
Remove-Item -Path "ok-nslg" -Recurse -Force


python -m ok.update.push_repos --repos https://pt6zehyzhff2:a53da683819bfc7720e03bc93928eed88c5028ba@e.coding.net/g-frfh1513/ok-wuthering-waves/ok-nslg.git --files deploy.txt
