import time
import platform
import warnings
from selenium.webdriver.common.by import By
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from fxtest.logging import log
from fxtest.running.config import Fxtest
from fxtest.logging.exceptions import NotFindElementError

LOCATOR_LIST = {
    'css': By.CSS_SELECTOR,
    'id_': By.ID,
    'name': By.NAME,
    'xpath': By.XPATH,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'tag': By.TAG_NAME,
    'class_name': By.CLASS_NAME,
    "android_uiautomator": MobileBy.ANDROID_UIAUTOMATOR,
    "accessibility_id": MobileBy.ACCESSIBILITY_ID
}

def find_element(elem):
    for _ in range(Fxtest.timeout):
        elems = Fxtest.driver.find_elements(by=elem[0], value=elem[1])
        if len(elems) == 1:
            log.info(" Find element: {by}={value} ".format(
                by=elem[0], value=elem[1]))
            break
        elif len(elems) > 1:
            log.info(" Find {n} elements through: {by}={value}".format(
                n=len(elems), by=elem[0], value=elem[1]))
            break
        else:
            time.sleep(1)
    else:
        error_msg = " Find 0 elements through: {by}={value}".format(
            by=elem[0], value=elem[1])
        log.error(error_msg)
        raise NotFindElementError(error_msg)


def get_element(**kwargs):
    if not kwargs:
        raise ValueError("Please specify a locator")
    if len(kwargs) > 1:
        raise ValueError("Please specify only one locator")

    by, value = next(iter(kwargs.items()))
    try:
        LOCATOR_LIST[by]
    except KeyError:
        raise ValueError(
            "Element positioning of type '{}' is not supported. ".format(by))
    if by == "id_":
        find_element((By.ID, value))
        elem = Fxtest.driver.find_elements_by_id(value)
    elif by == "name":
        find_element((By.NAME, value))
        elem = Fxtest.driver.find_elements_by_name(value)
    elif by == "class_name":
        find_element((By.CLASS_NAME, value))
        elem = Fxtest.driver.find_elements_by_class_name(value)
    elif by == "tag":
        find_element((By.TAG_NAME, value))
        elem = Fxtest.driver.find_elements_by_tag_name(value)
    elif by == "link_text":
        find_element((By.LINK_TEXT, value))
        elem = Fxtest.driver.find_elements_by_link_text(value)
    elif by == "partial_link_text":
        find_element((By.PARTIAL_LINK_TEXT, value))
        elem = Fxtest.driver.find_elements_by_partial_link_text(value)
    elif by == "xpath":
        find_element((By.XPATH, value))
        elem = Fxtest.driver.find_elements_by_xpath(value)
    elif by == "css":
        find_element((By.CSS_SELECTOR, value))
        elem = Fxtest.driver.find_elements_by_css_selector(value)
    
    elif by == "android_uiautomator":
        find_element((MobileBy.ANDROID_UIAUTOMATOR,value))
        elem = Fxtest.driver.find_elements_by_android_uiautomator(value)
    elif by == "accessibility_id":
        find_element((MobileBy.ACCESSIBILITY_ID,value))
        elem = Fxtest.driver.find_elements_by_accessibility_id(value)
    else:
        raise NameError(
            "Please enter the correct targeting elements,'id_/name/class_name/tag/link_text/xpath/css/android_uiautomator/accessibility_id'.")

    return elem


def show_element(elem):
    """
    Show the elements of the operation
    :param elem:
    """
    style_red = 'arguments[0].style.border="2px solid #FF0000"'
    style_blue = 'arguments[0].style.border="2px solid #00FF00"'
    style_null = 'arguments[0].style.border=""'
    try:
        for _ in range(2):
            Fxtest.driver.execute_script(style_red, elem)
            time.sleep(0.1)
            Fxtest.driver.execute_script(style_blue, elem)
            time.sleep(0.1)
        Fxtest.driver.execute_script(style_blue, elem)
        time.sleep(0.3)
        Fxtest.driver.execute_script(style_null, elem)
    except Exception as e:
        log.warn(e)
        pass


