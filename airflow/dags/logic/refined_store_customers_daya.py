"""
steps :
-------
1.connect db
2.read customers data from raw_layers.sales
3.store results to refiend_layer.customers table
4.close table

We need :
--------
we need to also store ingestion_time
we need to keep track of data that was capied
and not duplicate it once this script is ran again
we need some kind of a check mechanism 
"""