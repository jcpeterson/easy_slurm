import argparse
#from tensorflow.python.client import device_lib
#print(device_lib.list_local_devices())

parser = argparse.ArgumentParser()
parser.add_argument("--int", type=int)
parser.add_argument("--str", type=str)
parser.add_argument("--float", type=float)
#parser.add_argument("--bool", type=bool)
parser.add_argument('--include_flag', action='store_true',
                                      default=False)

args = parser.parse_args()

for arg in vars(args):
     print('Name:', arg, 
           'Type:', type(getattr(args, arg)),
           'Value:', getattr(args, arg))