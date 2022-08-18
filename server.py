from concurrent import futures
import grpc
import pd.MBARTLarge50_pb2  as mbPB
import pd.MBARTLarge50_pb2_grpc as mbRPC
import logging
import torch

import dl_translate as dlt

class Mbart(mbRPC.MBARTLarge50Servicer):

    def InterpretE2C(self, request, context):
        m = interpret(request.message)
        return mbPB.ChineseReply(message=str(m))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=500))
    mbRPC.add_MBARTLarge50Servicer_to_server(Mbart(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("启动成功 [::]:50051")
    server.wait_for_termination()


# 翻译
def interpret(article):
    v =  mt.translate(article, source=dlt.lang.ENGLISH, target=dlt.lang.CHINESE)
    return v


if __name__ == '__main__':
    device = torch.device("cuda")
    print("加载训练结果")
    mt = dlt.TranslationModel(device="gpu")
    mt = dlt.TranslationModel("facebook/mbart-large-50-many-to-many-mmt")
    print("启动监听")
    logging.basicConfig()
    serve()