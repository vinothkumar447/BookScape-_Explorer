import pymysql
import pandas as pd
import streamlit as st
from pymysql.cursors import DictCursor

# Function to establish database connection
def connect_to_database():
    try:
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            password="Vinoth@2001",
            database="books",
            autocommit=True
        )
        # Use DictCursor for the cursor, which allows dictionary-based access
        mycursor = mydb.cursor(DictCursor)
        return mydb, mycursor
    except pymysql.MySQLError as err:
        st.error(f"Error connecting to the database: {err}")
        return None, None

def run_query(mycursor, query, params=None):
    try:
        mycursor.execute(query, params)
        results = mycursor.fetchall()
        columns = [i[0] for i in mycursor.description]
        df = pd.DataFrame(results, columns=columns)
        return df
    except pymysql.MySQLError as err:
        st.error(f"Error executing query: {err}")
        return None

# Initialize Streamlit app
st.title('BookScape Explorer :book:')

# Sidebar Navigation
choice = st.sidebar.selectbox("Navigation", ["Home", "Explore Books", "Analytics"])

if choice == "Home":
    # Home Page
    st.header("Welcome to BookScape Explorer! 🌟")
    st.subheader("Discover, Explore, and Analyze Books with Ease")

    st.markdown("""
    - 📚 Explore a vast collection of books.
    - 🔍 Search by title, author, or genre.
    - 🌟 Analyze books with advanced tools.
    """)

elif choice == "Explore Books":
    # Connect to the database
    mydb, mycursor = connect_to_database()

    if mydb is not None and mycursor is not None:
        # Search functionality
        keyword = st.text_input("Search for books by keyword:")

        if keyword:
            query = "SELECT * FROM music_book WHERE book_title LIKE %s;"
            results_df = run_query(mycursor, query, ('%' + keyword + '%',))
            if results_df is not None:
                st.write(results_df)

