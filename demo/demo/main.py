# encoding:utf-8
import fnmatch
import wx
import wx.lib.agw.customtreectrl as ct
import os
import pandas as pd


def append_dir(tree, tree_id, s_list_dir):
    """遍历路径,将文件生成节点加入到wx的tree中
        tree wx的tree
        tree_id 上级tree_id
        s_list_dir 一个绝对路径,会自动遍历下面的子目录
    """

    invalid_files = [".idea", "venv", "test1.py", "Tcs.xlsx", ".gitignore"]
    # 有些目录没有权限访问的,避免其报错
    try:
        list_first_dir = os.listdir(s_list_dir)
        for i in list_first_dir:

            # print("i is ", i)
            if i not in invalid_files:
                s_all_dir = s_list_dir + "/" + i
                # print("s_all_dir  ", s_all_dir)
                # 有些目录名非法,无法生成节点,只有try一把
                try:
                    child_id = tree.AppendItem(tree_id, i, ct_type=1)

                except:

                    child_id = tree.AppendItem(tree_id, "非法名称")
                # 如果是目录,那么递归
                if os.path.isdir(s_all_dir):
                    append_dir(tree, child_id, s_all_dir)
    except:
        pass


class MyFrame(wx.Frame):
    def __init__(self, parent):

        # self.checked_items = []
        self.item_list = []
        self.input_path = None
        self.times = 0
        self.times1 = 0

        wx.Frame.__init__(self, parent, -1, title="simple tree", size=(400, 500),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        # v_box = wx.BoxSizer(wx.VERTICAL)
        v_box1 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"请输入文件夹绝对路径", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        v_box1.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.text_main1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=(200, 30),
                                      style=wx.TE_CENTRE)
        v_box1.Add(self.text_main1, 0, wx.ALL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button1.Bind(wx.EVT_BUTTON, self.main_button_click)
        v_box1.Add(self.m_button1, 0, wx.ALL, 5)

        v_box1.Add((-1, 20))

        self.custom_tree = ct.CustomTreeCtrl(self, agwStyle=wx.TR_DEFAULT_STYLE)
        # self.times += 1
        self.Bind(ct.EVT_TREE_ITEM_CHECKED, self.checked_item)
        # print("times ", self.times)
        # v_box1.Add(h_box1, 0, wx.ALL, 5
        v_box1.Add(self.custom_tree, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)

        v_box1.Add((-1, 15))

        h_box1 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"请输入loop times", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        h_box1.Add(self.m_staticText2, flag=wx.RIGHT, border=8)

        self.text_main2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                      style=wx.TE_CENTRE)
        h_box1.Add(self.text_main2, proportion=1)

        v_box1.Add(h_box1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        v_box1.Add((-1, 15))
        h_box2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"添加到xmls文件中", wx.DefaultPosition, size=(150, 30))
        self.m_button2.Bind(wx.EVT_BUTTON, self.add_button_file)
        h_box2.Add(self.m_button2)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"执行自动化测试TcsRunner", wx.DefaultPosition, size=(200, 30))
        self.m_button3.Bind(wx.EVT_BUTTON, self.run_test)
        h_box2.Add(self.m_button3, flag=wx.LEFT | wx.BOTTOM, border=5)

        v_box1.Add(h_box2, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=20)
        v_box1.Add((-1, 15))

        self.SetSizer(v_box1)
        self.Layout()

        self.Centre(wx.BOTH)

    def run_test(self, event):
        print("run_test")
        current_path = os.path.abspath(os.path.dirname(__file__))
        print("当前路径", current_path)
        cmd1 = "cd" + " " + current_path
        os.system(cmd1)
        cmd2 = "python test1.py"
        os.system(cmd2)

    def add_button_file(self, event):
        print("add_button_file")
        print("当前loop times ", self.text_main2.GetValue())
        print("当前要添加的文件为 ", self.item_list)

        file_name = "./Tcs.xlsx"
        df = pd.read_excel(file_name, usecols=[0], sheet_name='Sheet1')
        df_li = df.values.tolist()

        list_name_existed = []
        for s_li in df_li:
            list_name_existed.append(s_li[0])
        print("list_name_existed  first read ", list_name_existed)

        # add_list = []
        new_item_list = []
        for item in self.item_list:
            new_item_list.append(item.split(".")[0])

        for n in new_item_list:
            if n not in list_name_existed:
                list_name_existed.append(n)
        print("list_name_existed   ", list_name_existed)

        # print("add_list   ", add_list)
        loop_times = [self.text_main2.GetValue() for i in range(len(list_name_existed))]

        columns = ['Name', 'Loop times']
        writer = pd.ExcelWriter(file_name)
        df1 = pd.DataFrame(data={'Name': list_name_existed, 'Loop times': loop_times})
        df1.to_excel(writer, 'Sheet1', index=False, encoding='utf-8-sig', columns=columns)
        writer.save()

        # list_loop_existed = pd.read_excel(file_name, sheetname=None)
        column1_name = "Name"
        column2_name = "Loop Times"
        # print(list_existed['Sheet1'].(loop times))
        # print(list_existed['Sheet1'].column2_name)
        # print("list_name_existed ", list_name_existed)
        # print("list_loop_existed ", list_loop_existed)

        if self.text_main2.GetValue() and self.item_list:
            wx.CallLater(3000, self.ShowMessage)

            self.SetTitle('Message box')

    def ShowMessage(self):
        wx.MessageBox('添加成功', 'Info',
                      wx.OK | wx.ICON_INFORMATION)

    def main_button_click(self, event):
        # event.Skip()
        # print("当前路径", os.path.abspath(os.path.dirname(__file__)))
        print("当前文件夹", self.text_main1.GetValue())
        self.input_path = self.text_main1.GetValue()
        if os.path.isdir(self.input_path):
            root_name = self.input_path.split("\\")[-1]
            self.root = self.custom_tree.AddRoot(root_name, ct_type=1)
            print("self.root ", self.root)
            append_dir(self.custom_tree, self.root, self.input_path)
            self.custom_tree.ExpandAll()

    def add_all_childs(self, item_obj):

        # print("item_obj", item_obj)
        # (item, cookie) = self.custom_tree.GetFirstChild(item_obj)
        # print("item, cookie", (item, cookie))
        file_patterns = "*.py"
        # print(" item name in childs",self.custom_tree.GetItemText(item_obj))
        # print(" GetSelection ", self.custom_tree.GetSelection())
        # print(" self.custom_tree.ItemHasChildren(item_obj) ", self.custom_tree.ItemHasChildren(item_obj))
        # print(" GetChildrenCount() ", self.custom_tree.GetChildrenCount(item_obj, recursively=True))

        # print(" GetChildrenCount() ", self.custom_tree.GetChildren(item_obj, recursively=True)[0])
        print(len(item_obj.GetChildren()))
        for i in item_obj.GetChildren():
            print(" current file is  ", self.custom_tree.GetItemText(i))
            # print("times ", self.times)
            # self.times += 1
            if fnmatch.fnmatch(self.custom_tree.GetItemText(i), file_patterns) and (
                    self.custom_tree.GetItemText(i) not in self.item_list):
                self.item_list.append(self.custom_tree.GetItemText(i))
            else:
                self.add_all_childs(i)
        # #
        #     else:
        #         item = self.custom_tree.GetNextActiveItem(item_obj, down=True)
        #         self.get_childs(item_obj)
        #         # (item, cookie) = self.custom_tree.GetNextChild(item_obj, cookie)
        # while item:
        #     item_list.append(item)
        #     # print("ok")
        #     (item, cookie) = self.custom_tree.GetNextChild(item_obj, cookie)
        #     print("item in loop is ", self.custom_tree.GetItemText(item))

        print("item_list ", self.item_list)

    def delete_all_childs(self, item_obj):
        # print("item_obj", item_obj)

        file_patterns = "*.py"
        print(item_obj.GetChildren())
        try:
            for i in item_obj.GetChildren():
                self.custom_tree.CheckItem(i, False)
                if fnmatch.fnmatch(self.custom_tree.GetItemText(i), file_patterns) and (
                        self.custom_tree.GetItemText(i) in self.item_list):
                    # print("current delete file in all childs is ", self.custom_tree.GetItemText(i))
                    self.item_list.remove(self.custom_tree.GetItemText(i))
                    # print("item_list ", self.item_list)
                else:
                    self.delete_all_childs(i)
        except:
            pass

        # print("item_list ", self.item_list)

    def add_childs(self, item_obj):

        # print("item_obj", item_obj)
        file_patterns = "*.py"
        # self.custom_tree.CheckChilds(event.GetItem())
        print(item_obj.GetChildren())
        if item_obj.GetChildren():
            self.add_all_childs(item_obj)
        else:
            self.custom_tree.CheckChilds(item_obj)
            self.item_list.append(self.custom_tree.GetItemText(item_obj))
        print("item_list ", self.item_list)

    def delete_childs(self, item_obj):
        # print("item_obj", item_obj)
        # print("times1 ", self.times1)

        file_patterns = "*.py"
        # print(item_obj.GetChildren())
        if item_obj.GetChildren():
            self.delete_all_childs(item_obj)
        else:
            try:
                self.custom_tree.CheckItem(item_obj, False)
                # print("current delete file in childs is ",self.custom_tree.GetItemText(item_obj))

                self.item_list.remove(self.custom_tree.GetItemText(item_obj))

            except:
                pass

        # print("item_list ", self.item_list)

    def checked_item(self, event):
        # 只要树控件中的任意一个复选框状态有变化就会响应这个函数
        file_patterns = "*.py"
        # print("event.GetItem() ", event.GetItem())
        # print("self.custom_tree.GetItemText(event.GetItem()) ", self.custom_tree.GetItemText(event.GetItem()))
        # file_path = self.input_path.split("\\")[:-1]
        # print("file_path ", file_path)
        # temp = file_path + "\\" + self.custom_tree.GetItemText(event.GetItem())
        print("times ", self.times)
        # print("times1 ", self.times1)
        # print("temp ", temp)

        if self.custom_tree.IsItemChecked(event.GetItem()):
            # print("self.custom_tree.GetItemText(event.GetItem()) is ", self.custom_tree.GetItemText(event.GetItem()))
            # if fnmatch.fnmatch(self.custom_tree.GetItemText(event.GetItem()), file_patterns):
            # self.checked_items.append(self.custom_tree.GetItemText(event.GetItem()))
            self.custom_tree.CheckChilds(event.GetItem())
            self.add_childs(event.GetItem())
            print("add child")
        else:

            # self.checked_items.remove(self.custom_tree.GetItemText(event.GetItem()))
            self.delete_childs(event.GetItem())
            print("remove child ")
        self.times += 1
        '''
        ##如果当前选中的为root节点
        if event.GetItem() == self.root:
            if self.custom_tree.IsItemChecked(event.GetItem()):
                self.custom_tree.CheckChilds(event.GetItem())

                # self.times += 1
                # print("times ", self.times)
                self.add_all_childs(event.GetItem())
                print("add all")
                    # self.checked_items.append(self.custom_tree.GetItemText(item))
            else:

                self.delete_all_childs(event.GetItem())
                    # self.checked_items.remove(self.custom_tree.GetItemText(item))
                print("remove all ")


        ###如果选中的不是root节点
        else:

            if self.custom_tree.IsItemChecked(event.GetItem()):
                # print("self.custom_tree.GetItemText(event.GetItem()) is ", self.custom_tree.GetItemText(event.GetItem()))
                # if fnmatch.fnmatch(self.custom_tree.GetItemText(event.GetItem()), file_patterns):
                # self.checked_items.append(self.custom_tree.GetItemText(event.GetItem()))
                self.custom_tree.CheckChilds(event.GetItem())
                self.add_childs(event.GetItem())
                print("add child")
            else:

                # self.checked_items.remove(self.custom_tree.GetItemText(event.GetItem()))
                self.delete_childs(event.GetItem())
                print("remove child ")
        '''
        # print(self.checked_items)

        # print("last item_list ", self.item_list)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()
