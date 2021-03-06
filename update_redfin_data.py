'''
Created on Mar 13, 2016

@author: pitzer
'''

import logging
import os

from realdeal.fusion_tables_client import FusionTablesClient
from realdeal.redfin_client import RedfinClient, REDFIN_FIELDS

__NEEDS_UPDATE_STATUS = [
  "",
#   "active",
#   "pending",
]

    
def main():
  logging.getLogger().setLevel(logging.INFO)
  fusion_tables = FusionTablesClient(
      table_id=os.environ["REALDEAL_FUSION_TABLE_ID"])
  redfin = RedfinClient()
  
  logging.info("Fetching properties without redfin data from Fusion Table.")
  status_list = ", ".join(["'%s'" % status for status in __NEEDS_UPDATE_STATUS])
  sql = "SELECT "
  sql += ", ".join(REDFIN_FIELDS)
  sql += " FROM " + fusion_tables.table_id
  sql += " WHERE status IN ( %s )" % status_list
  properties = fusion_tables.query(sql)
  
  logging.info("Updating properties.")
  num_updated_properties = 0
  for prop, is_updated in redfin.updatePropertiesWithRedfinData(properties):
    if is_updated:
      fusion_tables.updateRow(prop["rowid"], prop)
      num_updated_properties += 1
  logging.info("%d properties updated." % num_updated_properties)
 
if __name__ == "__main__":
  main()
    


    
    
    
  