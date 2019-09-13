    
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# file name: mac_manuf_api_rest.py
#

import os, re
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mac_manuf_table_def import MacAddressManuf

ROOT_DIR = "manuf"
FINAL_MANUF_DB_FILENAME = "mac_address_manuf.db"

engine = create_engine("sqlite:///" + os.path.join(ROOT_DIR, FINAL_MANUF_DB_FILENAME))
Session = sessionmaker(bind=engine)

app = Flask(__name__)

# 
# API Rest:
# # i.e. http://localhost:5000/chilcano/api/manuf/00:50:5a:e5:6e:cf
# 
@app.route("/srujana28/api/manuf/<string:macAddress>", methods=["GET"])
def get_manuf(macAddress):
    try:
        if re.search(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', macAddress.strip(), re.I).group():
            # expected MAC formats : a1-b2-c3-p4-q5-r6, a1:b2:c3:p4:q5:r6, A1:B2:C3:P4:Q5:R6, A1-B2-C3-P4-Q5-R6
            mac1 = macAddress[:2] + ":" + macAddress[3:5] + ":" + macAddress[6:8]
            mac2 = macAddress[:2] + "-" + macAddress[3:5] + "-" + macAddress[6:8]
            mac3 = mac1.upper()
            mac4 = mac2.upper()
            session = Session()
            result = session.query(MacAddressManuf).filter(MacAddressManuf.mac.in_([mac1, mac2, mac3, mac4])).first()
            try:
                return jsonify(mac=result.mac, manuf=result.manuf, manuf_desc=result.manuf_desc)
            except:
                return jsonify(error="The MAC Address '" + macAddress + "' does not exist"), 404
        else:
            return jsonify(mac=macAddress, manuf="Unknown", manuf_desc="Unknown"), 404
    except:
        return jsonify(error="The MAC Address '" + macAddress + "' is malformed"), 400

if __name__ == "__main__":
     app.run(debug=True,host="0.0.0.0")
