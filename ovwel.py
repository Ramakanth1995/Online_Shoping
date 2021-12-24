s = [11, 12,13,14,15,16,17,18,19,20]

# Output like=[12, 19,14,17,16,15,18,13,20,11]

ind = 0
even = []
odd = []
for i in range(0, len(s)):  # 2

    for j in range(0, len(s)):  #
        if s[i] < s[j] and s[j]%2 != 0:
            ind = s.index(s[j])
        if s[i] < s[j] and s[j]%2 == 0:
            ind = s.index(s[j])

    s.insert(ind + 1, s[i])
    s.remove(s[i])
    ind = 0

even_nos = [num for num in s if num % 2 == 0]
od_nos = [num for num in s if num % 2 != 0]
re = []
print(s,even_nos,od_nos)
for n in range(0,len(even_nos)):
    re.append(even_nos[n])
    re.append(od_nos[n])
print(re)