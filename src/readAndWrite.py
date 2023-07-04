
class ReadAndWrite():
    
    def __init__(self):
        self.datatext = {}
        self.filename = '/home/pi/project/storage/data.txt'

    def __write_dict_to_file(self, data):
        with open(self.filename, 'a') as file:
            print(data)
            for key, value in data.items():
                file.write(f"{key}: {value}\n")
            file.close()


    def __allReadData(self):
        allData = {}
        with open(self.filename, 'r') as file:
            for line in file:
                key, value = line.strip().split(':')
                allData[key.strip()] = value.strip()
            file.close()
        
        return allData


    def getValue(self, findkey):
        if findkey in self.datatext:
            return self.datatext[findkey]
        data = self.__allReadData()
        if findkey in data:
            return data[findkey]
        return None
        # 这里data是所有的数据


    def check_update(self, keyadd, valueadd):
        # true 是不用写， false 是要写
        # 在内存里
        if keyadd in self.datatext:
            # 一样，文件里不用改
            if self.datatext[keyadd] == valueadd:
                return True
            #else:
            # 不一样，内存和文件都要改
            self.__update_file(keyadd, valueadd)
            return False
        
        # 在文件里
        if self.getValue(keyadd) is None:
            return False    # 文件里没有这个键, 新的直接写
        if valueadd == self.getValue(keyadd):
            self.datatext[keyadd] = valueadd
            return True # 一样别写
        # 最离谱的情况，文件里有错的
        # 删除文件当新的得了
        self.__delect_file(keyadd)
        return False
            
        
    # 确定有这个key才行
    def __delect_file(self, keychange):
        alldata = self.__allReadData()
        with open(self.filename, 'w') as file:
            for key, value in alldata.items():
                if key == keychange:
                    continue
                file.write(f"{key}: {value}\n")
            file.close()


    def setValue(self, key, value):
        if self.check_update(key, value) is True:
            return
        newdate = {key:value}
        self.__write_dict_to_file(newdate)
        self.datatext.update(newdate)
