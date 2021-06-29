from vdr.vdr import Vdr

VDR = Vdr()
VDR.add_connection("localhost", 12345, "test1")
VDR.add_connection("localhost", 12346, "test2")

VDR.receiving_frame("test1")
