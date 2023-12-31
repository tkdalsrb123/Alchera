from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup as bs4

from datetime import datetime, date

from time import sleep

import pandas as pd


def filter_by_condition(rows):
    result = []
    for row in rows:
        location_condition = row.find_element_by_css_selector("p.work_place").text
        career_condition = row.find_element_by_css_selector(".career").text
        deadline = row.find_element_by_css_selector('.deadlines').text
        url = row.find_element_by_css_selector(
            '.str_tit').get_attribute('href')

        try:
            if is_deadline_over_ten_days(deadline) \
                    and "대전" in location_condition \
                    and ("신입" in career_condition or "경력무관" in career_condition):
                print("=====FILTERED ROW=====")
                print("LOCATION CONDITION", location_condition)
                print("CAREER CONDITION", career_condition)
                print("DEADLINE CONDITIOn", deadline)
                print("=====END FILTERED=====")
                result.append(url)
            else:
                print("=====UNFILTERED ROW=====")
                print("LOCATION CONDITION", location_condition)
                print("CAREER CONDITION", career_condition)
                print("DEADLINE CONDITIOn", deadline)
                print("=====END UNFILTERED=====")
        except:
            print("UNFILTERED DEADLINE ROW", deadline)

    return result


def is_deadline_over_ten_days(deadline):
    today = date.today()
    iso_format = get_deadline_for_iso(deadline)
    deadline_date = date.fromisoformat(iso_format)
    deadline = (deadline_date - today).days
    return deadline >= 10


def get_deadline_for_iso(deadline):
    iso_format = [str(date.today().year)]
    a = deadline.split(" ")
    b = a[1].split("(")
    c = b[0].split("/")
    d = iso_format + c
    return "-".join(d)


def get_column_value(soup, selector, parser_function):
    try:
        value = parser_function(soup, selector)
        return value
    except:
        return ""


def default_parser(soup, selector):
    return soup.select(selector)[0].text.strip()


def replace_wrap_parser(soup, selector):
    target = soup.select(selector)[0]
    result = target.text
    if target.select(".toolTipWrap"):
        result = result.replace(target.select(".toolTipWrap")[0].text, "")

    return result.strip()


def deadline_parser(soup, selector):
    deadline = soup.select(selector)[0].text  # YYYY.MM.DD tt:mm
    return deadline.split(" ")[0]  # YYYY.MM.DD


def href_parser(soup, selector):
    return soup.select(selector)[0].attrs["href"]


def benefit_parser(soup, selector):
    # 버튼이 있는지 없는지 살펴보기
    # 있으면 버튼 클릭하기
    # option: 복리후생이 있는 곳 까지 스크롤 내리기
    # row가져오고 col 단위로 접근하기
    result = []

    parent = soup.select(selector)[0]
    button = parent.find('button')
    if button is not None:
        driver.find_element_by_css_selector('.jv_benefit > div.cont > button').click()

    columns = parent.select('.col')
    for column in columns[:-2]:
        title = column.dt.text
        value = column.dd.text.strip()

        result.append(title)
        result.append(value)
        result.append("\n")

    return "\n".join(result)


def get_next_page_url(base_url, page):
    url = base_url.split("?")
    url[1] = f"page={page}&" + url[1]
    return "?".join(url)


