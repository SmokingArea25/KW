import openpyxl
import json


def load_excel_data(file_path):
    """
    解析excel内的测试用例
    """

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]  # 第一行为表头
    test_cases = []

    for row in sheet.iter_rows(min_row=2, values_only=True):  # 从第二行开始获取数据
        case = {headers[i]: row[i] for i in range(len(headers))}

        # 将json解析为字典
        if case.get("Headers"):
            case["Headers"] = json.loads(case["Headers"])
        if case.get("JSON"):
            case["JSON"] = json.loads(case["JSON"])
        if case.get("Response"):
            case["Response"] = json.loads(case["Response"])

        test_cases.append(case)

    return test_cases
