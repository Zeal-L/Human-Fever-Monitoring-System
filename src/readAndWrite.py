import ast

def write_dict_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(str(data))

def read_dict_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
        data = ast.literal_eval(content)
        if isinstance(data, dict):
            return data
        else:
            raise ValueError('File does not contain a dictionary.')

# 示例用法
filename = 'data.txt'

# 写入字典到文件
my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
write_dict_to_file(filename, my_dict)

# 从文件中读取字典
read_data = read_dict_from_file(filename)
print(read_data)

















