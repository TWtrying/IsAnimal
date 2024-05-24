# -*- coding:utf-8 -*-

'''
本程序为推理机程序，不包含规则库
规则库格式为:
animal:最终的推理结果
rule:推理过程
[animal|rule]:feature[^feature]-result
For example:
    animal:信天翁
    rule:鸟类^善于飞-信天翁
'''



def RuleFileLoader(rulefilepath='./AI/config'):
    '''
    规则库解析器
    参数:
        rulefilepath:str ,规则库的路径,默认在'./AI/config'
    返回:
        res:list ,字典数组,{'animal':[ ],'rule':[ ]}
    '''

    #定义文件描述符
    ruleloader = None

    #定义返回字典格式
    resdata = {
        'animal':[],
        'rule':[]
    }

    #尝试打开规则库文件
    try:
        ruleloader = open(file=rulefilepath ,mode='r' ,encoding='UTF-8')
    except:
        print(">>>Error:文件读取失败,程序退出")
        exit()

    #解析规则库文件
    for ruleitem in ruleloader.readlines():
        #逐行解析,当前行:ruleitem

        #解析规则类型
        ruletype = ruleitem.split(':')

        #保存规则递推结果
        if ruletype[0] == 'animal':
            resdata['animal'].append(ruletype[1].replace('\n',''))
            continue

        #解析特征规则
        elif ruletype[0] == 'rule':
            #分离结果与特征
            resultandfeature = ruletype[1].split('-')
            resultandfeature[1] = resultandfeature[1].replace('\n','')
            resdata['rule'].append({resultandfeature[1].replace('\n',''):resultandfeature[0].split('^')})
            continue
        #防止空白行干扰
        else:
            continue
    return resdata

class ToAnimal:
    '''
    识别动物类封装
    '''
    #推理结果
    InferenceResult:str = ''
    #用户描述
    CurrentFeature:list = []

    #推理规则及结果
    AnimalRule:list = []
    AnimalName:list = []

    def __init__(self ,rule:dict ,feature:list=[]) -> None:
        '''
        构造函数
        参数:
            rule:list ,规则库{'animal':[ ],'rule':[ ]}
            feature:list ,当前特征数组
        '''
        
        print('**********  初始化程序  **********')
        self.AnimalName = rule['animal']
        self.AnimalRule = rule['rule']
        print('**********导入规则库成功**********')
        self.CurrentFeature = feature

    def AddFeature(self,addlist):
        '''
        增加特征至当前特征
        参数:
            addlist:list ,特征数组
        '''
        self.CurrentFeature = self.CurrentFeature + addlist
        print('>>>添加特征:',addlist)
        return
    
    def InputFeature(self) ->bool:
        '''
        获取用户输入的特征
        '''
        print('********** 请以空格分隔 **********')
        print('>>>请输入特征:',end='')
        Max = 3
        while Max != 0:
            Max = Max - 1
            tempinput = input()
            if tempinput == '':
                print('>>>输入为空,请重新输入特征:',end='')
                continue
            try:
                tempfeature = tempinput.split(' ')
                if len(tempinput) < 1:
                    print('>>>输入有误,请重新输入特征:',end='')
                    raise
                self.AddFeature(tempfeature)
                return
            except:
                pass
        print('\n>>>输入错误三次,程序退出!')
        exit()

    def CheakPoint(self) ->bool:
        '''
        检查点函数
        参数:
            无
        返回:
            res:bool, 推理成功则返回True,反之False
        '''

        #循环次数,两次即可全部推理一次
        Max = 2
        while(Max != 0):
            Max = Max-1

            #遍历规则库中的规则
            for rule in self.AnimalRule:
                flag = True
                
                #与当前特征对比,若都符合则向当前特征数组中加入该段的推理结果
                for i in list(rule.values())[0]:
                    if i in self.CurrentFeature:
                        continue
                    else:
                        flag = False
                        break
                #若特征均符合 并且 当前特征数组中无将要加入的特征,则进行加入操作
                if flag and list(rule.keys())[0] not in self.CurrentFeature:
                    self.AddFeature([list(rule.keys())[0]])

            #遍历结果数组，查询是否有推理成功的特征
            for i in self.AnimalName:
                if i in self.CurrentFeature:
                    Max = 0
                    self.InferenceResult = i
                    return True
        return False

    def Run(self):
        while True:
            self.InputFeature()
            if self.CheakPoint():
                print('>>>推理成功:',self.InferenceResult)
                return
            else:
                print('>>>特征不足,请补充')
                continue


# UserDescription = ['善于飞', '产奶','反刍','会游泳','黑白二色','不会飞']
#会飞 会下蛋 有羽毛 长脖 长腿 会游泳 黑白二色 善于飞


toanimal = ToAnimal(RuleFileLoader('./AI/rule'))
toanimal.Run()