from fxtest.running.config import Fxtest
from selenium.webdriver.common.by import By
from fxtest.logging import log
from time import sleep
from fxtest.webdriver import WebDriver


class TestCase(WebDriver):


    
    def AssertElementisExist(self,xpath=None,id_=None,msg=""):
        if xpath and id_ is None:
            raise NameError("元素未指定")
        if id_ is None:
            elem=Fxtest.driver.find_elements(By.XPATH,xpath)
        if xpath is None:
            elem=Fxtest.driver.find_elements(By.ID,id_)
        if xpath and id_ is not None:
            raise NameError("请选择一种定位方式 支持xpath 和id_")
        for _ in range (Fxtest.timeout):
            if len(elem) != 0:
                assert elem[0].is_displayed(),msg
            else:
                raise AssertionError(msg)

    
    def AssertHtmlText(self,text=None,msg=""):
        if text is None:
            raise NameError ("断言信息为空")
        elem=Fxtest.driver.find_element_by_tag_name("html")
        for _ in range(Fxtest.timeout):           
            try:
                assert text in elem.text,msg
            except AssertionError:
                sleep(1)

    
    def AssertElementText(self,text=None,xpath=None,msg=""):
        if xpath and id_ is None:
            raise NameError("元素未指定")
        if id_ is None:
            elem=Fxtest.driver.find_elements(By.XPATH,xpath)
        if xpath is None:
            elem=Fxtest.driver.find_elements(By.ID,id_)
        if xpath and id_ is not None:
            raise NameError("请选择一种定位方式 支持xpath 和id_")
        for _ in range (Fxtest.timeout):
            if len(elem) !=0:
                assert text in elem[0].text,msg
            else:
                raise AssertionError("元素未找到")

    def AssertElementEqualText(self,text=None,xpath=None,msg=""):
        if xpath and id_ is None:
            raise NameError("元素未指定")
        if id_ is None:
            elem=Fxtest.driver.find_elements(By.XPATH,xpath)
        if xpath is None:
            elem=Fxtest.driver.find_elements(By.ID,id_)
        if xpath and id_ is not None:
            raise NameError("请选择一种定位方式 支持xpath 和id_")
        for _ in range (Fxtest.timeout):
            if len(elem) !=0:
                assert text == elem[0].text,msg
            else:
                raise AssertionError("元素未找到")     
            
        

        