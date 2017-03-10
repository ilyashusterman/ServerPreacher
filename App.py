import argparse
import json, requests
import time
import threading

exit_flag = 0


class FactorizeThread(threading.Thread):
    def __init__(self, threadID, name, counter, url, data):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.url = url
        self.data = data
        self.name = name
        self.counter = counter

    def run(self):
        print "Starting " + self.name
        penetrate_url(self.name, self.counter, 200, self.url, self.data)
        print "Exiting " + self.name


def penetrate_url(thread_name, delay, counter, url, data):
    while counter:
        if exit_flag:
            thread_name.exit()
        time.sleep(delay)
        r = requests.post(url, data=json.dumps(data))
        print(r)
        counter -= 1


class App(object):
    def __init__(self, url, filename=None):
        self.json_spec = {'command': 'summary'}
        self.url = url
        self.filename = filename

    def operate_times(self, urls):
        start = time()
        threads = []
        for url in urls:
            thread = FactorizeThread(100, 'operate', 10, url, self.json_spec)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        end = time()
        print('Took % .3fseconds' % (end - start))

    def crack(self):
        print('Begin to crack the api ...')
        self.operate_times([self.url] * 50)

    @classmethod
    def main(cls):
        parser = argparse.ArgumentParser()
        commands = parser.add_mutually_exclusive_group(required=True)
        commands.add_argument('--crack', action='store_true')
        commands.add_argument('--filter', action='store_true')
        parser.add_argument('--url', required=True, help='Enter the url http://example.com')
        parser.add_argument('-f', '--filename', default=None,
                            help='Custom ou'
                                 'tput')
        args = parser.parse_args()
        report = cls(args.url)
        if args.crack:
            report.crack()
        elif args.filter:
            report.filter()
        elif args.insert:
            raise NotImplementedError()
        else:
            print 'Nothing to do.'


if __name__ == '__main__':
    App.main()
