from datetime import datetime

def 대여_시간_계산(대출일자, 반납일자):
    """
    대출일자와 반납일자를 받아서 대여 시간을 계산하는 함수입니다.
    :param 대출일자: 대출일자 문자열 (형식: "YYYY-MM-DD")
    :param 반납일자: 반납일자 문자열 (형식: "YYYY-MM-DD")
    :return: 대여 시간 (일수)
    """
    대출일자_객체 = datetime.strptime(대출일자, "%Y-%m-%d")
    반납일자_객체 = datetime.strptime(반납일자, "%Y-%m-%d")
    
    대여_시간 = (반납일자_객체 - 대출일자_객체).days
    
    return 대여_시간


def 규칙_확인(회원_등급, 대여_시간):
    규칙 = {
        'A': [
            {'대여_시간': lambda x: x <= 7, '무료_대여': True, '연체료_5000원': False, '연체료_10000원': False, '블랙리스트': False},
            {'대여_시간': lambda x: x > 7, '무료_대여': False, '연체료_5000원': True, '연체료_10000원': False, '블랙리스트': False}
        ],
        'B': [
            {'대여_시간': lambda x: x <= 7, '무료_대여': True, '연체료_5000원': False, '연체료_10000원': False, '블랙리스트': False},
            {'대여_시간': lambda x: 7 < x <= 14, '무료_대여': False, '연체료_5000원': True, '연체료_10000원': False, '블랙리스트': False},
            {'대여_시간': lambda x: x > 14, '무료_대여': False, '연체료_5000원': False, '연체료_10000원': True, '블랙리스트': False}
        ],
        'C': [
            {'대여_시간': lambda x: x <= 7, '무료_대여': False, '연체료_5000원': False, '연체료_10000원': False, '블랙리스트': True},
            {'대여_시간': lambda x: 7 < x <= 14, '무료_대여': False, '연체료_5000원': False, '연체료_10000원': True, '블랙리스트': False},
            {'대여_시간': lambda x: x > 14, '무료_대여': False, '연체료_5000원': False, '연체료_10000원': False, '블랙리스트': True}
        ]
    }

    for rule in 규칙[회원_등급]:
        if rule['대여_시간'](대여_시간):
            return {
                '무료_대여': rule['무료_대여'],
                '연체료_5000원': rule['연체료_5000원'],
                '연체료_10000원': rule['연체료_10000원'],
                '블랙리스트': rule['블랙리스트']
            }

    return None  # 해당 규칙이 없을 경우