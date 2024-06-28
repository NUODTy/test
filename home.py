import streamlit as st
import psycopg2
import pandas as pd




# 初始化登录状态为 False
if "success" not in st.session_state:
    st.session_state.success = False

# 如果登录成功，则显示欢迎页面
if st.session_state.success:
    pass  # 显示欢迎页面
else:
    # 登录页面
    st.title("Welcome!!!")
    st.header("登录页面")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    if st.button("登录"):
        if username == "xlw" and password == "111000":
            st.session_state.success = True  # 更新登录状态
            st.session_state.username = username  # 保存用户名
            st.success("登录成功")
            st.experimental_rerun()  # 刷新页面
        else:
            st.error("用户名或密码错误")

    if st.button("注册新用户"):
        new_username = st.text_input("新用户名")
        new_password = st.text_input("新密码", type="password")
        if st.button("确认注册"):
            # 连接到数据库
            conn = psycopg2.connect(
                dbname="首页",
                user="postgres",
                password="111000",
                host="localhost"
            )
            
            # 创建一个数据库游标
            cur = conn.cursor()

            # 创建一个数据库表格，用于存储用户信息
            cur.execute('''CREATE TABLE IF NOT EXISTS users (username VARCHAR(50), password VARCHAR(50))''')
            
            # 将新用户名和密码插入到数据库中的用户表中
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_username, new_password))
            
            # 提交更改
            conn.commit()
            
            # 关闭游标和数据库连接
            cur.close()
            conn.close()
            
            st.success("注册成功")



