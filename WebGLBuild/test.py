import mysql.connector

# 데이터베이스 연결
db = mysql.connector.connect(
    host="172.30.1.39",
    user="manager",
    password="1234",
    database="yori_db"
)

cursor = db.cursor()

try:
    # 트랜잭션 시작
    cursor.execute("START TRANSACTION")

    # orders 테이블 제약조건 수정
    cursor.execute("""
        ALTER TABLE orders 
        MODIFY COLUMN order_status ENUM('Waiting', 'Preparing', 'Cooking', 'Plating', 'Delivering', 'Completed')
    """)

    # order_detail 테이블 제약조건 수정
    cursor.execute("""
        ALTER TABLE order_detail 
        MODIFY COLUMN cook_status ENUM('Waiting', 'Preparing', 'Cooking', 'Plating', 'Delivering', 'Completed')
    """)

    # 트랜잭션 커밋
    db.commit()
    print("Table columns updated successfully!")

except Exception as e:
    # 오류 발생 시 롤백
    db.rollback()
    print("Failed to update tables:", e)

finally:
    cursor.close()
    db.close()
