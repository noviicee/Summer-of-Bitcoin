# Import modules 
import pandas as pd

# Import mempool.csv file into a Dataframe using pandas by reading from mempool.csv
dataframe  = pd.read_csv("mempool.csv")
print(dataframe.head())

"""just for visulaization
"""
# print number of rows and columns
print(dataframe.shape)

# print the data types 
print(dataframe.dtypes)

# concise summary of DataFrame
print(dataframe.info)

# decription of the dataframe
print(dataframe.describe())


"""actual approach
"""
def sort_trans(dataframe, maxfee, minwght):
    """Sorting the Dataframe using sort_values for Fee & Weight.
    Maximise the fee & minimise the weight
    """
    dataframe = dataframe.sort_values([maxfee, minwght], ascending=[False, True]).reset_index(drop=True)
    return dataframe


def check_weight(x):
    """Checks for the upper bound of weight.
    Maximum weight should be less than 4000000
    """
    if min_weight + x['weight'] <= highest_weight:
        return True
    else:
        return False


def check_list(x):
    """Checks if the id is already existing in the final set.
    """
    if str(x) in final_set_of_txids:
        return True
    else:
        return False

def check_parent(x):
    """Checks if the parent id is already existing in the final set.
    If it exists, go to that transaction and include it in output block.
    Else,
    add parent to the list(if eligible) before adding the child.
    """
    if str(x[3]) != "nan":
        parent_list = str(x[3]).split(";")
        for i in parent_list:
            if(check_list(i)):
                continue
            else:
                txnindex = dataframe[dataframe['tx_id'] == i].index.item()
                k = dataframe.loc[txnindex]
                check_add_txn(k)

# Adding appropiate txids to block.txt
def add_to_block(x):
    global min_weight
    txnID = x[0]
    weight = x[2]
    min_weight += weight
    final_set_of_txids.append(txnID)

def check_add_txn(x):
    if(check_weight(x)):
        if(not check_list(x)):
            check_parent(x)
            if(check_weight(x)):
                add_to_block(x)


def Main(dataframe):
    sorted_transactions = sort_trans(dataframe, "fee", "weight")
    for i in range(len(sorted_transactions)):
        txnVar =  sorted_transactions.loc[i]
        check_add_txn(txnVar)


def write_to_file(fin_list):
    file = open("block.txt","a")
    for i in fin_list:
        file.write(str(i) + '\n')
    file.close()


if __name__=="__main__":
    highest_weight = 4000000
    min_weight = 0
    final_set_of_txids = []

    data = dataframe
    Main(data)

    write_to_file(final_set_of_txids)
