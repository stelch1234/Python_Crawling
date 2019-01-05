#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import re
#번역
from googletrans import Translator
#영어감지
import langdetect
from langdetect.lang_detect_exception import LangDetectException


#데이터 불러오기
headers = ['reviews','reviews_translation']
beer_필스너= pd.read_csv('/Users/stella/Downloads/beer_필스너.csv', encoding = 'utf-8')


#빈칸 처리
beer_필스너.replace('', np.nan, inplace = True)


#영어만 추출하기
text_languages = []
for text in beer_필스너['reviews'].dropna():
    try:
        if detect(text) == 'en' :
            text_languages.append({
        'text' : text,
        'detected language' : langdetect.detect(text)
    })
    except LangDetectException:
        pass


df_필스너 = pd.DataFrame(text_languages)


translator = Translator()

#빈데이터 프레임 만들기
df_필스너_empty = pd.DataFrame(index=range(0,len(df_필스너)), columns=headers)


def translate_row(row):
    a = translator.translate(row[0], dest='ko')
    return pd.Series([a.origin, a.text], headers)

#데이터 채우기 (오류발생)
for i, row in enumerate(df_필스너['text'].values):
    df_필스너_empty.loc[i] = translate_row(row)


df_필스너_empty.to_csv('beer_필스너_번역완료.csv', index=False)