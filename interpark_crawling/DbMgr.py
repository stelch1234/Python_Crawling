# 디비 처리, 연결, 해제, 검색어 가져오기, 데이터 삽입
import pymysql as my


class DBHelper:
    '''
    맴버변수 : 커넥션
    '''
    conn = None
    '''
    생성자 
    '''

    def __init__(self):
        self.db_init()

    '''
    맴버 함수
    '''

    def db_init(self):
        self.conn = my.connect(
            host='localhost',
            user='root',
            password='1234',
            db='pythonDB',
            charset='utf8',
            cursorclass=my.cursors.DictCursor)  # 딕셔너리/ 안쓰면 튜플로 반환

    def db_free(self):  # 해제 코드
        if self.conn:
            self.conn.close()

    # 검색 키워드 가져오기 => 웹에서 검색
    def db_selectKeyword(self):
        # 커서 오픈
        # with => 닫기를 처리를 자동으로 처리해준다 => I/O 많이 사용
        rows = None
        with self.conn.cursor() as cursor:
            sql = "select * from tbl_keyword;"
            cursor.execute(sql)  # 파라미터 넘길때 수행
            rows = cursor.fetchall()  # fetchone은 하나만 들고옴
            print(rows)
        return rows

    def db_insertCrawlingData(self, title, price, area, contents, keyword):
        with self.conn.cursor() as cursor:
            sql = '''
            insert into `tbl_crawlingdata` 
            (title, price, area, contents, keyword) 
            values( %s,%s,%s,%s,%s )
            '''
            cursor.execute(sql, (title, price, area, contents, keyword))
        self.conn.commit()


# 단독으로 수행시에만 작동 => 테스트코드를 삽입해서 사용
if __name__ == '__main__':
    db = DBHelper()  # 연결
    print(db.db_selectKeyword())
    print(db.db_insertCrawlingData('1', '2', '3', '4', '5'))
    db.db_free()  # 해제
