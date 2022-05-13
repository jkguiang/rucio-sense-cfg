from scheduler import TransferScheduler

import argparse
import logging
import sys

def main(args) -> None:
    tsched = TransferScheduler(args.source, args.destination, args.numTransfers)
    tsched.startTransfers()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run TPC Tests')
    parser.add_argument('--source', type=str, help='Source Server')
    parser.add_argument('--destination', type=str, help='Dest Server')
    parser.add_argument('--numTransfers', type=int, help='# of Transfers')
    args = parser.parse_args()
    main(args)
