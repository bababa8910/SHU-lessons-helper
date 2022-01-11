# -*- coding = utf-8 -*-
# @Author:何欣泽
# @Time:2021/1/16 22:10
# @File:lessons_helper.py
# @Software:PyCharm


from selenium import webdriver
from bs4 import BeautifulSoup
import os, time


def take_lessons(driver_path, url, username, password, lesson_id, teacher_id, campus, fucy, session='1'):
    chromedriver = driver_path.strip()

    os.environ['webdriver.Chrome.driver'] = chromedriver

    driver = webdriver.Chrome(chromedriver)

    try:
        driver.get(url)
        driver.refresh()
        time.sleep(1)
        login(username, password, driver)
        title = driver.title
        if title == '上海大学本硕博一体化选课系统':

            choose_session(driver, session=session)

            choose_lesson(driver, lesson_id, teacher_id, campus, fucy)
            return 0
        else:
            time.sleep(60)
            take_lessons(driver_path, url, username, password, lesson_id, teacher_id, campus, fucy)

    except:
        time.sleep(60)
        take_lessons(driver_path, url, username, password, lesson_id, teacher_id, campus, fucy)


def login(username, password, driver):
    driver.find_element_by_id('username').click()
    driver.find_element_by_id('username').clear()
    driver.find_element_by_id('username').send_keys(username)
    time.sleep(1)
    driver.find_element_by_id('password').click()
    driver.find_element_by_id('password').clear()
    driver.find_element_by_id('password').send_keys(password)
    time.sleep(1)
    driver.find_element_by_id('submit-button').click()
    print('账号%s登录成功' % username)
    time.sleep(1)
    driver.find_element_by_tag_name('tr').click()
    time.sleep(2)
    driver.find_element_by_tag_name('button').click()


def choose_session(driver, session = '1'):
    driver.get('http://xk.autoisp.shu.edu.cn/Home/TermIndex')

    if session == '1':
        xpath_choose = '/html/body/form/div/table/tbody/tr[1]/td'
        driver.find_elements_by_xpath(xpath_choose)[0].click()

    else:
        xpath_choose = '/html/body/form/div/table/tbody/tr'
        tar_session = driver.find_elements_by_xpath(xpath_choose)
        for i in tar_session:
            if session in i.text:
                print(i.text)
                i.click()
                xpath_submit = '/html/body/form/div/button'
                tar_sub = driver.find_elements_by_xpath(xpath_submit)
                for j in tar_sub:
                    if '确' in j.text:
                        time.sleep(2)
                        j.click()
                        time.sleep(2)
                        break

def choose_lesson(driver, lesson_id, teacher_id, campus, fucy):
    start_time = time.time()
    driver.get('http://xk.autoisp.shu.edu.cn/CourseSelectionStudent/FuzzyQuery')
    time.sleep(2)
    driver.find_element_by_name('CID').send_keys(lesson_id)
    time.sleep(1)
    driver.find_element_by_name('TeachNo').send_keys(teacher_id)
    time.sleep(1)
    cout = 1
    while True:
        driver.find_element_by_id('QueryAction').click()
        time.sleep(fucy)
        source = driver.page_source
        bs_html = BeautifulSoup(source, 'html.parser')
        link = bs_html.find_all("tr")
        print('已经尝试{}次'.format(cout))
        cout += 1
        for i in link:
            if lesson_id in str(i):
                for td in list(i):
                    if campus in td:
                        index = i.index(td)
                        selected = str(list(i)[index - 2]).split('>')[-2][:-4]
                        limit = str(list(i)[index - 4]).split('>')[-2][:-4]
                        print('人数：{}    容量：{}'.format(selected, limit))

                        if limit != selected:
                            driver.find_element_by_class_name('rowchecker').click()
                            time.sleep(0.1)
                            driver.find_element_by_id('CourseCheckAction').click()
                            end_time = time.time()
                            driver.get_screenshot_as_file('./result.png')
                            print('恭喜，选课成功，共尝试%d次，共用%.3f秒钟' % (cout, (end_time - start_time)))
                            driver.quit()
                            return 0


if __name__ == '__main__':
    #################################################################################
    #                                                                               #
    #                            作者：SiliconHe                                     #
    #                                                                               #
    #                              版本：V1.1.0                                      #
    #                                                                               #
    #                           最后更新日期：2021/5/9                               #
    #                                                                               #
    #                            P.S.请连接校园网再启动                               #
    #                                                                               #
    #                                                                               #
    #################################################################################

    '''请将自己的driver地址覆盖下面的默认地址'''

    driver_path = r'./chromedriver.exe'

    lessons_url = 'http://xk.autoisp.shu.edu.cn'  # 不要动

    username = '18121939'  # 请输入自己的学号

    password = '111'  # 请输入自己的密码

    lesson_id = '0081EY03'  # 请输入想要抢的课程号

    teacher_id = '1000'  # 请输入对应的老师号

    campus = '宝山'  # 请输入校区(宝山/延长/嘉定)

    fucy = 1  # 查询时间间隔，单位秒

    session = '夏季'

    take_lessons(driver_path=driver_path, url=lessons_url, username=username,
                 password=password, lesson_id=lesson_id, teacher_id=teacher_id, campus=campus,
                 fucy=fucy, session=session)
