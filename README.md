test-out
========

Class to provide helpful logging, test run data and summary statistics for automated tests.


## Usage

### Example \#1 - Simple Reporting 
* use test_start() & test_end() methods to bookend your test code
* timer_test will kickoff automatically when test_start is called
* Example
```
import TestOut from test_out

        for i in xrange(1, max):
            test.test_start(i)
            result = <your test here: 'PASS', 'FAIL', or 'ERROR'>
            test.test_end(result)
        test.write_result_summary()
```

### Example \#2 - Custom reporting with service startup, etc. 
* pass param 'CUSTOM' to test_start: ` test_start('CUSTOM')
* Note: timer_start() will NOT kick-off automatically
* <do any test setup (start selenium server, etc.)>
* timer_start()
* <start your test>
* <end your test>
* timer_end()
* write_result_summary()
```
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
```