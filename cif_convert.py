import argparse
import re
import sys


atom_re = re.compile(r'\b(C|H)(\d+)([a-zA-Z]?)\b')


def test_atom_re():
    assert atom_re.match("C14")
    assert atom_re.match("C14x")
    assert atom_re.match("C1778")
    assert atom_re.match("H1778")
    assert atom_re.match("dC14") is None
    assert atom_re.match("C14xy") is None
    assert atom_re.match("D1778") is None

    def substitute(x):
        return 'x'

    assert atom_re.sub(substitute, "C14 xC34") == 'x xC34'

    match = atom_re.match("C14x")
    assert match.group(1) == "C"
    assert match.group(2) == "14"
    assert match.group(3) == "x"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cif')
    parser.add_argument('permutation')
    args = parser.parse_args()

    replacements = {}
    with open(args.permutation) as f:
        for line in f:
            current, desired = line.split()  
            current = int(current)
            desired = int(desired)
            replacements[current] = desired

    with open(args.cif) as f:
        cif_text = f.read()

    def substitute(match):
        element = match.group(1)
        number = int(match.group(2))
        suffix = match.group(3)
        desired = replacements.get(number, number)
        return ''.join([element, str(desired), suffix])

    sys.stdout.write(atom_re.sub(substitute, cif_text))
