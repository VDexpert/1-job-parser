import json
import os.path

class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None
    all_connectors = {}

    def __init__(self, filename):
        self.all_connectors[filename] = self
        self.__data_file = filename
        self.connect()

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self.connect()

    def connect(self):
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
            source_data = self.connect()
            source_data += data
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
            source_data = self.connect()
            key_filter = [x for x in query.keys()]
            value_filter = [x for x in query.values()]
            if not query or not value_filter:
                return source_data
            else:
                res_data = []
                for i in source_data:
                    if i[key_filter[0]] == value_filter[0]:
                        res_data.append(i)
                return res_data

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        with open(self.__data_file, "r") as f:
            source_data = self.connect()
            key_filter = [x for x in query.keys()]
            value_filter = [x for x in query.values()]
            if not query or not value_filter:
                print("Не переданы параметры для удаления")
            else:
                res_data = []
                for i in source_data:
                    if i[key_filter[0]] == value_filter[0]:
                        continue
                    else:
                        res_data.append(i)
                return res_data

if __name__ == "__main__":
    df = Connector('df.json')

    data_for_file = [{'id': 1, 'title': 'tet'}]

    df.insert(data_for_file)
    data_from_file = df.select(dict())
    assert data_from_file == data_for_file

    df.delete({'id': 1})
    data_from_file = df.select(dict())
    assert data_from_file == []
