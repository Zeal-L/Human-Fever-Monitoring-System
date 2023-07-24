class ReadAndWrite():
    datatext = {}
    filename = '/home/pi/project/storage/data.txt'

    @staticmethod
    def __write_dict_to_file(data):
        with open(ReadAndWrite.filename, 'a') as file:
            print(data)
            for key, value in data.items():
                file.write(f"{key}: {value}\n")
            file.close()

    @staticmethod
    def __allReadData():
        allData = {}
        with open(ReadAndWrite.filename, 'r') as file:
            for line in file:
                key, value = line.strip().split(':')
                allData[key.strip()] = value.strip()
            file.close()
        
        return allData

    @staticmethod
    def getValue(findkey):
        if findkey in ReadAndWrite.datatext:
            return ReadAndWrite.datatext[findkey]
        data = ReadAndWrite.__allReadData()
        if findkey in data:
            return data[findkey]
        return None
        # 这里data是所有的数据

    @staticmethod
    def check_update(keyadd, valueadd):
        # true 是不用写， false 是要写
        # 在内存里
        if keyadd in ReadAndWrite.datatext:
            # 一样，文件里不用改
            if ReadAndWrite.datatext[keyadd] == valueadd:
                return True
            #else:
            # 不一样，内存和文件都要改
            ReadAndWrite.__update_file(keyadd, valueadd)
            ReadAndWrite.datatext[keyadd] = valueadd
            return True
        
        # 在文件里
        if ReadAndWrite.getValue(keyadd) is None:
            return False    # 文件里没有这个键, 新的直接写
        if valueadd == ReadAndWrite.getValue(keyadd):
            ReadAndWrite.datatext[keyadd] = valueadd
            return True # 一样别写
        # 最离谱的情况，文件里有错的
        # 删除文件当新的得了
        ReadAndWrite.__delect_file(keyadd)
        return False
            
    @staticmethod
    def __update_file(keychange, valuechange):
        alldata = ReadAndWrite.__allReadData()
        with open(ReadAndWrite.filename, 'w') as file:
            for key, value in alldata.items():
                if key == keychange:
                    file.write(f"{key}: {valuechange}\n")
                else:
                    file.write(f"{key}: {value}\n")
            file.close()
    
    @staticmethod
    # 确定有这个key才行
    def __delect_file(keychange):
        alldata = ReadAndWrite.__allReadData()
        with open(ReadAndWrite.filename, 'w') as file:
            for key, value in alldata.items():
                if key == keychange:
                    continue
                file.write(f"{key}: {value}\n")
            file.close()
            
    @staticmethod
    def setValue(key, value):
        if ReadAndWrite.check_update(key, value) is True:
            return
        newdate = {key:value}
        ReadAndWrite.__write_dict_to_file(newdate)
        ReadAndWrite.datatext.update(newdate)
