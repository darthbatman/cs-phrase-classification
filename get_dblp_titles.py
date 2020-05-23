def get_dblp_titles():
    with open('data/dblp/dblp_titles.txt', 'w') as fw:
        with open('data/dblp/dblp.xml', 'r') as fr:
            line = fr.readline()
            while line:
                if '<title>' in line and '</title>' in line:
                    title = line.split('<title>')[1].split('</title>')[0]
                    fw.write(title + '\n')
                line = fr.readline()
            fr.close()
        fw.close()


if __name__ == '__main__':
    get_dblp_titles()
