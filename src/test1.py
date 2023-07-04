import unittest
from src.readAndWrite import ReadAndWrite

class TestReadAndWrite(unittest.TestCase):

    def setUp(self):
        self.data = ReadAndWrite()

    def tearDown(self):
        # 清理测试产生的资源
        pass

    def test_get_value(self):
        # 测试添加键值对并获取值
        key = 'new_key'
        value = 'new_value1'
        self.data.setValue(key, value)
        self.assertEqual(self.data.datatext[key], value)

    def test_read_nonexistent_key(self):
        # 测试读取不存在的键
        non_existent_key = 'non_existent_key'
        self.assertIsNone(self.getValue(non_existent_key))

    def test_read_existent_key(self):
        key = '123'
        self.assertEqual(self.getValue(key), '123435')


if __name__ == '__main__':
    unittest.main()
