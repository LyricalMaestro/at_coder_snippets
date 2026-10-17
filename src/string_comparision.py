from typing import List


class SuffixArrayBuilder:
    """
    指定した文字列に対応するSurffix Arrayを構築するためのクラス
    """

    def __init__(self, bucket_chars: str):
        self.bucket_chars = bucket_chars

    def build_by_sa_is(self, S: str) -> List[int]:
        """Build suffix array by SA-IS algorithm.

        Args:
            S (str): target string

        Returns:
            List[int]: suffix array
        """
        S = S + "$"
        
        # Step 1: L型とS型の判定
        ls_array = self._judge_type_l_or_s(S)

        # Step 2: LMSの設定
        lms_array = [False] * len(S)
        for i in range(1, len(S) - 1):
            if ls_array[i - 1] == "L" and ls_array[i] == "S":
                lms_array[i] = True
        lms_array[-1] = True

        # Step 3: LMS部分文字列を入れる
        bucket_map_index = {}
        for i in reversed(range(len(S))):
            if lms_array[i]:
                if S[i] not in bucket_map_index:
                    bucket_map_index[S[i]] = []
                bucket_map_index[S[i]].append(i)

        # Step 4: L型文字を並べる
        for s in "$" + self.bucket_chars:
            if s in bucket_map_index:
                for j in bucket_map_index[s]:
                    if j > 0:
                        if ls_array[j - 1] == "L": 
                            s0 = S[j - 1]
                            if s0 not in bucket_map_index:
                                bucket_map_index[s0] = []
                            bucket_map_index[s0].append(j - 1)
        
        # Step 5: LMS型部分文字列削除
        new_bucket_map_index = {}
        for key, array in bucket_map_index.items():
            remaind_target = []
            for i in range(len(array)):
                if not (lms_array[array[i]] and array[i] != len(S) - 1):
                    remaind_target.append(array[i])
            new_bucket_map_index[key] = remaind_target

        for array in new_bucket_map_index.values():
            array.reverse()

        # Step 6: S型文字列を追加していく
        for s in reversed("$" + self.bucket_chars):
            if s in new_bucket_map_index:
                for j in new_bucket_map_index[s]:
                    if j > 0:
                        if ls_array[j - 1] == "S":
                            s0 = S[j - 1]
                            if s0 not in new_bucket_map_index:
                                new_bucket_map_index[s0] = []
                            new_bucket_map_index[s0].append(j - 1)
        
        for array in new_bucket_map_index.values():
            array.reverse()

        # Step 7: Suffix Arrayを作る
        suffix_array = []
        for s in self.bucket_chars:
            if s in new_bucket_map_index:
                for j in new_bucket_map_index[s]:
                    suffix_array.append(j)

        return suffix_array
    
    def _judge_type_l_or_s(self, S: str) -> List[str]:
        ls_array = [""] * len(S)
        ls_array[-1] = "S"
        for i in reversed(range(len(S) - 1)):
            if S[i] < S[i + 1]:
                ls_array[i] = "S"
            elif S[i] > S[i + 1]:
                ls_array[i] = "L"
            else:
                ls_array[i] = ls_array[i + 1]
        return ls_array
    

if __name__ == "__main__":
    builder = SuffixArrayBuilder("abcdefghijklmnopqrstuvwxyz")
    sa1 = builder.build_by_sa_is("toukoudai")
    sa2 = builder.build_by_sa_is("zazazazaz")

    print(sa1)
    print(sa2)
