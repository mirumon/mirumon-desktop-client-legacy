* Use `nuitka` to convert python code to `.exe`:

```bash
python -m nuitka --standalone --windows-dependency-tool=pefile --experimental=use_pefile_recurse --experimental=use_pefile_fullrecurse --follow-imports  --mingw64 --show-progress tmp.service.py
```

nssm set mirumon AppExit Default Restart
nssm set mirumon AppRestartDelay 0

nssm set mirumon AppStdout C:\games\ut2003\service.log
nssm set mirumon AppStderr C:\games\ut2003\service.log


nssm remove test_service confirm


```bash
python -m app.main
```