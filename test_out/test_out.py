# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import time
import datetime
import timeit
import os
import shutil
import random
from box_it_up import Box

'''
Test result handler and formatter
'''
class TestOut(object):
    '''
    Purpose:
    The TestOut class is meant to provide logging and statistics for
    automated tests.

    Usage (Simple)
    * use test_start, test_end methods to start/end test timer, write test headers, etc.
    * timer_test will kickoff automatically when test_start is called
    * Example
        for i in xrange(1, max):
            test.test_start(i)
            result = <your test here: 'PASS', 'FAIL', or 'ERROR'>
            test.test_end(result)
        test.write_result_summary()

    Usage (Custom)
    * pass param 'CUSTOM' to test_start
    * Note: timer_start() will NOT kick-off automatically
    * <do any test setup (start selenium server, etc.)>
    * timer_start()
    * <start your test>
    * <end your test>
    * timer_end()
    * write_result_summary()

    '''

    def __init__(self):
        self._log_file = 'test.log'
        self.dir_current = os.getcwd()
        self._test_num = 0
        # self._test_result = []
        self._test_results = []
        # PASS, FAIL, ERROR
        self._test_result_count = [ 0, 0, 0 ]
        self._test_duration_total = 0
        self._timer_start = 0
        self._test_duration = 0
        self._test_duration_avg = 0

    @property
    def log_file(self):
        return self._log_file

    @log_file.setter
    def log_file(self, value):
        self._log_file = value

    @property
    def result_summary(self):
        return [
            [ 'AVG TEST DURATION',  '{}s'.format(self.test_duration_avg)],
            [ 'TEST RESULTS', 'PASS: {}, FAIL: {}, ERROR: {}'.format(
            self.test_result_count[0],
            self.test_result_count[1],
            self.test_result_count[2]
             )]
        ]

    @property
    def timer_start(self):
        return self._timer_start

    @timer_start.setter
    def timer_start(self, value):
        self._timer_start = value

    @property
    def test_num(self):
        return self._test_num

    @test_num.setter
    def test_num(self, value):
        self._test_num = value

    @property
    def test_results(self):
        return self._test_results

    @property
    def test_result_count(self):
        return self._test_result_count

    @test_result_count.setter
    def test_result_count(self, value):
        self._test_result_count = value

    @property
    def test_duration(self):
        return int(round(self._test_duration))

    @test_duration.setter
    def test_duration(self, value):
        self._test_duration = int(round(value))

    @property
    def test_duration_avg(self):
        if self.test_result_count[0] > 0:
            self._test_duration_avg = int(round(self._test_duration_total / self._test_result_count[0]))
        return int(round(self._test_duration_avg))

    @test_duration_avg.setter
    def test_duration_avg(self):
        self._test_duration_avg = int(round(self._test_duration_total / self._test_result_count[0]))

    @property
    def test_duration_total(self):
        return int(round(self._test_duration_total))

    @test_duration_total.setter
    def test_duration_total(self, value):
        self._test_duration_total += value

    def get_result_random(self):
        rand_int = random.randint(1, 3)
        if rand_int == 1:
            return 'PASS'
        elif rand_int == 2:
            return 'FAIL'
        else:
            return 'ERROR'

    def update_result_count(self, result, test_duration):
        if result is 'PASS':
            self._test_result_count[0] += 1
            self.test_duration_total = test_duration
        elif result is 'FAIL':
            self._test_result_count[1] += 1
        else: # ERROR
            self._test_result_count[2] += 1

    def _get_timestamp(self):
        ts = time.time()
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    def print_log(self, message, log_type='SUB_SECTION'):
        if log_type is 'BIG_BANNER':
            line = '******************\n******************\n******************\n******************\n******************'
            print line
            print '\n{}\n'.format(message)
            print line
        elif log_type is 'NEW_SECTION':
            header_line = '=' * 70
            print '\n\n{}\n{}\n{}\n'.format(header_line, message, header_line)
        elif log_type is 'SUMMARY':
            header_line = '*' * 70
            print '\n\n{}\n{}\n{}'.format(header_line, message, header_line) + '\n'
        else:
            header_line = '-' * 45
            print '\n{}\n{}\n{}'.format(header_line, message, header_line)

    def write_result(self, result, message, test_duration):
        message = str(message)

        # write to: stdout
        print '\nTEST RESULT: {} {}'.format(result, message)
        print 'TEST DURATION: {}s'.format(self.test_duration)

        # write to: log file
        orientations = [ '>', '^', '>', '^', '<' ]
        box = Box(table_data=self._test_results, type='MINIMAL', col_orientations=orientations)
        summary = box.box_it()

        log_file = open(self._log_file, "w")
        log_file.write(summary + '\n\n')
        log_file.close()


    def write_result_summary(self):

        box = Box(table_data=self.result_summary, type='SIMPLE_OUTLINE', header=False)

        # write to: stdout
        summary = box.box_it()
        self.print_log('SUMMARY RESULTS', 'SUMMARY')
        print summary + '\n\n'

        # write to: log file
        # Note: we keep around the extra file til the last minute
        #       in case the script crashes, we still have current log
        summary = '\nTEST RESULT SUMMARY{}\n\n'.format(summary)

        log_file_tmp = self._log_file.replace('.log', '_summary.log')
        log_file = open(log_file_tmp, "w")
        with open (self._log_file, "r") as myfile:
            test_data=myfile.read()

        log_file.write(summary)
        log_file.write(test_data)
        log_file.close()
        shutil.copy(log_file_tmp, self._log_file)
        os.remove(log_file_tmp)

    def timer_start(self):
        self._timer_start = timeit.default_timer()

    def timer_end(self):
        self.test_duration = timeit.default_timer() - self._timer_start

    def test_start(self, test_num=0, test_type='SIMPLE'):
        self.test_num = test_num
        if test_num != 0:
            self.print_log('TEST RUN # {}'.format(test_num), 'NEW_SECTION')
        else:
            self.print_log('TEST RUN', 'NEW_SECTION')
        if test_type is 'SIMPLE':
            self.timer_start()

    def test_end(self, result_pass_fail, comment='', test_type='SIMPLE'):
        if test_type is 'SIMPLE':
            self.timer_end()

        self.update_result_count(result_pass_fail, self.test_duration)

        result = []
        result.append(self.test_num)
        result.append(self._get_timestamp())
        result.append(str(self.test_duration) + 's')
        result.append(result_pass_fail)
        result.append(comment)

        if self.test_num == 1:
            header = [ '#', 'TIMESTAMP', 'TIME', 'RESULT', 'DESCRIPTION' ]
            self._test_results.append(header)
        self._test_results.append(result)

        self.write_result(result_pass_fail, comment, self.test_duration)

if __name__ == '__main__':

    '''
    Example usage
    '''
    test = TestOut()

    ###########################
    # Example #1 - Simple Usage
    ###########################
    # for i in xrange(1, 6):
    #     test.test_start(i)
    #
    #     # FAKE TEST
    #     print 'running your test here...'
    #     result = test.get_result_random()
    #     comment = 'This test was bogus, bro!'
    #     time.sleep(2)
    #
    #     test.test_end(result, comment)
    #
    # test.write_result_summary()

    ###########################
    # Example #2 - Custom Usage
    ###########################
    for i in xrange(1, 6):
        test.test_start(i, 'CUSTOM')
        test.print_log('TEST SETUP'.format(i))
        print 'starting Selenium'
        print 'starting apache'
        print 'starting server XYZ'
        test.print_log('START TEST'.format(i))
        test.timer_start()

        # FAKE TEST
        print 'running your test here...'
        result = test.get_result_random()
        time.sleep(2)
        test.timer_end()
        test.test_end(result)

    test.write_result_summary()


