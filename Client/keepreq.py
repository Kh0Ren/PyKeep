import sys
import argparse


def createparser():
    parser = argparse.ArgumentParser()

    return parser


parser = createparser()
namespace = parser.parse_args(sys.argv)
