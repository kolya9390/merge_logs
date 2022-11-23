import json
import time
import argparse
from pathlib import Path


def _parse_logs():
    parser = argparse.ArgumentParser(description='add path two logs file')
    parser.add_argument('log_file_A', type=str, metavar='< <path/to/dir/log_A> ')
    parser.add_argument('log_file_B', type=str, metavar='< <path/to/dir/log_B>')
    parser.add_argument('-o', '--output', type=str, default='log_merged.jsonl', \
                        dest='merge_file', metavar='<path/to/merged_log>')

    return parser.parse_args()


def merge_log(path_log_file_A: Path, path_log_file_B: Path, path_merge_file):
    with open(path_log_file_A, mode='rb') as log_a, \
            open(path_log_file_B, mode='rb') as log_b, \
            open(path_merge_file, mode='wb') as res:
        lst_1 = log_a.readline()
        lst_2 = log_b.readline()
        while True:
            if lst_1 and lst_2:
                if json.loads(lst_1).get('timestamp') <= json.loads(lst_2).get('timestamp'):
                    res.write(lst_1)
                    lst_1 = log_a.readline()
                elif json.loads(lst_1).get('timestamp') > json.loads(lst_2).get('timestamp'):
                    res.write(lst_2)
                    lst_2 = log_b.readline()
            elif not lst_1 and lst_2:
                res.write(lst_2)
                lst_2 = log_b.readline()
            elif lst_1 and not lst_2:
                res.write(lst_1)
                lst_1 = log_a.readline()
            else:
                break


def merge_sort_quick(path_log_file_A: Path, path_log_file_B: Path, path_merge_file):
    with open(path_log_file_A, mode='rb') as log_a, \
            open(path_log_file_B, mode='rb') as log_b, \
            open(path_merge_file, mode='wb') as res:
        result_lst = log_a.readlines() + log_b.readlines()
        res.writelines(sorted(result_lst, key=lambda x: json.loads(x).get('timestamp')))


def main() -> None:
    args = _parse_logs()

    t0 = time.time()
    path_log_file_A = Path(args.log_file_A)
    path_log_file_B = Path(args.log_file_B)
    path_merge_file = Path(args.merge_file)
    merge_log(path_log_file_A, path_log_file_B, path_merge_file)
    print(f"finished in {time.time() - t0:0f} sec")


if __name__ == '__main__':
    main()