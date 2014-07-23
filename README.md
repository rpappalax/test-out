test-out
========

Python class to provide useful logging, test run data and summary statistics for automated tests.

## Features
- Bookend your test code with test_start, test_end methods
- This will start/stop test timers, provide average test duration
- Track test results
- Log test run and summary test results to console and log file


## Usage

### Example \#1 - Simple Reporting 
- use test_start() & test_end() methods to bookend your test code
- timer_test will kickoff automatically when test_start is called
- see: [Sample output](https://github.com/rpappalax/test-out/blob/master/Examples/console_log_simple.txt)

```
import time
from test_out import TestOut 

tout = TestOut()

for i in xrange(1, 6):
    tout.test_start(i)
    
    # FAKE TEST
    print 'running your test here...'
    # your result must be: 'PASS', 'FAIL' or 'ERROR'
    # generating random for this example:
    result = tout.get_result_random()
    comment = ' - This test is bogus, bro!'
    time.sleep(2)
    
    tout.test_end(result, comment)
    
tout.write_result_summary()
```

### Example \#2 - Custom reporting with service startup, etc. 
- pass param 'CUSTOM' to test_start: ` test_start 
- Note: timer_start() will NOT kick-off automatically
- \[do any test setup (start selenium server, etc.)\]
- timer_start()
- \[start your test\]
- \[end your test\]
- timer_end()
- write_result_summary()
-see: [Sample output](https://github.com/rpappalax/test-out/blob/master/Examples/console_log_custom.txt)

```
import time
from test_out import TestOut 

tout = TestOut()

for i in xrange(1, 6):
    tout.test_start(i, 'CUSTOM')
    tout.print_log('TEST SETUP'.format(i))
    print 'starting Selenium'
    print 'starting apache'
    print 'starting server XYZ'
    
    tout.print_log('START TEST'.format(i))
    tout.timer_start()

    # FAKE TEST
    print 'running your test here...'
    # your result must be: 'PASS', 'FAIL' or 'ERROR'
    # generating random for this example:
    result = tout.get_result_random()
    comment = '- This test is bogus, bro'
    time.sleep(2)
    tout.timer_end()
    tout.test_end(result, comment)

test.write_result_summary()
```