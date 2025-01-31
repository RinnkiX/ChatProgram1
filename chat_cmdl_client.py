###############################################
#                  Group 14                   #
###############################################
#             Xin Wen (a1893343)              #
#           Yuhang Chen (a1914212)            #
###############################################

from chat_client_class import *


def main():
    import argparse
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    args = parser.parse_args()

    client = Client(args)
    client.run_chat()


main()
