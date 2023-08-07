def minimumDistance(word1, word2):
    matrix = [[0 for _ in range(len(word2) + 1)] for _ in range(len(word1) + 1)]

        for i in range(len(word1)):
            matrix[i][-1] = len(word1) - i
        
        for i in range(len(word2)):
            matrix[-1][i] = len(word2) - i

        for i in range(len(word1) - 1, -1, -1):
            for j in range(len(word2) - 1, -1, -1):
                if word1[i] == word2[j]:
                    matrix[i][j] = matrix[i + 1][j + 1]
                else:
                    matrix[i][j] = 1 + min(matrix[i + 1][j], matrix[i][j + 1], matrix[i + 1][j + 1])
        
        return matrix[0][0]
