import pandas as pd
import sys

def main(input,output):

    df = pd.read_csv(input)
    df = df.replace({'\r': '|'}, regex=True)
    df.to_csv(output, index=False)
if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]
    
    print("usage: python csvConversion.py \"/Users/babu/Documents/hive.csv\" \"/Users/babu/Documents/hiveOutput.csv\"")
    print("python csvConversion.py “input” “output\"")
    main(input,output)
