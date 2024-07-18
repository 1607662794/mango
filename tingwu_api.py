# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys

from typing import List

from alibabacloud_tingwu20230930.client import Client as tingwu20230930Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tingwu20230930 import models as tingwu_20230930_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    @staticmethod
    def create_client() -> tingwu20230930Clie
    def __init__(self):
        pass
nt:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/tingwu
        config.endpoint = f'tingwu.cn-beijing.aliyuncs.com'
        return tingwu20230930Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        create_task_request = tingwu_20230930_models.CreateTaskRequest(
            type='your_value',
            operation='your_value'
        )
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.create_task_with_options(create_task_request, headers, util_models.RuntimeOptions())
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        create_task_request = tingwu_20230930_models.CreateTaskRequest(
            type='your_value',
            operation='your_value'
        )
        headers = {}
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.create_task_with_options_async(create_task_request, headers, util_models.RuntimeOptions())
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)


if __name__ == '__main__':
    Sample.main(sys.argv[1:])

