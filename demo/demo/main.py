# encoding:utf-8
import wx
import wx.lib.agw.customtreectrl as ct
import os


def appendDir(tree, treeID, sListDir):
    """遍历路径,将文件生成节点加入到wx的tree中
        tree wx的tree
        treeID 上级treeID
        sListDir 一个绝对路径,会自动遍历下面的子目录
    """
    # 有些目录没有权限访问的,避免其报错
    try:
        list_first_dir = os.listdir(sListDir)
        for i in list_first_dir:
            s_all_dir = sListDir + "/" + i
            # 有些目录名非法,无法生成节点,只有try一把
            try:
                childID = tree.AppendItem(treeID, i, ct_type=1)


            except:

                childID = tree.AppendItem(treeID, "非法名称")
            # 如果是目录,那么递归
            if os.path.isdir(s_all_dir):
                appendDir(tree, childID, s_all_dir)
    except:
        pass


class MyFrame(wx.Frame):
    def __init__(self, parent):

        self.checked_items = []
        wx.Frame.__init__(self, parent, -1, title="simple tree", size=(400, 500),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"请输入文件夹路径", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer2.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.text_main = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTRE)
        bSizer2.Add(self.text_main, 0, wx.ALL, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.m_button2, 0, wx.ALL, 5)


        self.custom_tree = ct.CustomTreeCtrl(self, agwStyle=wx.TR_DEFAULT_STYLE)
        self.root = self.custom_tree.AddRoot("root", ct_type=1)
        appendDir(self.custom_tree, self.root, "./test1")

        bSizer2.Add(self.custom_tree, 0, wx.ALL, 5)

        self.SetSizer(bSizer2)
        self.Layout()

        self.Centre(wx.BOTH)

        # for y in range(5):
        #     item = self.custom_tree.AppendItem(self.root, "wangjian", ct_type=1)
        self.custom_tree.ExpandAll()

        self.Bind(ct.EVT_TREE_ITEM_CHECKED, self.checked_item)
        self.m_button2.Bind(wx.EVT_BUTTON, self.main_button_click)

    def main_button_click(self, event):
        # event.Skip()
        print(self.text_main.GetValue())

    def checked_item(self, event):
        # 只要树控件中的任意一个复选框状态有变化就会响应这个函数
        if event.GetItem() == self.root:
            if self.custom_tree.IsItemChecked(event.GetItem()):
                self.custom_tree.CheckChilds(self.root)
                for item in self.get_childs(self.root):
                    self.checked_items.append(self.custom_tree.GetItemText(item))

            else:
                for item in self.get_childs(self.root):
                    self.custom_tree.CheckItem(item, False)
                    self.checked_items.remove(self.custom_tree.GetItemText(item))

        # else:
        #     if self.custom_tree.IsItemChecked(event.GetItem()):
        #         self.checked_items.append(self.custom_tree.GetItemText(event.GetItem()))
        #         print "add"
        #     else:
        #         self.checked_items.remove(self.custom_tree.GetItemText(event.GetItem()))
        #         print "remove"
        print(self.checked_items)

    def get_childs(self, item_obj):
        item_list = []
        (item, cookie) = self.custom_tree.GetFirstChild(item_obj)
        while item:
            item_list.append(item)
            print("ok")
            (item, cookie) = self.custom_tree.GetNextChild(item_obj, cookie)
        return item_list


app = wx.App()
frame = MyFrame(None)
frame.Show()
app.MainLoop()
