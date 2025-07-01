from instrument import Instrument
from rigol_ds1000z import Rigol_DS1000Z

with Rigol_DS1000Z() as oscope:
            # reset to defaults and print the IEEE 488.2 instrument identifier
            ieee = oscope.ieee(rst=True)
            print(ieee.idn)