with webdriver.Chrome("./chromedriver") as driver:
    wait = WebDriverWait(driver, 10)

    company_name_list = []
    content_list = []
    aa_list = []
    recruitment_number_list = []
    task_list = []
    work_location_list = []
    url_list = []
    deadline_list = []
    imployee_list = []
    sales_list = []
    gender_list = []
    find_who_list = []
    income_list = []
    work_time_list = []
    benefit_list = []
    resume_format_list = []

    print("*" * 35)
    print("*" + " " * 33 + "*")
    print("*     한남대학교 취업전략개발팀   *")
    print("* 근로장학생 업무 자동화 프로젝트 *")
    print("*      사람인 채용공고 크롤러     *")
    print("*" + " " * 33 + "*")
    print("*********CREATED BY PRAYME*********")

    print()
    print()
    print()
    print(">> 데이터를 수집할 URL을 입력해주세요 ")
    target_url = input("<< ").strip()

    driver.get(target_url)
    print(">> 수집을 시작합니다....")

    rows = driver.find_elements_by_css_selector("#default_list_wrap > section > div.list_body > .list_item")
    print(">> 대전 지역, 10일 이상, 신입 조건 채용공고 필터링 시작....")
    rows = filter_by_condition(rows)

    page = 1
    while len(rows) <= 40:
        page += 1
        next_page = get_next_page_url(target_url, page)
        driver.get(next_page)
        elements = driver.find_elements_by_css_selector("#default_list_wrap > section > div.list_body > .list_item")
        rows += filter_by_condition(elements)
        rows = set(rows)
        rows = list(rows)

    print(">> 필터링 완료. 총 {}개의 채용공고 수집을 시작합니다....".format(len(rows)))

    for i, row in enumerate(rows):
        print(">> {}/{}번째 채용공고 수집 시작".format(i, len(rows)))
        # print("ROW", row)
        # row에서 해결할 수 있는 것들

        # 아이템 페이지로 이동하기
        driver.get(row)

        # DOM 로딩 기다리기
        # wait.until(presence_of_element_located(
        #     (By.CSS_SELECTOR, ".info_period > dd:nth-child(4)")
        # ))
        sleep(5)

        # HTML 얻기
        html = driver.page_source
        soup = bs4(html, 'html.parser')

        # # 각 아이템의 회사 이름 가져오기
        company_name = get_column_value(soup, ".company_name", default_parser)
        print("COMPANY NAME", company_name)

        ############# 여기까지 완료 #################

        # # # 각 아이템의 근무 주소 가져오기
        work_location = get_column_value(
            soup, "#map_0 > div > address > span", default_parser)
        print("WORK LOCATION", work_location)

        # # # 각 아이템의 이력서 제출 형식 가져오기
        # resume_submission_format = get_column_value(
        #     soup, '.template', default_parser)
        resume_submission_format = get_column_value(
            soup, '.template', replace_wrap_parser)
        print("RESUME SUBMISSION FORMAT", resume_submission_format)

        # # 각 아이템의 모집 마감 날짜 가져오기
        deadline = get_column_value(
            soup, '.info_period > dd:nth-child(4)', deadline_parser)
        print("DEADLINE", deadline)

        # # # 각 아이템의 복리후생 가져오기
        benefit = get_column_value(soup, '.jv_benefit', benefit_parser)
        print("BENEFIT", benefit)

        income = ""
        work_time = ""
        find_who = ""
        try:
            cont = soup.select(".cont")[0]
            for column in cont:
                for dl in column.select("dl"):
                    title = dl.dt.text
                    content = dl.dd.text
                    tooltip = dl.select(".toolTipWrap")
                    if "급여" == title:
                        print("급여", content)
                        if tooltip:
                            content = content.replace(tooltip[0].text, "").strip()
                        income = content
                        print("급여", income)
                    elif "근무일시" == title:
                        print("근무일시", content)
                        if tooltip:
                            content = content.replace(tooltip[0].text, "").strip()
                        work_time = content
                        print("근무일시", work_time)
                    elif "우대사항" == title:
                        result = []
                        for item in dl.select(".toolTipTxt > li"):
                            result.append(item.text.strip())
                        print("우대사항", "\n".join(result))
                        find_who = "\n".join(result)
        except:
            print("ERROR")

        recruitment_number = get_column_value(soup, ".recruit_division_0 #template_divisions_work_dept_nm_0",
                                              default_parser)
        print("RECRUIT_NUMBER", recruitment_number)

        task = get_column_value(soup,
                                ".recruit_division_0 #template_divisions_assign_task_nm_0 > tbody > tr:nth-child(2) > td",
                                default_parser)
        print("TASK", task)

        # 사업내용 가져오기
        company_detail = get_column_value(
            soup, '.jv_header > a.company', href_parser)
        print("COMPANY_DETAIL", company_detail)

        sleep(5)

        driver.get("http://www.saramin.co.kr" + company_detail)

        sleep(5)
        # wait.until(presence_of_element_located(
        #     (By.CSS_SELECTOR, "#company_info_introduce")
        # ))

        company_detail_html = driver.page_source
        company_detail_soup = bs4(company_detail_html, 'html.parser')

        # document.querySelector("#company_info_introduce").textContent.trim()[116:]
        content = ""
        imployee = ""
        sales = ""
        gender = "무관"
        try:
            detail = company_detail_soup.select(".summary > li")

            for li in detail:
                title = li.span.text
                body = li.strong.text
                if "사원수" == title:
                    imployee = body
                elif "매출액" == title:
                    sales = body

            print(f"사원수: {imployee}, 매출액: {sales}")



            data_title = company_detail_soup.select(".info > dt")
            data_content = company_detail_soup.select(".info > dd")

            position = 0
            for i, title in enumerate(data_title):
                if "업종" == title.text or "사업내용" == title.text:
                    content = data_content[i].text

            print(f"사업내용: {content}")
        except:
            print("사업내용 쪽 에러 남")

        company_name_list.append(company_name)
        content_list.append(content)
        aa_list.append("")
        recruitment_number_list.append(recruitment_number)
        task_list.append(task)
        work_location_list.append(work_location)
        url_list.append(row)
        deadline_list.append(deadline)
        imployee_list.append(imployee)
        sales_list.append(sales)
        gender_list.append(gender)
        find_who_list.append(find_who)
        income_list.append(income)
        work_time_list.append(work_time)
        benefit_list.append(benefit)
        resume_format_list.append(resume_submission_format)

    print(">> Excel 파일로 저장을 시작합니다.")
    df = pd.DataFrame({
        "사업장명(회사이름)": company_name_list,
        "사업내용": content_list,
        "모집직종": aa_list,
        "모집인원": recruitment_number,
        "직무내용": task_list,
        "근무지주소": work_location_list,
        "소재지주소": work_location_list,
        "공지사이트": url_list,
        "서류마감": deadline_list,
        "근로자 수": imployee_list,
        "매출액": sales_list,
        "성별": gender_list,
        "우대조건": find_who_list,
        "임금액": income_list,
        "근무시간": work_time_list,
        "복리후생": benefit_list,
        "제출서류": resume_format_list
    })

    save_time = datetime.now().strftime("%Y_%m_%d_%H시%M분")
    name = '{}_채용공고.csv'
    df.to_csv('{}utf_채용공고.csv'.format(save_time), encoding='utf-8-sig')
    # df.to_csv(name.format(save_time), encoding='euc-kr')
    print(">> Excel 파일로 저장을 완료했습니다.")