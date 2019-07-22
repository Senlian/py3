import os, sys, hashlib


def isdir(target):
    return os.path.isdir(target)


def isfile(target):
    try:
        return os.path.isfile(target)
    except:
        return False


def get_md5(target):
    obj = hashlib.md5()
    if not isfile(target):
        if not isinstance(target, bytes):
            target = target.encode("utf-8")
        obj.update(target)
    else:
        with open(target, 'rb') as f:
            obj.update(f.read())
    return obj.hexdigest()


def get_configurer():
    from optparse import OptionParser
    usage = r"usage: %prog [-f] filepath [-l logfile]"
    parser = OptionParser(usage)
    # parser._add_help_option()
    if len(sys.argv) < 2:
        print('ERROR: Please give a file path!')
        parser.print_usage()
        exit(-1)

    parser.add_option('-f', '--file', dest='filepath', action='store', type='string',
                      default=sys.argv[1],
                      help='filepath, default is first arg, example:-f "filepath"')
    parser.add_option('-l', '--log', dest='logfile', action='store', type='string',
                      default='',
                      help='log file, default is "" ,example:-l "logfile"')
    parser.add_option('-r', '--rename', dest='rename', action='store_true', default=False,
                      help='rename, default is "False" ,example:-r')
    options, args = parser.parse_args()
    return options.filepath, options.logfile, options.rename


if __name__ == '__main__':
    file, logfile, rename = get_configurer()
    # file = r'D:\软件安全下载目录\镜像\RDO Setup.exe'
    # file2 = r'ftp://60.205.212.231/RDO Setup/RDO Setup.exe'
    md5 = get_md5(file)
    print(md5)
    # import ftplib
    # ftp = ftplib.FTP('60.205.212.231')
    # ftp.encoding='utf-8'
    # ftp.login('test', '123456')
    # ftp.cwd('/正式服/2019-07-22/平台/')
    #
    # files = (ftp.nlst())
    # data = [b'']
    # def add(b):
    #     data[0]+=b
    #     print(len(data[0]))
    # print(ftp.retrbinary(cmd='RETR %s' % 'netframwork.zip', callback=add, blocksize=1024*1024*1024))
    # print(get_md5(data[0]))
    # os.chdir(r'D:\软件安全下载目录\镜像')
    # print(get_md5('RDO Setup.exe'))
    if logfile:
        logfile = os.path.realpath(os.path.normpath(logfile))
        if not isdir(os.path.dirname(logfile)):
            os.makedirs(os.path.dirname(logfile))
        with open(logfile, 'w') as f:
            f.write(md5)
    if md5 and rename:
        os.rename(file, os.path.join(os.path.dirname(file), md5 + os.path.splitext(file)[1]))
