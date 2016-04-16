# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


class treeModel(object):
    def __init__(self, Id, value, fatherId):
        self.Id = Id
        self.value = value
        self.fatherId = fatherId

    def show(self):
        return self.value


class treeShow(object):

    logList = [treeModel(0, 'addTree', 0)]
    writtenList = [treeModel(0, 'addTree', 0)]

    def __init__(self, rootId, list):
        self.rootId = rootId
        self.list = list

    def getModelById(self, Id):
        for t in self.list:
            if t.Id == Id:
                return t
        return None

    def haveChild(self, t):
        for t1 in self.list:
            if t1.fatherId == t.Id and not self.IsInLogList(t1):
                return True
        return False

    def getFirstChild(self, t):
        for t1 in self.list:
            if t1.fatherId == t.Id and not self.IsInLogList(t1):
                return t1
        return None

    def IsInLogList(self, t):
        for t1 in self.logList:
            if t1.Id == t.Id:
                return True
        return False

    def IsInWrittenList(self, t):
        for t1 in self.writtenList:
            if t1.Id == t.Id:
                return True
        return False

    def getFatherTree(self, t):
        for t1 in self.list:
            if t1.Id == t.fatherId:
                return t1
        return None

    def show(self, startnum):
        currentTree = self.getModelById(self.rootId)
        # s = '->'
        strNum = startnum
        while(True):
            if self.haveChild(currentTree):
                if not self.IsInWrittenList(currentTree):
                    # print s * strNum, currentTree.show()
                    self.writtenList.append(currentTree)
                currentTree = self.getFirstChild(currentTree)
                strNum += 1
                continue
            else:
                if(currentTree.Id == self.rootId):
                    break
                else:
                    # if not self.IsInWrittenList(currentTree):
                    #    print s * strNum, currentTree.show()
                    self.logList.append(currentTree)
                    currentTree = self.getFatherTree(currentTree)
                    strNum -= 1
                    continue


t1 = treeModel(11, 'A-1', 9)
t2 = treeModel(12, 'B-1', 11)
t3 = treeModel(13, 'B-2', 12)
t4 = treeModel(14, 'C-1', 12)
t5 = treeModel(15, 'C-2', 12)
t6 = treeModel(16, 'C-3', 13)
t7 = treeModel(17, 'C-4', 13)
t8 = treeModel(18, 'D-1', 14)
t9 = treeModel(19, 'E-1', 18)
t10 = treeModel(20, 'E-2', 18)
t11 = treeModel(121, 'E-3', 18)
t12 = treeModel(122, 'E-4', 18)


ll = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]


ts = treeShow(11, ll)
ts.show(11)
