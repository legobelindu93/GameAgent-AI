# Upstream interface bridges
Inspected root trees and actual entrypoints of all six projects. NIKKEAutoScript and StarRailCopilot expose gui.py with host and port options. OK-WW and OK-NTE expose main.py. The bridge uses an existing reviewed isolated Python environment or an installed executable. MFABD2 and BetterGI use their native release packages; latest source and MFABD2 README indicate .NET 10, not .NET 8. Check the exact MFABD2 release and its client support; prior classic PC capture was observed.
Source references:
- https://github.com/megumiss/NIKKEAutoScript/blob/master/gui.py
- https://github.com/sunyink/MFABD2/blob/main/assets/interface.json
- https://github.com/babalae/better-genshin-impact/blob/main/BetterGenshinImpact/BetterGenshinImpact.csproj
- https://github.com/ok-oldking/ok-wuthering-waves/blob/master/main.py
- https://github.com/BnanZ0/ok-nte/blob/main/main.py
- https://github.com/LmeSzinc/StarRailCopilot/blob/master/gui.py
Inventory is read-only, not a task execution API. Original interfaces retain their own features. No game-specific functions have been ported to the shared AI, no automatic startup tasks are passed, no anti-cheat bypass. The source environments may require additional upstream deployment steps; not all actual launches have been tested.


Current version: 0.15. See the [user guide](user-guide.md) and [technical reference](technical-reference.md).
