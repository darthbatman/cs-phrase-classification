with open('more.txt', 'w') as wf:
    with open('nngp.txt', 'r') as f:
        line = f.readline()[:-1]
        while True:
            if len(line.strip()) > 0:
                print(line)
                which = input('1 or 0: ')
                if which == '1':
                    wf.write(line + ',True\n')
                else:
                    wf.write(line + ',False\n')
            line = f.readline()[:-1]
        f.close()
    wf.close()
