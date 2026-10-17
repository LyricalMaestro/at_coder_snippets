

def make_suffix_array(S: str, is_lower: bool):
    """
    Suffix Arrayを構築します.

    https://atcoder.jp/contests/abc213/tasks/abc213_f
    https://trap.jp/post/953/
    を参考に実装
    """
    base_a = ("a" if is_lower else "A")

    S_star = S + "*"

    # L型かS型かをきめる
    ls_array = [-1] * len(S_star)
    ls_array[-1] = "S"
    for i in reversed(range(len(S_star) - 1)):
        if S_star[i] > S_star[i + 1]:
            ls_array[i] = "S"
        elif S_star[i] < S_star[i + 1]:
            ls_array[i] = "L"
        else:
            ls_array[i] = ls_array[i + 1]
    
    # LMS
    is_lms_array = [False] * len(S_star)
    for i in range(1, len(S_star)):
        if ls_array[i - 1] == "L" and ls_array[i] == "S":
            is_lms_array[i] = True

    # step1. LMS部分文字列を入れていく
    lms_list = []
    bucket_array = [[] for _ in range(27)]
    prev = -1
    filled = [False] * len(S_star)
    for i in reversed(range(len(S_star))):
        if is_lms_array[i] and prev != i:
            if prev == -1:
                s_ = S_star[i]
                s = S_star[i]
            else:
                s_ = S_star[i:(prev + 1)]
                s = S_star[i]

            lms_list.append((s_, i))
            if s == "*":
                bucket_array[0].append(i)
            else:
                o = ord(s) + 1 - ord(base_a)
                bucket_array[o].append(i)
            filled[i] = True
            prev = i

    
    # step2. L型文字を並べる
    for i0 in range(len(bucket_array)):
        for i in bucket_array[i0]:
            if ls_array[i - 1] == "L":
                if not filled[i - 1]:
                    o = ord(S_star[i - 1]) + 1 - ord(base_a)
                    bucket_array[o].append(i)
                    filled[i - 1] = True
    
    # step3. LMS部分文字列を除く
    new_bucket_array = [[] for _ in range(27)]
    for i0 in range(len(bucket_array)):
        for i in bucket_array[i0]:
            if is_lms_array[i]:
                new_bucket_array[i0].append(i)
            else:
                filled[i] = False
    bucket_array = new_bucket_array

    # step4. S型文字列を並べる
    for i0 in reversed(range(bucket_array)):
        for i in reversed(bucket_array[i0]):
            if i > 0:
                if ls_array[i - 1] == "S":
                    if not filled[i - 1]:
                        o = ord(S_star[i - 1]) + 1 - ord(base_a)
                        bucket_array[o].append(i)
                        filled[i - 1] = True
    
    
    # ステップ5 重複するLMS部分文字列と辞書順
    lms_list.sort(key=lambda x : x[0])
    index_list = [-1]
    index = 1
    for i in range(len(lms_list)):
        if i == 0:
            index_list[i] = (index, lms_list[i][1])
        else:
            if lms_list[i][0] != lms_list[i - 1][0]:
                index += 1
            index_list[i]  = (index, lms_list[i][1])

    lms_list.sort(key=lambda x :x[1])
    index_list.sort(key=lambda x :x[1])

    array = []
