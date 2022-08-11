import grpc
import sys
import pd.MBARTLarge50_pb2 as Pdm
import pd.MBARTLarge50_pb2_grpc as MBrpc

def run():
  channel = grpc.insecure_channel('127.0.0.1:50051')
  stub = MBrpc.MBARTLarge50Stub(channel)
  print("输入:")
  for line in sys.stdin:
      print("翻译中...")
      response = stub.InterpretE2C(Pdm.EnglishRequest(message=line))
      print( " => 【"+str(response.message)+"】")
      print("输入:")
if __name__ == '__main__':
    run()