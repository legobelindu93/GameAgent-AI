# Windows native host — v0.15

Install modern-ui and native-ui extras. The console can explicitly provision .NET Desktop Runtime 10 and VC++ x64 via winget for BetterGI/MFABD2, or a reviewed root requirements.txt in an isolated uv environment for supported Python projects. This is not a universal installer.

In Interface native, select a visible window owned by the process started from this console. The Qt NativeSurface adapter reuses WindowHost and Win32 SetParent; parent, style and rectangle are saved for detach. DPI, privilege and process ownership affect compatibility. Child-process launchers are not supported. Use external mode or the classic launcher if incompatible. Do not elevate GameAgent to bypass permissions.

Prior MFABD2 capture/embedding was manually observed using the classic launcher; the Qt adapter still requires actual Windows acceptance. Offscreen CI tests construction only. No task execution API or automatic game actions are introduced.
