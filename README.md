# fxtest

fxtest -h 可以查看用法

fxtest --project project_name 创建你的测试项目

fxtest -r project_name 可以执行你的项目
备注：要确保已经安装了allure 否则只会生成普通的report 不会生成allure 报告，确保ui自动化已经安装了浏览器驱动




请先按照以下步骤安装allure 
1.打开powershell 
2.输入以下命令"Set-ExecutionPolicy RemoteSigned -scope CurrentUser"
3.然后输入 "iwr -useb get.scoop.sh | iex" (备注如果无法解析地址 可以在hosts 文件添加 199.232.68.133 raw.githubusercontent.com )
具体可以参考"https://github.com/lukesampson/scoop"
4.安装后后 输入 "scoop install allure"
allure 可以参考 "https://docs.qameta.io/allure/"
5.最后 "allure -v" 确认安装成功


关于脚本里面，所有的test 类都必须继承 fxtest.TestCase
最好在每个测试函数下面加上对这个测试的描述，以便在结果中得知该项测试的内容
比如：

def test():
  """ test login"""
  
脚本的最后都是用fxtest.main()执行
fxtest main 包括了参数 浏览器类型，执行文件，和 cmd 
cmd 等于pytest  你想添加的参数
