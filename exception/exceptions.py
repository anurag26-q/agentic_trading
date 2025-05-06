import sys
import os
class TradingBotException(Exception):
    def __init__(self,error_messages,error_detail:sys):
        self.error_messages=error_messages

        _,_,exc_tb=error_detail.exc_info()

        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename


    def __str__(self):
        return f'Error occured in python script name [{self.file_name}] Line Number [{self.lineno}] error mesage [{self.error_messages}]'

    