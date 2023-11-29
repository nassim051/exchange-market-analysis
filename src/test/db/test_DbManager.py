import pytest, os, sys
path=os.path.join(os.path.dirname( __file__),'../..')
sys.path.insert(0,path)
import db.DbManager as dbm
sys.path.pop(0)

# Fixture to create and return a DatabaseManager instance
@pytest.fixture
def db_manager():
    return dbm.DbManager()
@pytest.mark.skip
def test_create_table(db_manager):
    db_manager.create_table("test_table", ["id INTEGER", "name TEXT"])
    result = db_manager.fetch_all("PRAGMA table_info(test_table);")
    assert len(result) == 2
    db_manager.delete_table("test_table")
@pytest.mark.skip
def test_execute(db_manager):
    # Create a test table
    db_manager.create_table("test_table", ["id INTEGER", "name TEXT"])
    
    # Insert data into the test table
    db_manager.insert_into_table("test_table", (1, "Alice"))
    
    # Define a query to update data
    update_query = "UPDATE test_table SET name=? WHERE id=?;"
    
    # Execute the query with parameters
    params = ("Bob", 1)
    db_manager.execute(update_query, params)
    
    # Fetch data from the test table
    result = db_manager.select_from_table("test_table")
    
    # Check that the data has been updated
    assert result[0][1] == "Bob"

    # Delete the test table
    db_manager.delete_table("test_table")
@pytest.mark.skip
def test_insert_select_delete(db_manager):
    db_manager.insert_into_table('volume4h',("BTC",0,0,0))
    db_manager.insert_into_table('volume4h',("BTC_USDT",4000000,200000,200000))
@pytest.mark.skip
def test_select_columns_withConditions(db_manager):
    vol="SWAP_USDT"
    selected_data = db_manager.select_from_table("volume4h", columns=["volume"],conditions=[f"symbol='{vol}'"])[0][0]
    print(selected_data)
    print(type(selected_data))
@pytest.mark.skip
def test_turnToList(db_manager):
    selected_data = db_manager.select_from_table("volume4h", columns=["symbol"],conditions=["volume!=0"])
    result=db_manager.turnToList(selected_data)
    print(result)

      
@pytest.mark.skip   
def test_fetch_one(db_manager):
    # Create table
    db_manager.create_table("test_table", ["id INTEGER", "name TEXT"])

    # Insert data
    db_manager.insert_into_table("test_table", (1, "Alice"))
    db_manager.insert_into_table("test_table", (2, "Bob"))

    # Fetch one
    result = db_manager.fetch_one("SELECT * FROM test_table WHERE id = ?", (1,))
    assert result[1] == "Alice"
@pytest.mark.skip
def test_renitialise(db_manager):
    # Create table
    db_manager.create_table("test_table", ["id INTEGER", "name TEXT"])
    
    # Insert data
    db_manager.insert_into_table("test_table", (1, "Alice"))
    db_manager.insert_into_table("test_table", (2, "Bob"))
    
    # Check initial row count
    initial_row_count = len(db_manager.select_from_table("test_table"))
    
    # Call renitialise
    db_manager.renitialise("test_table")
    
    # Check row count after renitialise
    row_count_after_renitialise = len(db_manager.select_from_table("test_table"))
    
    # Check that the row count has been reset to 0
    assert row_count_after_renitialise == 0
    
    # Delete table
    db_manager.delete_table("test_table")
# Close the connection after all tests
@pytest.mark.skip
def test_teardown(db_manager):
    db_manager.close()
@pytest.mark.skip
def test_update(db_manager):
    db_manager.update('volume4h',column='volume',newValue=6,conditionName='symbol',conditionValue='BTC_USDT')

def test_increment(db_manager):
    symbol='btc_usdt'
    exchange='lbank'
    db_manager.increment('pairwithliquidity',column='gap',newValue=str(2),condition=[f"symbol='{symbol}'",f"exchange='{exchange}'"])
    