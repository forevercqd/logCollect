# coding: utf-8
import pandas as pd
import numpy as np
import os


class Analysis(object):
    def __init__(self, xls_path):
        self.df = pd.read_excel(xls_path)
        """
        self.add_index = ['gap_cqd.3', 'gap_cqd.4', 'dur_cqd.3_4', 'gap_cqd.5.1', 'gap_cqd.5.4', 'dur_cqd.4_5.1','dur_cqd_3_1']
        gap_cqd.3 :  表示前后相邻两帧, cqd.3 位置处的时间戳的差值, 表示 RenderEngine 接收数据的时间间隔;
        gap_cqd.4 :  表示前后相邻两帧, cqd.4 位置处的时间戳的差值，表示 RenderEngine 发送数据的时间间隔;
        dur_cqd.3_4: 表示同一帧 cqd.4 - cqd.3， 表示 RenderEngine 接收一帧到 发送渲染后帧至Encoder 的时间间隔;
        gap_cqd.5.1：表示 “当前帧 Encoder 成功输出一帧对应送入数据的时间戳” 减去 “上一帧第一次遍历输入帧的时间戳” 的差值;
        gar_cqd.5.4: 表示 Encoder 编码器吐出前后两帧数据的时间间隔;
        dur_cqd.4_5.1: “当前帧第一次接收到 RenderEngine 发送过来的数据的时间戳” 减去 “RenderEngine 发送时间的时间戳”, 表示 RenderEninge 发送的待编码帧在消息队列中耗费的时间;
        
        
        """
        self.add_index = ['gap_cqd.3', 'gap_cqd.4', 'dur_cqd.3_4', 'gap_cqd.5.1', 'gap_cqd.5.4', 'dur_cqd.4_5','dur_cqd_3_1']

        self.case_dict_keys = ['cqd_3', 'cqd_4', 'cqd_5_1_first', 'cqd_5_1_last', 'cqd_5_4','cqd_1']
        # self.case_dict_keys = []

        self.first_index = 'pts'

        # list 乘标量表示将list 扩展;
        self.add_df = pd.DataFrame([[np.nan] * len(self.add_index)] * len(self.df), columns=self.add_index) # 根据源 excel 文件的行数，及要添加的列数，分配空间;

    @staticmethod
    def add_parameters(params, **kwargs):
        params.update(kwargs)

    @property
    def df_index(self):
        """
        取出所有的列索引为 pts 的列的所有内容 ,并去除重复值;
        :return:    pts 列表;
        """
        return self.df[self.first_index].drop_duplicates()

    def _case_generator(self):
        """
        生成器: 取出源 excel 文件中 pts 等于 某pts 对应的所有的行;
        :return:
        """
        for ind in self.df_index:
            yield self.df[self.df[self.first_index] == ind]

    @staticmethod
    def _get_cqd_first(case_df, index):
        """
        取出 case_df 表格中"第0行,index 列"的值;
        :param case_df: 某相同pts 的各行组成的表格;
        :param index:   列号
        :return:        返回 case_df 表格中"第0行,index 列"的值;
        """
        return case_df.loc[case_df.index[0], index] # 取出 case_df 第0行, 列号为 index 的单元的值;

    @staticmethod
    def _get_cqd_last(case_df, index):
        return case_df.loc[case_df.index[-1], index]

    @staticmethod
    def _get_last_index(case_df):
        return case_df.index[-1]

    def _gen_case_dict_key_single(self, func, index):
        base_key = index.replace('.', '_')
        key = '{}_{}'.format(self._dtype(func), base_key)
        return key

    def _dtype(self, func):
        if func == self._get_cqd_first:
            return 0
        elif func == self._get_cqd_last:
            return 1
        else:
            raise ValueError("Input must be self._get_cqd_first or self._get_cqd_last.")

    def _get_func_from_dtype(self, dtype):
        if dtype == 0:
            return self._get_cqd_first
        elif dtype == 1:
            return self._get_cqd_last
        else:
            raise ValueError("Input must be 0 or 1.")

    def _gen_case_dict_keys(self):
        func_index_list = [['CQD.3', self._get_cqd_first], ['CQD.4', self._get_cqd_first],
                           ['CQD.5.1', self._get_cqd_first], ['CQD.5.1', self._get_cqd_last],
                           ['CQD.5.4', self._get_cqd_last]]
        for index, func in func_index_list:
            key = self._gen_case_dict_key_single(func, index)
            assert key not in self.case_dict_keys
            self.case_dict_keys.append(key)

    def _get_case_dict(self, case_df):
        case_dict = dict()
        # assert self.case_dict_keys
        # for key in self.case_dict_keys:
        #     case_dict[key] = func(case_df, index)

        # index = 'CQD.3'
        # key = self._gen_case_dict_keys(0, index)
        # assert key not in self.case_dict_keys
        # self.case_dict_keys.append(key)
        # case_dict[key] = self._get_cqd_first(case_df, index)
        #
        # index = 'CQD.4'
        # key = self._gen_case_dict_keys(0, index)
        # assert key not in self.case_dict_keys
        # self.case_dict_keys.append(key)
        # case_dict[key] = self._get_cqd_first(case_df, index)
        #
        # index = 'CQD.5.1'
        # key = self._gen_case_dict_keys(0, index)
        # assert key not in self.case_dict_keys
        # self.case_dict_keys.append(key)
        # case_dict[key] = self._get_cqd_first(case_df, index)
        #
        # index = 'CQD.5.1'
        # key = self._gen_case_dict_keys(1, index)
        # assert key not in self.case_dict_keys
        # self.case_dict_keys.append(key)
        # case_dict[key] = self._get_cqd_last(case_df, index)
        #
        # index = 'CQD.5.4'
        # key = self._gen_case_dict_keys(1, index)
        # assert key not in self.case_dict_keys
        # self.case_dict_keys.append(key)
        # case_dict[self._gen_case_dict_keys(1, index)] = self._get_cqd_last(case_df, index)

        # cqd.note.2 此处添加 CQD.1, CQD.2,CQD.6,CQD.7 相关的内容;

        case_dict[self.case_dict_keys[0]] = self._get_cqd_first(case_df, 'CQD.3')
        case_dict[self.case_dict_keys[1]] = self._get_cqd_first(case_df, 'CQD.4')
        case_dict[self.case_dict_keys[2]] = self._get_cqd_first(case_df, 'CQD.5.1')
        case_dict[self.case_dict_keys[3]] = self._get_cqd_last(case_df, 'CQD.5.1')
        case_dict[self.case_dict_keys[4]] = self._get_cqd_last(case_df, 'CQD.5.4')
        case_dict[self.case_dict_keys[5]] = self._get_cqd_first(case_df, 'CQD.1')
        return case_dict

    @staticmethod
    def _diff(case_dict_pre, case_dict_current, index_pre, index_current, dtype_func):
        if np.isnan(case_dict_pre[index_pre]) or np.isnan(case_dict_current[index_current]):
            return np.nan
        else:
            return dtype_func(case_dict_current[index_current]) - dtype_func(case_dict_pre[index_pre])

    def _diff_items(self, case_dict_pre, case_dict_current):
  #      dur_3_1 = ;    # cqd.note.1 此处添加 关于 cqd.3 - cqd.1 的值, 同时添加至新增列中;
        diff_cqd_3 = self._diff(case_dict_pre, case_dict_current, self.case_dict_keys[0], self.case_dict_keys[0], int)
        diff_cqd_4 = self._diff(case_dict_pre, case_dict_current, self.case_dict_keys[1], self.case_dict_keys[1], int)
        diff_cqd_5_1 = self._diff(case_dict_pre, case_dict_current, self.case_dict_keys[2], self.case_dict_keys[3], int)
        diff_cqd_5_4 = self._diff(case_dict_pre, case_dict_current, self.case_dict_keys[4], self.case_dict_keys[4], int)
        dur_4_3 = self._diff(case_dict_current, case_dict_current, self.case_dict_keys[0], self.case_dict_keys[1], int)
        dur_51_4 = self._diff(case_dict_current, case_dict_current, self.case_dict_keys[1], self.case_dict_keys[2], int)


        dur_3_1 = self._diff(case_dict_current, case_dict_current, self.case_dict_keys[5], self.case_dict_keys[0], int)

        diff_list = [diff_cqd_3, diff_cqd_4, dur_4_3, diff_cqd_5_1, diff_cqd_5_4, dur_51_4, dur_3_1]
        assert len(diff_list) == len(self.add_index)
        return diff_list

    def _get_adding_colums(self):   # 将要计算的结果存于 self.add_df 中;
        for index, case_df in enumerate(self._case_generator()):    # 每次取出源表格中某个相同的 pts 的所有行;最终会遍历所有的不同的pts的行;
            if index == 0:
                continue
            if index == 1:
                case_dict_pre = self._get_case_dict(case_df) # case_df 存储的是 pts 值相同的所有行构成的表格;
                continue
            case_dict_current = self._get_case_dict(case_df)
            diff_list = self._diff_items(case_dict_pre, case_dict_current)
            self.add_df.loc[self._get_last_index(case_df)] = diff_list
            case_dict_pre = case_dict_current

    def add_columns(self):
        self._get_adding_colums()
        df = pd.concat([self.df, self.add_df], axis=1)  # axis=1 列合并(行索引相同的行合成一行;)
        return df


def test():
    xls_path = '/Users/robert/Documents/doc/problemData/19_export_picture_to_video/21_grep_cqd.xls'
    out_path = os.path.join(os.path.dirname(xls_path), os.path.basename(xls_path).split('.')[0] + '_add_dff_copy.xls')
    analysis = Analysis(xls_path)
    out_df = analysis.add_columns()
    out_df.to_excel(out_path, header=True, index=False)


if __name__ == '__main__':
    test()