from concurrent import futures
import grpc
import pd.MBARTLarge50_pb2  as mbPB
import pd.MBARTLarge50_pb2_grpc as mbRPC
import logging
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

class Mbart(mbRPC.MBARTLarge50Servicer):

    def InterpretE2C(self, request, context):
        m = interpret(request.message)
        return mbPB.ChineseReply(message=str(m[0]))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mbRPC.add_MBARTLarge50Servicer_to_server(Mbart(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("启动成功 [::]:50051 ")
    server.wait_for_termination()


# 翻译
def interpret(article):
    model_inputs = tokenizer(article,return_tensors="pt")

    generated_tokens = model.generate(
        **model_inputs,
        max_length=500,
        forced_bos_token_id=tokenizer.lang_code_to_id["zh_CN"]
    )

    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)



if __name__ == '__main__':

    print("加载训练结果")
    model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-one-to-many-mmt")
    tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-one-to-many-mmt", src_lang="en_XX")
    print("启动监听")
    logging.basicConfig()
    serve()