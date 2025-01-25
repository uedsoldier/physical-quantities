import unittest

def all_tests_passed():
    # Create a test suite that discovers all tests in the current directory
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='.', pattern='test*.py')

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Check if all tests passed
    return result.wasSuccessful()

if __name__ == '__main__':
    if all_tests_passed():
        print('All tests passed successfully!')
    else:
        print('Some tests failed. Check the output above for details.')

