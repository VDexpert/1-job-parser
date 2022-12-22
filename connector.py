import json
import os.path

class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    def __init__(self, df):
        self.__data_file = df
        self.__connect()

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        if os.path.exists(self.__data_file):
            with open(self.__data_file, "r") as f:
                try:
                    return json.load(f)
                except Exception:
                    raise ValueError("Файл не json-формата или был подвергнут деградации")
        else:
            with open(self.__data_file, "w") as f:
                null_source = []
                json.dump(null_source, f)

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        with open(self.__data_file, "r") as f:
            source_data = self.__connect()
            source_data += data
            source_data = [data]
            with open(self.__data_file, "w") as outfile:
                json.dump(source_data, outfile, indent=2)

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        with open(self.__data_file, "r") as f:
            source_data = self.__connect()
            key_filter = [x for x in query.keys()]
            value_filter = [x for x in query.values()]
            if not query or not value_filter:
                print("Исходные данные")
                return source_data
            else:
                res_data = []
                for item in source_data:
                    if item[key_filter[0]] == value_filter[0]:
                        res_data.append(item)
                print("Селективные данные")
                return res_data



    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        with open(self.__data_file, "r") as f:
            source_data = self.__connect()
            key_filter = [x for x in query.keys()]
            value_filter = [x for x in query.values()]
            if not query or not value_filter:
                print("Не переданы параметры для удаления")
            else:
                res_data = []
                for item in source_data:
                    if item[key_filter[0]] == value_filter[0]:
                        continue
                    else:
                        res_data.append(item)
                with open(self.__data_file, "w") as outfile:
                    json.dump(res_data, outfile, indent=2)



if __name__ == '__main__':
    df = Connector('df.json')

    data_for_file = {'id': 1, 'title': 'tet'}

    df.insert(data_for_file)
    data_from_file = df.select(dict())
    assert data_from_file == [data_for_file]

    df.delete({'id':1})
    data_from_file = df.select(dict())
    assert data_from_file == []