elif choice == "Analytics":
    # Analytics Section
    mydb, mycursor = connect_to_database()

    if mydb is not None and mycursor is not None:
        question = st.selectbox("Select an Analytics Query:", [
            "1. Check Availability of eBooks vs Physical Books",
            "2. Find the Publisher with the Most Books Published",
            "3. Identify the Publisher with the Highest Average Rating",
            "4. Get the Top 5 Most Expensive Books by Retail Price",
            "5. Find Books Published After 2010 with at Least 500 Pages",
            "6. List Books with Discounts Greater than 20%",
            "7. Find the Average Page Count for eBooks vs Physical Books",
            "8. Find the Top 3 Authors with the Most Books",
            "9. List Publishers with More than 10 Books",
            "10. Find the Average Page Count for Each Category",
            "11. Retrieve Books with More than 3 Authors",
            "12. Books with Ratings Count Greater Than the Average",
            "13. Books with the Same Author Published in the Same Year",
            "14. Books with a Specific Keyword in the Title",
            "15. Year with the Highest Average Book Price",
            "16. Count Authors Who Published 3 Consecutive Years",
            "17. Authors Who Have Published Books in the Same Year Under Different Publishers",
            "18. Average Retail Price of eBooks vs Physical Books",
            "19. Books with Ratings More than 2 Standard Deviations Away from Average Rating",
            "20. Publisher with Highest Average Rating (More Than 10 Books)"
        ])

        if question == "1. Check Availability of eBooks vs Physical Books":
            query = "SELECT isEbook, COUNT(*) AS book_count FROM music_book GROUP BY isEbook;"
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        elif question == "2. Find the Publisher with the Most Books Published":
            query = "SELECT publisher, COUNT(*) AS book_count FROM music_book GROUP BY publisher ORDER BY book_count DESC LIMIT 1;"
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        elif question == "3. Identify the Publisher with the Highest Average Rating":
            query = """
            SELECT 
                publisher, 
                AVG(averagerating) AS avg_rating 
            FROM music_book 
            GROUP BY publisher 
            ORDER BY avg_rating DESC 
            LIMIT 1;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)
                
        elif question == "4. Get the Top 5 Most Expensive Books by Retail Price":
            query = """
            SELECT 
                book_title, 
                amount_retailPrice 
            FROM music_book 
            ORDER BY amount_retailPrice DESC 
            LIMIT 5;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)        

        elif question == "5. Find Books Published After 2010 with at Least 500 Pages":
            query = """
            SELECT 
                book_title, 
                year, 
                pagecount 
            FROM music_book 
            WHERE year > 2010 AND pagecount >= 500;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        elif question == "6. List Books with Discounts Greater than 20%":
            query = """
            SELECT 
                book_title, 
                amount_listPrice, 
                amount_retailPrice, 
                (amount_listPrice - amount_retailPrice) / amount_listPrice * 100 AS discount_percentage 
            FROM music_book 
            WHERE amount_listPrice > 0 AND (amount_listPrice - amount_retailPrice) / amount_listPrice > 0.2;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        # Query for "7. Find the Average Page Count for eBooks vs Physical Books"
        elif question == "7. Find the Average Page Count for eBooks vs Physical Books":
            query = """
            SELECT 
                CASE WHEN isebook = 1 THEN 'eBook' ELSE 'Physical Book' END AS book_type, 
                AVG(pagecount) AS avg_page_count 
            FROM music_book 
            GROUP BY isebook;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        # Query for "8. Find the Top 3 Authors with the Most Books"
        elif question == "8. Find the Top 3 Authors with the Most Books":
            query = """
            SELECT 
                book_authors, 
                COUNT(*) AS book_count 
            FROM music_book 
            GROUP BY book_authors 
            ORDER BY book_count DESC 
            LIMIT 3;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        # Query for "9. List Publishers with More than 10 Books"
        elif question == "9. List Publishers with More than 10 Books":
            query = """
            SELECT 
                publisher, 
                COUNT(*) AS book_count 
            FROM music_book 
            GROUP BY publisher 
            HAVING book_count > 10;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        # Query for "10. Find the Average Page Count for Each Category"
        elif question == "10. Find the Average Page Count for Each Category":
            query = """
            SELECT 
                category, 
                AVG(pagecount) AS avg_page_count 
            FROM music_book 
            GROUP BY category;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        # Query for "11. Retrieve Books with More than 3 Authors"
        elif question == "11. Retrieve Books with More than 3 Authors":
            query = """
            SELECT 
                book_title, 
                book_authors 
            FROM music_book 
            WHERE LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) + 1 > 3;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        # Query for "12. Books with Ratings Count Greater Than the Average"
        elif question == "12. Books with Ratings Count Greater Than the Average":
            query = """
            SELECT 
                book_title, 
                ratings_count 
            FROM music_book 
            WHERE ratings_count > (SELECT AVG(ratings_count) FROM music_book);
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        # Query for "13. Books with the Same Author Published in the Same Year"
        elif question == "13. Books with the Same Author Published in the Same Year":
            query = """
            SELECT 
                book_title, 
                book_authors, 
                year 
            FROM music_book 
            WHERE book_authors IN (SELECT book_authors 
                                    FROM music_book 
                                    GROUP BY book_authors, year 
                                    HAVING COUNT(*) > 1);
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        # Query for "14. Books with a Specific Keyword in the Title"
        elif question == "14. Books with a Specific Keyword in the Title":
            keyword = st.text_input("Enter Keyword to Search in Book Titles:")
            if keyword:
                query = f"SELECT book_title FROM music_book WHERE book_title LIKE '%{keyword}%';"
                results_df = run_query(mycursor, query)
                if results_df is not None:
                    st.write(results_df)

        # Query for "15. Year with the Highest Average Book Price"
        elif question == "15. Year with the Highest Average Book Price":
            query = """
            SELECT 
                year, 
                AVG(amount_retailPrice) AS avg_price 
            FROM music_book 
            GROUP BY year 
            ORDER BY avg_price DESC 
            LIMIT 1;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        # Query for "16. Count Authors Who Published 3 Consecutive Years"
        elif question == "16. Count Authors Who Published 3 Consecutive Years":
            query = """
            SELECT 
                book_authors, 
                COUNT(DISTINCT year) AS year_count 
            FROM music_book 
            GROUP BY book_authors 
            HAVING year_count >= 3;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        # Query for "17. Authors Who Have Published Books in the Same Year Under Different Publishers"
        elif question == "17. Authors Who Have Published Books in the Same Year Under Different Publishers":
            query = """
            SELECT 
                book_authors, 
                year, 
                COUNT(DISTINCT publisher) AS publisher_count 
            FROM music_book 
            GROUP BY book_authors, year 
            HAVING publisher_count > 1;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        # Query for "18. Average Retail Price of eBooks vs Physical Books"
        elif question == "18. Average Retail Price of eBooks vs Physical Books":
            query = """
            SELECT 
                CASE WHEN isebook = 1 THEN 'eBook' ELSE 'Physical Book' END AS book_type, 
                AVG(amount_retailPrice) AS avg_retail_price 
            FROM music_book 
            GROUP BY isebook;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        # Query for "19. Books with Ratings More than 2 Standard Deviations Away from Average Rating"
        elif question == "19. Books with Ratings More than 2 Standard Deviations Away from Average Rating":
            query = """
            SELECT 
                book_title, 
                averagerating 
            FROM music_book 
            WHERE ABS(averagerating - (SELECT AVG(averagerating) FROM music_book)) > 2 * (SELECT STD(averagerating) FROM music_book);
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)

        # Query for "20. Publisher with Highest Average Rating (More Than 10 Books)"
        elif question == "20. Publisher with Highest Average Rating (More Than 10 Books)":
            query = """
            SELECT 
                publisher, 
                AVG(averagerating) AS avg_rating 
            FROM music_book 
            GROUP BY publisher 
            HAVING COUNT(*) > 10 
            ORDER BY avg_rating DESC 
            LIMIT 1;
            """
            results_df = run_query(mycursor, query)
            if results_df is not None:
                st.write(results_df)
