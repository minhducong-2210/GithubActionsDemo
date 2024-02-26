import unittest
from mock import create_autospec, Mock, MagicMock
from ppv_pal.interfaces.icare_about_test_result import ICareAboutTestResult
from ppv_pal.data_contracts.test_result import TestResult
from ppv_pal.interfaces.ilog import ILog
import sys
sys.path.append("C:\git\GithubActionsDemo\GithubActionsDemo")
from PythonScripts.product_independent.os_bdat_generator import OSBdatGenerator

class OSBdatGeneratorUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        self._mock_os_access_provider = Mock()
        self._mock_ituff_logger = create_autospec(ICareAboutTestResult)
        self._mock_logger = create_autospec(ILog)
        self._target = OSBdatGenerator(self._mock_logger, self._mock_ituff_logger,
                                                self._mock_os_access_provider)

    def test_return_output_pass(self):
        self.assertEqual(self._target.return_output(), True)
        self._mock_logger.log("No answer from Marionette").assert_not_called()

    def test_return_output_fail(self):
        self._target._os_access_provider.execute_command.return_value=None
        self.assertEqual(self._target.return_output(), False)
        self._mock_logger.log.assert_any_call("No answer from Marionette")
        _failed_result = TestResult()
        _failed_result.test_name ="os_bdat_output".upper()
        _failed_result.test_result = "No answer from Marionette"
        self._mock_ituff_logger.process_test_result.assert_any_call(_failed_result)

if __name__ == '__main__':
    unittest.main()