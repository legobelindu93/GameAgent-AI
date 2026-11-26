def main():
    import sys
    if "--classic" not in sys.argv:
        try:
            import PySide6
        except ImportError:
            pass
        else:
            from .obsidian_ui import main as modern
            return modern()
    from .launcher_ui import main as classic
    return classic()

if __name__=="__main__":main()
