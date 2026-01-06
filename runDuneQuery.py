
def updateQuery (inputID):
#actually runs and updates query table

    import dotenv, os
    from dune_client.client import DuneClient
    from dune_client.query import QueryBase

    # change the current working directory where .env file lives
    os.chdir("/home/imimim/alchemix/dune")
    # load .env file
    dotenv.load_dotenv("dune.env")
    # setup Dune Python client
    dune = DuneClient.from_env()

    query = QueryBase(
        query_id=inputID,

        # uncomment and change the parameter values if needed
        # params=[
        #     QueryParameter.text_type(name="contract", value="0x6B175474E89094C44Da98b954EedeAC495271d0F"), # default is DAI
        #     QueryParameter.text_type(name="owner", value="owner"), # default using vitalik.eth's wallet
        # ],
    )

    #query_result = dune.run_query_dataframe(
    query_result = dune.run_query(
        query=query
    # , ping_frequency = 10 # uncomment to change the seconds between checking execution status, default is 1 second
    # , performance="large" # uncomment to run query on large engine, default is medium
    # , batch_size = 5_000 # uncomment to change the maximum number of rows to retrieve per batch of results, default is 32_000
    )

    # Note: to get the result in csv format, call run_query_csv(); for json format, call run_query().

    return (query_result.result.rows)

def getQuery (inputID):
# just gets the most recent query results without re-running the query

    import dotenv, os
    from dune_client.client import DuneClient
    from dune_client.query import QueryBase

    # change the current working directory where .env file lives
    os.chdir("/home/imimim/alchemix/dune")
    # load .env file
    dotenv.load_dotenv("dune.env")
    # setup Dune Python client
    dune = DuneClient.from_env()

    print('Getting data for Query ', inputID)

    return dune.get_latest_result(inputID).result.rows

#results = getQuery(5946834)

#print(results)
#for item in results:
 #   print(item)