# encoding:utf-8
import fnmatch

import wx
import wx.lib.agw.customtreectrl as ct
import os


def append_dir(tree, tree_id, s_list_dir):
    """遍历路径,将文件生成节点加入到wx的tree中
        tree wx的tree
        tree_id 上级tree_id
        s_list_dir 一个绝对路径,会自动遍历下面的子目录
    """

    invalid_files = [".idea", "venv", "test1.py", "Tcs.xlsx"]
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

        self.checked_items = []
        self.input_path = None

        wx.Frame.__init__(self, parent, -1, title="simple tree", size=(400, 500),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        # v_box = wx.BoxSizer(wx.VERTICAL)
        v_box1 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"请输入文件夹绝对路径", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        v_box1.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.text_main1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=(200, 30), style=wx.TE_CENTRE)
        v_box1.Add(self.text_main1, 0, wx.ALL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_button1.Bind(wx.EVT_BUTTON, self.main_button_click)
        v_box1.Add(self.m_button1, 0, wx.ALL, 5)

        v_box1.Add((-1, 20))

        self.custom_tree = ct.CustomTreeCtrl(self, agwStyle=wx.TR_DEFAULT_STYLE)
        self.Bind(ct.EVT_TREE_ITEM_CHECKED, self.checked_item)
        # v_box1.Add(h_box1, 0, wx.ALL, 5
        v_box1.Add(self.custom_tree, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)

        v_box1.Add((-1, 15))

        h_box1 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"请输入loop times", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        h_box1.Add(self.m_staticText2,flag=wx.RIGHT, border=8)

        self.text_main2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,  wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTRE)
        h_box1.Add(self.text_main2, proportion=1)

        v_box1.Add(h_box1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        v_box1.Add((-1, 15))
        h_box2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"添加到xmls文件中", wx.DefaultPosition, size=(150, 30))
        self.m_button2.Bind(wx.EVT_BUTTON, self.add_button_file)
        h_box2.Add(self.m_button2)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"执行自动化测试TcsRunner", wx.DefaultPosition, size=(200, 30))
        self.m_button3.Bind(wx.EVT_BUTTON, self.run_test)
        h_box2.Add(self.m_button3, flag=wx.LEFT|wx.BOTTOM, border=5)

        v_box1.Add(h_box2, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=20)
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
        print("当前文件夹", self.text_main2.GetValue())
        print("当前要添加的文件为 ", self.checked_items)

    def main_button_click(self, event):
        # event.Skip()
        # print("当前路径", os.path.abspath(os.path.dirname(__file__)))
        print("当前文件夹", self.text_main1.GetValue())
        self.input_path = self.text_main1.GetValue()
        if os.path.isdir(self.input_path):
            self.root = self.custom_tree.AddRoot(self.input_path.split("\\")[-1], ct_type=1)
            append_dir(self.custom_tree, self.root, self.input_path)
            self.custom_tree.ExpandAll()

    def checked_item(self, event):
        # 只要树控件中的任意一个复选框状态有变化就会响应这个函数
        file_patterns = "*.py"
        if event.GetItem() == self.root:
            if self.custom_tree.IsItemChecked(event.GetItem()):
                self.custom_tree.CheckChilds(self.root)
                for item in self.get_childs(self.root):
                    # print("item is ", item)
                    # print("self.custom_tree.GetItemText(item) is ",self.custom_tree.GetItemText(item))
                    if fnmatch.fnmatch(self.custom_tree.GetItemText(item), file_patterns):
                        self.checked_items.append(self.custom_tree.GetItemText(item))
                        print("add all")
            else:
                for item in self.get_childs(self.root):
                    self.custom_tree.CheckItem(item, False)
                    self.checked_items.remove(self.custom_tree.GetItemText(item))
                    print("remove all ")
        else:
            if self.custom_tree.IsItemChecked(event.GetItem()):
                # print("self.custom_tree.GetItemText(event.GetItem()) is ", self.custom_tree.GetItemText(event.GetItem()))
                if fnmatch.fnmatch(self.custom_tree.GetItemText(event.GetItem()), file_patterns):
                    self.checked_items.append(self.custom_tree.GetItemText(event.GetItem()))
                    print("add child")
            else:
                self.checked_items.remove(self.custom_tree.GetItemText(event.GetItem()))
                print("remove child ")
        print(self.checked_items)

    def get_childs(self, item_obj):
        item_list = []
        (item, cookie) = self.custom_tree.GetFirstChild(item_obj)
        while item:
            item_list.append(item)
            # print("ok")
            (item, cookie) = self.custom_tree.GetNextChild(item_obj, cookie)
        return item_list

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()