# 如果已经登录成功或者当前是登录操作，则显示目录
if  st.session_state.success or st.session_state.success is None:
    # 替换原有的 st.sidebar.title("HELLO, " + st.session_state.username)
    st.sidebar.title("HELLO, " + st.session_state.username)

    st.sidebar.header("目录")

    # 添加目录选项
    choice = st.sidebar.radio("请选择操作", ["上证指数所有股票数据", "财务报表"])


    if choice == "上证指数所有股票数据":
        # 连接数据库信息
        db_name = 'test500'
        db_user = 'postgres'
        db_password = '111000'
        db_host = 'localhost'
        db_port = '5432'

        # 连接到数据库
        conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)

    # 查询数据
        query = "SELECT * FROM sza500"
        data = pd.read_sql(query, conn)

        # 在Streamlit应用程序中显示数据
        st.write("上证指数所有股票的数据：")
        st.write(data)

        # 选择要查看的行
        row_to_display_custom = st.text_input("输入要查看的行的代码或名称")

        if row_to_display_custom:  # 检查输入是否为空
            matched_rows = data[data['代码'].str.contains(row_to_display_custom, case=False, na=False) | data['名称'].str.contains(row_to_display_custom, case=False, na=False)]
            st.write("匹配的行数据：")
            st.write(matched_rows)


        st.divider()
        # 选择要查看的列
        columns_with_empty=['']+list(data.columns)
        column_to_display = st.selectbox("选择要查看的列", columns_with_empty)
        if column_to_display:  # 检查是否已选择列
            if column_to_display != '':  # 如果选择的不是空值
                selected_column = data[column_to_display]
                st.write("选择的列数据：")
                st.write(selected_column)
            else:
                pass
                    # 关闭数据库连接
        conn.close()
                
        # 查询历史数据
        st.divider()        
        db_name = 'history'
        db_user = 'postgres'
        db_password = '111000'
        db_host = 'localhost'
        db_port = '5432'

        # 连接到数据库
        conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        row_to_display_custom = st.text_input("输入要查看历史数据的股票代码")
        query = "SELECT * FROM history WHERE 代码= '{}'".format(row_to_display_custom)
        data = pd.read_sql(query, conn)

        # 在Streamlit应用程序中显示小表格数据
        if not data.empty:
            st.write("代码 {} 的历史数据：".format(row_to_display_custom))
            st.write(data)
        else:
            pass

        # 关闭数据库连接
        conn.close()




    elif choice == "财务报表":
        st.write("暂时可查看的日期有:2024-03-31, 2023-12-31")
        st.header("资产负债表") 
        date_input = st.text_input("请选择日期,例如:2024-03-31")

        if date_input:  # 检查是否输入了日期
            # 连接数据库信息
            db_name = '财务报表'
            db_user = 'postgres'
            db_password = '111000'
            db_host = 'localhost'
            db_port = '5432'

            # 连接到数据库
            conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)

            # 根据日期来查询不同的表格
            if date_input == '2024-03-31':
                query = "SELECT * FROM 资产负债表24年3月"
            elif date_input == '2023-12-31':
                query = "SELECT * FROM 资产负债表23年12月"
            
            data = pd.read_sql(query, conn)

            # 在Streamlit应用程序中显示数据
            st.write("从数据库中检索到的数据：")
            st.write(data)

                # 关闭数据库连接
            conn.close()
            # 用户选择提取的行或列
            operation = st.selectbox("选择要进行的操作", ["提取某一行", "提取某一列"])

            if operation == "提取某一行":
                # 用户输入要提取的行的关键元素值
                key_value = st.text_input("输入要匹配的股票代码或名称")
                if key_value:  # 检查是否输入了关键元素值
                # 根据股票代码或股票名称进行匹配
                    matched_rows = data[data['股票代码'].str.contains(key_value, case=False, na=False) | data['股票简称'].str.contains(key_value, case=False, na=False)]

                # 显示匹配的行数据
                    if not matched_rows.empty:
                        st.write("匹配的行数据：")
                        st.write(matched_rows)
                    else:
                        pass
            if operation == "提取某一列":
                columns_with_empty=['']+list(data.columns)
                column_to_display = st.selectbox("选择要查看的列", columns_with_empty)
                if column_to_display:  # 检查是否已选择列
                    if column_to_display != '':  # 如果选择的不是空值
                        selected_column = data[column_to_display]
                        st.write("选择的列数据：")
                        st.write(selected_column)
                    else:
                        pass


            


        st.divider()
        st.header("利润表")
        date_input = st.text_input("请选择日期,例如:2023-03-31")

        if date_input:  # 检查是否输入了日期
            # 连接数据库信息
            db_name = '财务报表'
            db_user = 'postgres'
            db_password = '111000'
            db_host = 'localhost'
            db_port = '5432'

            # 连接到数据库
            conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)

            # 根据日期来查询不同的表格
            if date_input == '2024-03-31':
                query = "SELECT * FROM 利润表24年3月"
            elif date_input == '2023-12-31':
                query = "SELECT * FROM 利润表23年12月"
            
            data = pd.read_sql(query, conn)

            # 在Streamlit应用程序中显示数据
            st.write("从数据库中检索到的数据：")
            st.write(data)

            # 关闭数据库连接
            conn.close()
                        # 用户选择提取的行或列
            operation = st.selectbox("选择要进行的操作", ["提取某一行", "提取某一列"])

            if operation == "提取某一行":
                # 用户输入要提取的行的关键元素值
                key_value = st.text_input("输入要匹配的股票代码或名称")
                if key_value:  # 检查是否输入了关键元素值
                # 根据股票代码或股票名称进行匹配
                    matched_rows = data[data['股票代码'].str.contains(key_value, case=False, na=False) | data['股票简称'].str.contains(key_value, case=False, na=False)]

                # 显示匹配的行数据
                    if not matched_rows.empty:
                        st.write("匹配的行数据：")
                        st.write(matched_rows)
                    else:
                        pass
            if operation == "提取某一列":
                columns_with_empty=['']+list(data.columns)
                column_to_display = st.selectbox("选择要查看的列", columns_with_empty)
                if column_to_display:  # 检查是否已选择列
                    if column_to_display != '':  # 如果选择的不是空值
                        selected_column = data[column_to_display]
                        st.write("选择的列数据：")
                        st.write(selected_column)
                    else:
                        pass

            

        st.divider()
        st.header("现金流量表")
        date_input = st.text_input("请选择日期,例如:2022-03-31")

        if date_input:  # 检查是否输入了日期
            # 连接数据库信息
            db_name = '财务报表'
            db_user = 'postgres'
            db_password = '111000'
            db_host = 'localhost'
            db_port = '5432'

            # 连接到数据库
            conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)

            # 根据日期来查询不同的表格
            if date_input == '2024-03-31':
                query = "SELECT * FROM 现金流量表24年3月"
            elif date_input == '2023-12-31':
                query = "SELECT * FROM 现金流量表23年12月"
            
            data = pd.read_sql(query, conn)

            # 在Streamlit应用程序中显示数据
            st.write("从数据库中检索到的数据：")
            st.write(data)

            # 关闭数据库连接
            conn.close()
                        # 用户选择提取的行或列
            operation = st.selectbox("选择要进行的操作", ["提取某一行", "提取某一列"])

            if operation == "提取某一行":
                # 用户输入要提取的行的关键元素值
                key_value = st.text_input("输入要匹配的股票代码或名称")
                if key_value:  # 检查是否输入了关键元素值
                # 根据股票代码或股票名称进行匹配
                    matched_rows = data[data['股票代码'].str.contains(key_value, case=False, na=False) | data['股票简称'].str.contains(key_value, case=False, na=False)]

                # 显示匹配的行数据
                    if not matched_rows.empty:
                        st.write("匹配的行数据：")
                        st.write(matched_rows)
                    else:
                        pass
            if operation == "提取某一列":
                columns_with_empty=['']+list(data.columns)
                column_to_display = st.selectbox("选择要查看的列", columns_with_empty)
                if column_to_display:  # 检查是否已选择列
                    if column_to_display != '':  # 如果选择的不是空值
                        selected_column = data[column_to_display]
                        st.write("选择的列数据：")
                        st.write(selected_column)
                    else:
                        pass











    


