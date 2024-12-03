from . import base_solution as bs


class SolutionDay02(bs.BaseSolution):
    def __init__(self, day_num: int, example=False, verbose=False):
        super().__init__(day_num, example, verbose=verbose)

    def _star_1(self) -> None:
        """Check each report for its validity

        :return:
        """
        input_file = self.get_input_file_path()
        safe_reports = 0
        with open(input_file, 'r') as of:
            while line := of.readline():
                report = [int(x) for x in line.strip().split(' ')]
                safety = self.check_report(report)
                safe_reports += safety

        return safe_reports

    def _star_2(self) -> None:
        """Check each report for its validity, where one level/item of the report can be excluded.

        The approach taken might not be the ideal one, but still do-able since the length of the reports is constant (7)
        and also not very large. So, we check every possible "sub-report" (skipping one level).
        This means, every input needs to be checked at most 7 times...
        So, it is kind of O(7*n), which counts still as linear.

        :return:
        """
        input_file = self.get_input_file_path()
        safe_reports = 0
        with open(input_file, 'r') as of:
            while line := of.readline():
                report = [int(x) for x in line.strip().split(' ')]
                for skip in range(len(report)):
                    sub_report = report[:skip] + report[skip+1:]
                    if self.check_report(sub_report):
                        safe_reports += 1
                        # Leave the loop, we found one, that's enough
                        break

        return safe_reports

    def check_report(self, report):
        """Check one report

        A report needs to consist of either strictly increasing or decreasing levels.
        Further, two consecutive levels should not be further apart than three from each other

        :param report: list of integers
        :return: 0 for unsafe reports, 1 for safe reports
        """
        # First to levels define the sign, it's either positive (increasing report) or negative (decreasing report)
        sign = 1 if report[1] > report[0] else -1
        for i in range(len(report) - 1):
            l1, l2 = report[i:i + 2]
            if sign * (l2 - l1) <= 0 or abs(l2 - l1) > 3:
                return 0

        return 1
