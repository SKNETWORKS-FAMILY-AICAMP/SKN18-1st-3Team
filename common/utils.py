from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd

#close_popups
def close_popups(driver):
    
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print("팝업 내용:", alert.text)
        alert.accept()  # 또는 alert.dismiss()
    except NoAlertPresentException:
        print("팝업 없음.")


def set_options(driver):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ico_querySetting"))
    ).click()


# <select> 박스에서 항목 선택 
def select_item(driver,item):
    element = driver.find_element(By.ID, "stat_box")
    select_element = Select(element)
    select_element.select_by_visible_text(item)
    print("선택완료")

#연도별이면 행렬 전환
def create_dataframe(th_list, data):
    df = pd.DataFrame(data, columns=[""] + th_list)
    # if name = :
    #     df = df.transpose()
    #     df.columns = df.iloc[0]
    #     df = df[1:]
    #     df.reset_index(inplace=True)
    #     df.rename(columns={"index": "연도"}, inplace=True)
    return df


def save_as_csv(df,name):
    print(df)
    df.to_excel(f"{name}.xlsx", index=False)