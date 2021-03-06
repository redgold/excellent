# -*- coding: utf-8 -*-
import exceltp.condition
from exceltp.config_define import *
import openpyxl


class Analyzer:

    def __init__(self, analyze_conf):
        self.condition_group_list = []
        self.analyze_data = []
        self.excel_workbook = None

        if analyze_conf is not None:
            self._parse_conf(analyze_conf)

    def _parse_conf(self, analyze_conf):
        # process 'analyze_conf' list info
        for group_dict in analyze_conf:

            # process dict info(group)
            #  - group_dict has key-value 1 pair.
            for group_name, conditions in group_dict.items():
                group = self._create_group(group_name, conditions)
                if group is None:
                    continue

            self.condition_group_list.append(group)

    def _create_group(self, group_name, group_conf):
        return exceltp.condition.ConditionGroup(group_name, group_conf)

    def set_excel_file(self, xls_filename):
        workbook = None

        try:
            workbook = openpyxl.load_workbook(filename = xls_filename)
        except Exception as e:
            print(e)

        if workbook is None:
            return False

        self.excel_workbook = workbook
        return True

    def set_excel_workbook(self, workbook):
        self.excel_workbook = workbook

    def analyze(self, verbose=True):
        if self.excel_workbook is None:
            return False

        # TODO : select worksheet. current work that all worksheet
        ws_sheet_total = len(self.excel_workbook.get_sheet_names())
        for ws_index, ws_name in enumerate(self.excel_workbook.get_sheet_names()):
            worksheet = self.excel_workbook.get_sheet_by_name(ws_name)

            if verbose:
                print("  process %d/%d sheet name '%s'" %
                            (ws_index+1, ws_sheet_total, worksheet.title))

            # send excel row to condition group
            for row in worksheet.rows:
                for group in self.condition_group_list:
                    # 'OR' logic per group
                    if group.match(row):
                        self.analyze_data.append(row)
                        break

        return True

    def get_analyze_data(self):
        return self.analyze_data

    def count_analyze_data(self):
        return len(self.analyze_data)

    def add_condition_group(self, group):
        self.condition_group_list.append(group)

    def remove_condition_group(self, group):
        self.condition_group_list.remove(group)

    def count_condition_group(self):
        return len(self.condition_group_list)
