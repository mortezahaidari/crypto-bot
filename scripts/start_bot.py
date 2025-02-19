import subprocess
import sys

def main():
    subprocess.run([sys.executable, '-m', 'src.core.bot'])

if __name__ == '__main__':
    main()
