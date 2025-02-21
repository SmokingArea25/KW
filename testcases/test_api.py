import sys
import os
import pytest
import allure

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.request_handler import RequestHandler
from utils.excel_handler import load_excel_data

# 获取excel内的测试case
test_data = load_excel_data("testcases/test_data.xlsx")

# 实例化请求处理对象
request_handler = RequestHandler()


@pytest.mark.parametrize(
    "case",
    test_data,
    ids=lambda case: case["Name"].encode('utf-8').decode('utf-8')
)
@allure.story("接口测试用例")
def test_api(case):
    response = request_handler.send_request(
        method=case["Method"],
        url=case["URL"],
        headers=case.get("Headers"),
        json=case.get("JSON")

    )

    with allure.step("断言 HTTP 状态码"):
        assert response.status_code == case["Status"], f"预期 {case['Status']}，实际 {response.status_code}"

    with allure.step("断言响应内容"):
        for key, value in case["Response"].items():
            assert response.json().get(key) == value, f"字段 {key} 预期 {value}，实际 {response.json().get(key)}"

    # 记录请求和响应信息到 allure 报告
    with allure.step("记录请求和响应信息"):
        allure.attach(str(case), name="请求信息", attachment_type=allure.attachment_type.JSON)
        allure.attach(response.text, name="响应数据", attachment_type=allure.attachment_type.JSON)
