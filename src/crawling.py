from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os
import sys

# 폴더 탐색을 위한 경로 설정
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

# from common.utils import close_popups
from common.utils import select_item, create_dataframe, save_as_csv

name_list = ["자동차_등록_현황","차종별_자동차_등록현황","용도별_자동차_등록_현황","시도별_자동차_등록_현황"]
item_list = ["자동차 등록 현황","차종별 자동차 등록현황","용도별 자동차 등록 현황","시도별 자동차 등록 현황"]
table_list = ["t_Table_125701","t_Table_125702","t_Table_125703","t_Table_125704"]

index = 3

name = name_list[index]
item = item_list[index]
table_id = table_list[index]

def find_table(soup,table_id):

    # 테이블 컬럼명
    th_list = []
    table = soup.find("table", id=table_id)
    thead = table.find("thead")
    th=thead.find_all("th")

    for t in th:
        text = t.text.strip()
        if text:  # 공백이 아닌 경우만 추가
            th_list.append(text)
    # 테이블을 찾고, 필요한 데이터를 추출하는 로직을 여기에 작성 
    # 예시로 테이블의 첫 번째 행을 출력
    print("테이블 헤더:", th_list)

    data = []
    # tbody 접근
    rows = table.find("tbody").find_all("tr")

    
    for row in rows:
        row_data = []

        # 행 제목
        row_th = row.find("th")

        if row_th:
            row_data.append(row_th.text.strip())
        
        tds = row.find_all("td")
        
        for td in tds:
            row_data.append(td.text.strip())

        data.append(row_data)
    return th_list, data



# Selenium WebDriver 설정 
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.index.go.kr/unity/potal/main/EachDtlPageDetail.do;jsessionid=IviZISOhpLAhhzql_xyVY8ptjtd76567fCuXawKC.node11?idx_cd=1257#"

# URL 접속
driver.get(url)
time.sleep(3)

############ 초기 설정 ###########
# <select> 박스에서 항목 선택 
select_item(driver,item)

#iframe 진입
driver.switch_to.frame("showStblGams")

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# 팝업 닫기
# close_popups(driver)

############ 크롤링 ############    
# 테이블 가져오기
th_list, data = find_table(soup,table_id)

# dataframe화 하기
df = create_dataframe(th_list, data)
save_as_csv(df,name)

# 드라이버 종료
driver.quit()
