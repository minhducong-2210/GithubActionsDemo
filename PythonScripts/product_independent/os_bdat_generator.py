from ppv_pal.data_contracts.test_result import TestResult
class OSBdatGenerator():
        def __init__(self, logger, ituff_logger, os_access_provider):
            self._os_access_provider = os_access_provider
            self._ituff_logger = ituff_logger
            self._logger = logger
            self._command ='bdat_extractor -p "EMR" -tse -f "PPV" -o "/root/content/LOS/Bdat_Extractor/result/"'
            self._result = True

        def _log_to_ituff(self, testname, testresult):
            result = TestResult()
            result.test_name = testname.upper()
            result.test_result = testresult
            self._ituff_logger.process_test_result(result)

        def _send_command(self):
            self._marionette_output = self._os_access_provider.execute_command(self._command, 60, True, 1)
            if self._marionette_output is None:
                # self._result = False
                self._log_to_ituff("os_bdat_output", "No answer from Marionette")
                self._log_to_ituff("os_bdat_output_answer", str(self._marionette_output))
                self._logger.log("No answer from Marionette")

            self._logger.log(f"Marionette Output: {str(self._marionette_output)}")

        def return_output(self):
            self._logger.log(f"Checking command: {self._command}")
            for retry in range(1):
                self._logger.log(f"Retry: #{retry + 1}")
                response = self._send_command()
                self._logger.log(f"Bdat Response: {response}")
                self._logger.log(f"Bdat Response1: {response}")
                self._logger.log(f"Bdat Response1: {response}")
            return self._result