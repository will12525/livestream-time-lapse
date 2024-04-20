from unittest.mock import patch


def patch_time_time(test_class, ret_val):
    patcher = patch('time.time')
    test_class.time = patcher.start()
    test_class.time.return_value = ret_val
    test_class.addCleanup(patcher.stop)


def patch_time_strftime(test_class, ret_val):
    patcher = patch('time.strftime')
    test_class.time = patcher.start()
    test_class.time.return_value = str(ret_val)
    test_class.addCleanup(patcher.stop)