class WebDriver(object):

    current_window=None

    class Key:
        def __init__(self, index=0, **kwargs):
            self.elem=get_element(**kwargs)[index]
            show_element(self.elem)
        def input(self, text=""):
            self.elem.send_keys(text)

        def enter(self):
            self.elem.send_keys(Keys.ENTER)

        def select_all(self):
            self.elem.send_keys(Keys.CONTROL, "a")

        def copy(self):
            self.elem.send_keys(Keys.CONTROL, "c")

        def cut(self):
            self.elem.send_keys(Keys.CONTROL, "x")  
        
        def paste(self):
            self.elem.send_keys(Keys.CONTROL, "v")  
    

    def get(self,url):
        """
        self.get(url)
        输入地址后，浏览器打开该地址
        """
        Fxtest.driver.get(url)

    def max_window(self):

        Fxtest.driver.maximize_window()

    def set_window(self,wide,high):
        Fxtest.driver.set_window_size(wide, high)

    def clear(self, index=0, **kwargs):

        elem=get_element(**kwargs)[index]
        show_element(elem)
        elem.clear()


    def input_text(self,text="",clear=False,index=0,enter=False,**kwargs):

        if clear is True:
            self.clear(index,**kwargs)
        elem=get_element(**kwargs)[index]
        show_element(elem)
        log.info(" input '{text}'.".format(text=text))
        elem.send_keys(text)
        if enter is True:
            elem.send_keys(Keys.ENTER)

    
    def click(self, index=0,**kwargs):
        elem=get_element(**kwargs)[index]
        show_element(elem)
        log.info(" click.")
        elem.click()

    
    def slow_click(self,index=0,**kwargs):
        elem = get_element(**kwargs)[index]
        show_element(elem)
        log.info(" click.")
        ActionChains(Fxtest.driver).move_to_element(elem).click(elem).perform()

        
    def right_click(self,index=0,**kwargs):
        elem = get_element(**kwargs)[index]
        show_element(elem)
        ActionChains(Fxtest.driver).context_click(elem).perform()  
    def move_to_element(self, index=0, **kwargs):
        """

        """
        elem = get_element(**kwargs)[index]
        show_element(elem)
        ActionChains(Fxtest.driver).move_to_element(elem).perform() 
    def double_click(self, index=0, **kwargs):
        """

        """
        elem = get_element(**kwargs)[index]
        show_element(elem)
        ActionChains(Fxtest.driver).double_click(elem).perform() 
    def close(self):
        """

        """
        Fxtest.driver.close()
    def quit(self):
        """

        """
        Fxtest.driver.quit()
    def refresh(self):
        """

        """
        Fxtest.driver.refresh()

    def execute_script(self, script, *args):
        """

        """
        return Fxtest.driver.execute_script(script, *args)
    def get_attribute(self, attribute=None, index=0, **kwargs):
        """
        """
        if attribute is None:
            raise ValueError("attribute is not None")
        elem = get_element(**kwargs)[index]
        show_element(elem)
        return elem.get_attribute(attribute)

    def get_text(self, index=0, **kwargs):
        """
 
        """
        elem = get_element(**kwargs)[index]
        show_element(elem)
        return elem.text
    def get_display(self, index=0, **kwargs):
        """

        """
        elem = get_element(**kwargs)[index]
        show_element(elem)
        return elem.is_displayed()
    


    @property
    def get_title(self):
        """

        """
        return Fxtest.driver.title

    def wait(self, time=10):
        """

        """
        Fxtest.driver.implicitly_wait(time)
    
    def switch_to_frame(self, index=0, **kwargs):
        """

        """
        elem = get_element(**kwargs)[index]
        show_element(elem)
        Fxtest.driver.switch_to.frame(elem)

    def switch_to_frame_out(self):
        """

        """
        Fxtest.driver.switch_to.default_content()
    
    @staticmethod
    def sleep(sec):
        """
        Usage:
            self.sleep(seconds)
        """
        time.sleep(sec)
    def wait_elements(self, interval=0.5,element=None ):
        """
        if element is display return True not return False
        """
        if element is None:
            raise NameError ("please input element")
        try:
            WebDriverWait(Fxtest.driver, Fxtest.timeout, interval).until(
                expected_conditions.presence_of_element_located((By.XPATH,element)))
            return True
        except Exception :
            log.error("Not Find {}".format(element))
            return False
    
    @property
    def hide_keyboard(self):
        """
        :描述 收起键盘
        """
        Fxtest.driver.hide_keyboard()
    
    @property
    def get_size(self):
        """
        :描述 获取手机屏幕分辨率
        """
        x=Fxtest.driver.get_window_size()['width']
        y=Fxtest.driver.get_window_size()['height']
        return (x,y)

    
    def swipeUp(self,swipe_time=1000):
        """
        :参数 swipe_time 滑动时间
        :描述 向上滑动
        """
        I=self.get_size
        x1=(int(I[0]*0.5))
        y1 = int(I[1] * 0.75)   
        y2 = int(I[1] * 0.25) 
        Fxtest.driver.swipe(x1, y1, x1, y2,swipe_time)
    
    def swipeDown(self,swipe_time=1000):
        """
        :参数 swipe_time 滑动时间
        :描述 向下滑动
        """
        I=self.get_size
        x1=(int(I[0]*0.5))
        y1 = int(I[1] * 0.25)   
        y2 = int(I[1] * 0.75) 
        Fxtest.driver.swipe(x1, y1, x1, y2,swipe_time)

    def swipe(self,start :tuple,end :tuple,swipe_time=1000):
        """
        :参数 start 起始坐标
        :参数 end   结束坐标
        :参数 swipe_time 滑动时间
        :描述 滑动屏幕
        """
        x1=start[0]
        y1=start[1]
        x2=end[0]
        y2=end[1]        
        Fxtest.driver.swipe(x1, y1, x2, y2,swipe_time)
    
    def press_keycode(self,code):
        """
        :描述 按下系统键
        参考:https://blog.csdn.net/crisschan/article/details/50419963
        """
        Fxtest.driver.press_keycode(code)
    
    def touch_actions(self):
        """
        def tap(self, element=None, x=None, y=None, count=1):
            模拟手指触摸屏

        def press(self, el=None, x=None, y=None):
            短按：模拟手指按住一个元素，或者坐标

        def long_press(self, el=None, x=None, y=None, duration=1000):
            长按：模拟按住一个元素，或者坐标

        def wait(self, ms=0):
            按住元素后的等待时间

        def move_to(self, el=None, x=None, y=None):
            移动手指到另外一个元素，或者坐标，注意这里坐标不是绝对坐标，是偏移量
            
        def release(self):
            释放手指

        def perform(self):
            执行前面的动作
        """
        return TouchAction(Fxtest.driver)