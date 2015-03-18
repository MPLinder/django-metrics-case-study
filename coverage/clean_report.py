def clean_report(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    with open(path, 'w') as f:
        for line in lines:
            if line.endswith('%\n'):
                f.write(line[:len(line)-2]+'\n')

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.exit("Script takes exactly one argument, which should be the path to a coverage.py report file.")
    path = sys.argv[1]
    clean_report(path)
