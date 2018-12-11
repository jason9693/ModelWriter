import pandas as pd
from tabulate import tabulate

class ModelValue:
    '''
    Model Value class contain model name and some values for during training time.
    '''
    def __init__(self, model_name: str, values: dict):
        self.model_name = model_name
        self.values = values

    def set_value(self, name, value):
        self.values[name] = value


class ModelValuesReader:
    def __init__(self, csv_path):
        self.classes = []
        self.__read_from_csv__(csv_path)
        pass

    def __read_from_csv__(self, csv_path):
        '''
        :param csv_path: path for read csv file.
        :return:
        '''
        df = pd.read_csv(csv_path, index_col=0)
        dic=df.to_dict()
        self.__dict__ = dic
        self.classes = [ModelValue(k, self.__dict__[k]) for k in self.__dict__]

    def search_model_value(self, model_name):
        try:
            return [i for i in self.classes if i.model_name == model_name][0]
        except:
            print('no value')
            return

    def get_all_model_values(self):
        '''
        :return: list of class 'ModelValue's
        '''
        return self.classes


class ModelValuesWriter:
    def __init__(self, values: list = None, io_name='mvio'):
        '''
        :param values[Optional]: list of class ModelValues
        '''
        if values is None:
            values=[]
        self.io_name = io_name
        self.model_names = [value.model_name for value in values]
        self.models_values = [value.values for value in values]

    def append(self, values: ModelValue):
        self.model_names.append(values.model_name)
        self.models_values.append((values.values))

    def to_markdown_str(self):
        df = pd.DataFrame(self.models_values, index=self.model_names).T
        md_str = tabulate(df, tablefmt="pipe", headers=self.model_names)
        return md_str

    def get_model_values(self):
        '''
        :return: list of class 'ModelValue's
        '''
        return [ModelValue(name, values) for name, values in zip(self.model_names, self.models_values)]

    def to_csv(self, csv_path):
        '''
        :param csv_path: csv path for save models.
        :return:
        '''
        df = pd.DataFrame(self.models_values, index=self.model_names).T
        df.to_csv(csv_path)

    def to_md(self, md_path):
        '''
        :param md_path: markdown path for save models to .md format
        :return:
        '''
        with open(md_path, mode='r', encoding='utf-8') as f:
            string = f.read()
            divided = string.split('[](from_{})'.format(self.io_name))

        with open(md_path, mode='w', encoding='utf-8') as f:
            string = divided[0]+\
                    '[](from_{})\n\n'.format(self.io_name)+\
                    self.to_markdown_str()+\
                    '\n[](from_{})'.format(self.io_name)
            if len(divided) > 2:
                string += divided[2]
            else:
                string += '\n'
            f.write(string)

    def reset(self):
        self.model_names = []
        self.models_values = []

if __name__ == '__main__':

    reader = ModelValuesReader('test.csv')

    mv1 = reader.search_model_value('model1')
    mv1.set_value('accuracy', 2)

    writer = ModelValuesWriter(reader.classes, io_name='d')
    writer.to_csv('test.csv')
    writer.to_md('README.md')





